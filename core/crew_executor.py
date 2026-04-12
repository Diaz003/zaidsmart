# crew_executor.py
import traceback
import os
import re
import time
from pathlib import Path
from crewai import Task, Crew
from crewai.process import Process

from agents import create_agents
from core.agent_runner import AgentRunner

try:
    from rich.console import Console
    from rich.panel import Panel
    console = Console()
except ImportError:
    console = None

def run_crew_task(runner, task_id, project_id, agent_name, model_id, description):
    runner.update_task(task_id, "running", logs="Iniciando tarea...")
    
    # Lista extendida de modelos gratuitos estables y comprobados en OpenRouter (evitando los 404/400)
    models_to_try = [
        model_id, 
        "google/gemini-2.0-flash-lite:free",
        "google/gemini-flash-1.5-8b:free",
        "meta-llama/llama-3.1-8b-instruct:free",
        "nousresearch/hermes-3-llama-3.1-405b:free"
    ]
    # Eliminar duplicados manteniendo el orden
    models_to_try = list(dict.fromkeys(models_to_try))
    
    last_exc = None
    result_text = None
    model_attempts = []  # Para registrar cada intento y su error

    for current_model in models_to_try:
        attempt_info = {"model": current_model, "status": "skipped", "error": None}
        success = False
        for attempt in range(1, 4):  # Máximo 3 intentos por modelo
            try:
                # -- Callback function for live progress --
                def step_callback(step_output):
                    try:
                        if hasattr(step_output, 'log'):
                            msg = step_output.log
                        elif hasattr(step_output, 'text'):
                            msg = step_output.text
                        else:
                            msg = str(step_output)
                            
                        msg_clean = msg.replace('\n', ' ').replace('`', '').strip()
                        
                        # --- Detector de Progreso Simple ---
                        prog = 10 # Base
                        if "Action:" in msg: prog = 30
                        if "Delegate" in msg or "Delegating" in msg: prog = 50
                        if "I now have a final answer" in msg or "Final Answer" in msg: prog = 90
                        
                        runner.update_task(task_id, "running", logs=runner.get_task(task_id).get("logs", ""), progress=prog)
                        
                        # Imprimir en la terminal del PC con estilo
                        if console:
                            if "Action:" in msg or "Delegate" in msg or "Delegating" in msg:
                                console.print(Panel(f"[bold magenta]{msg_clean}[/bold magenta]", title="[bold yellow]🤖 Interacción entre Agentes[/bold yellow]", border_style="magenta"))
                            else:
                                console.print(Panel(f"[cyan]{msg_clean[:400]}[/cyan]" + ("..." if len(msg_clean)>400 else ""), title="[bold blue]🧠 Proceso[/bold blue]", border_style="blue"))
                                
                        if len(msg_clean) > 100: msg_clean = msg_clean[:97] + "..."
                        runner.append_log(task_id, f"⚙️ {msg_clean}")
                    except: pass

                retry_msg = f" (Intento {attempt}/3)" if attempt > 1 else ""
                runner.append_log(task_id, f"Configurando Agentes (Cerebro: {current_model}){retry_msg}...")
                if console: console.print(f"\n[bold green]🚀 Arrancando Agentes con: [/bold green][white]{current_model}[/white]{retry_msg}")

                workers_registry, manager = create_agents(model_id=current_model, step_callback=step_callback)

                if agent_name == "manager":
                    main_agent = manager
                    workers = list(workers_registry.values())
                    expected_desc = "Un documento completo y estructurado que resuelva el objetivo inicial, combinando el trabajo de los especialistas."
                    task = Task(description=description, expected_output=expected_desc, agent=main_agent)

                    try:
                        runner.append_log(task_id, "Intentando modo Jerárquico (Manager)...")
                        all_agents = [manager] + workers
                        crew = Crew(agents=all_agents, tasks=[task], process=Process.hierarchical, manager_agent=manager, verbose=True)
                        runner.append_log(task_id, f"Lanzando operación con {current_model}...")
                        result = crew.kickoff()
                    except Exception as e:
                        err_msg = str(e).lower()
                        attempt_info["status"] = "tool-fallback"
                        attempt_info["error"] = str(e)
                        if "tool" in err_msg or "endpoint" in err_msg or "404" in err_msg or "delegat" in err_msg:
                            runner.append_log(task_id, "⚠️ El modelo no soporta Tools. Desactivándolas y reintentando en modo SECUENCIAL...")
                            if console: console.print(f"[bold yellow]⚠️ Fallo de Tools: Forzando modo Secuencial sin herramientas...[/bold yellow]")

                            for a in all_agents:
                                a.tools = []
                                a.allow_delegation = False

                            crew = Crew(agents=all_agents, tasks=[task], process=Process.sequential, verbose=True)
                            result = crew.kickoff()
                        else:
                            attempt_info["status"] = "exception"
                            raise e
                else:
                    if agent_name not in workers_registry: raise ValueError(f"Agente {agent_name} no existe.")
                    main_agent = workers_registry[agent_name]
                    expected_desc = "El resultado técnico específico solicitado (documento, código o lista de assets)."
                    task = Task(description=description, expected_output=expected_desc, agent=main_agent)
                    crew = Crew(agents=[main_agent], tasks=[task], verbose=True)
                    runner.append_log(task_id, f"Lanzando agente {agent_name} con {current_model}...")
                    result = crew.kickoff()

                result_text = str(result)
                runner.update_task(task_id, "done", result=result_text, progress=100)
                attempt_info["status"] = "success"
                attempt_info["error"] = None
                model_attempts.append(attempt_info)
                success = True
                break # Éxito en este modelo, salir del bucle de reintentos
                
            except Exception as exc:
                err_str = str(exc).lower()
                attempt_info["status"] = "error"
                attempt_info["error"] = str(exc)
                if "429" in err_str or "rate limit" in err_str:
                    if "free-models-per-day" in err_str:
                        msg = "🛑 Límite DIARIO de modelos gratuitos agotado en OpenRouter. Debes esperar 24h o añadir saldo ($5 USD)."
                        runner.append_log(task_id, msg)
                        result_text = msg
                        model_attempts.append(attempt_info)
                        break # Romper reintentos, pero también saldremos del bucle de modelos abajo
                    attempt_info["status"] = "rate-limited"
                    model_attempts.append(attempt_info)
                    if attempt < 3:
                        wait_time = 20 * attempt # Aumentar tiempo gradualmente
                        runner.append_log(task_id, f"⏳ Rate Limit (429). Esperando {wait_time}s para reintento {attempt}/3 en {current_model}...")
                        time.sleep(wait_time)
                        continue # Reintentar el MISMO modelo
                    else:
                        runner.append_log(task_id, f"❌ Agotados reintentos en {current_model}. Probando siguiente cerebro...")
                        break
                elif "404" in err_str or "not found" in err_str or "tool" in err_str:
                    attempt_info["status"] = "incompatible"
                    model_attempts.append(attempt_info)
                    runner.append_log(task_id, f"🚫 Incompatibilidad en {current_model}. Saltando.")
                    break # Salir de reintentos e ir al siguiente modelo
                else:
                    attempt_info["status"] = "exception"
                    model_attempts.append(attempt_info)
                    runner.append_log(task_id, f"⚠️ Error inesperado: {err_str[:60]}...")
                    break # Otros errores no se reintentan
                last_exc = exc
        if attempt_info["status"] != "success":
            model_attempts.append(attempt_info)
        if success: break # Salir del bucle de modelos si ya funcionó
        if result_text and "🛑 Límite DIARIO" in result_text: break # Salir si es el límite diario

    # Añadir resumen de modelos probados al resultado/logs
    summary = "\n\n---\n<b>Resumen de modelos probados:</b>\n"
    for att in model_attempts:
        summary += f"- {att['model']}: {att['status']}"
        if att['error']:
            summary += f" — {att['error'][:120]}"
        summary += "\n"

    if not result_text:
        err_msg = f"Fallo Crítico: Los modelos gratuitos no responden o son incompatibles. {last_exc}{summary}"
        runner.update_task(task_id, "error", result=err_msg)
        return
    else:
                                                    crew = Crew(agents=workers, tasks=[task], process=Process.hierarchical, manager_agent=manager, verbose=True)

    try:
        
        # --- Guardado de Archivo ---
        project = runner.get_project(project_id)
        project_name = project.get("name", "unnamed_project") if project else "unnamed_project"
        safe_project_name = re.sub(r"[^a-zA-Z0-9_\-]", "_", project_name)
        
        filename = f"resultado_{task_id[:8]}.md"
        custom_out = project.get("output_path", "").strip()
        
        if custom_out:
            output_dir = Path(custom_out)
        else:
            output_dir = Path("output") / safe_project_name

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result_text)
            
        runner.append_log(task_id, f"📁 Guardado en: {output_path}")
        
        current_logs = runner.get_task(task_id).get("logs", "")
        final_logs = f"{current_logs}\n✅ Tarea completada".strip()
        runner.update_task(task_id, "done", result=result_text, logs=final_logs)

    except Exception as exc:
        tb = traceback.format_exc()
        current_logs = runner.get_task(task_id).get("logs", "")
        error_logs = f"{current_logs}\n❌ Error: {exc}\n{tb}".strip()
        runner.update_task(task_id, "error", result=f"Error: {exc}", logs=error_logs)
