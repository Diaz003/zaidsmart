import os
import sys
# Añadir el directorio padre al path para importar agentes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents import create_agents
from crewai import Task, Crew
from crewai.process import Process

def run_test(model_id="google/gemini-2.0-flash-lite:free", task_desc="Explica brevemente qué es la singularidad tecnológica"):
    print(f"\n" + "="*50)
    print(f"🚀 TEST DIRECTO DE AGENTES")
    print(f"Cerebro: {model_id}")
    print(f"="*50 + "\n")
    
    def step_callback(step):
        print(f"⚙️ [PROCESO]: {str(step)[:120]}...")

    try:
        workers, manager = create_agents(model_id=model_id, step_callback=step_callback)
        
        task = Task(
            description=task_desc,
            expected_output="Una explicación técnica concisa y estructurada.",
            agent=manager
        )
        
        # FIX APLICADO: Lista completa de agentes
        all_agents = [manager] + list(workers.values())
        
        crew = Crew(
            agents=all_agents,
            tasks=[task],
            process=Process.hierarchical,
            manager_agent=manager,
            verbose=True
        )
        
        print("🧠 El Manager está analizando la tarea...")
        result = crew.kickoff()
        
        print(f"\n" + "✅"*20)
        print("RESULTADO DEL TEST:")
        print(result)
        print("✅"*20)

    except Exception as e:
        print(f"\n❌ ERROR EN EL TEST: {e}")

if __name__ == "__main__":
    # Permite pasar el modelo como argumento: python direct_test.py "modelo/id:free"
    model = sys.argv[1] if len(sys.argv) > 1 else "google/gemini-2.0-flash-lite:free"
    run_test(model_id=model)
