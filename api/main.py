import asyncio
import uuid
from typing import Optional

from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import httpx
import time
from core.agent_runner import AgentRunner
from core.crew_executor import run_crew_task

# Caché simple para modelos
_cached_models = []
_last_scan_time = 0
SCAN_INTERVAL = 3600 # 1 hora

app = FastAPI(title="Agentes UI")

app.mount("/static", StaticFiles(directory="web/static"), name="static")
templates = Jinja2Templates(directory="web/templates")

runner = AgentRunner()


class ProjectCreate(BaseModel):
    name: str
    output_path: str = ""

class TaskCreate(BaseModel):
    agent_name: str
    model_id: str
    description: str


async def run_agent_in_background(task_id: str, project_id: str, agent_name: str, model_id: str, description: str):
    """Run the real CrewAI agent in a thread so it doesn't block the event loop."""
    await asyncio.to_thread(run_crew_task, runner, task_id, project_id, agent_name, model_id, description)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"request": request},
    )

# --- Projects Endpoints ---

@app.get("/projects")
async def get_projects():
    return runner.list_projects()

@app.post("/projects")
async def create_project(project: ProjectCreate):
    project_id = runner.create_project(project.name, project.output_path)
    return {"ok": True, "project_id": project_id, "name": project.name}

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    runner.delete_project(project_id)
    return {"ok": True}

# --- Tasks Endpoints ---

@app.get("/projects/{project_id}/tasks")
async def get_tasks(project_id: str):
    # Verificar si el proyecto existe
    proj = runner.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return runner.list_tasks(project_id)

@app.post("/projects/{project_id}/tasks")
async def create_task(project_id: str, task: TaskCreate, background_tasks: BackgroundTasks):
    proj = runner.get_project(project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")

    task_id = str(uuid.uuid4())
    runner.create_task(task_id, project_id, task.agent_name, task.description)
    
    background_tasks.add_task(
        run_agent_in_background,
        task_id,
        project_id,
        task.agent_name,
        task.model_id,
        task.description,
    )
    return {
        "ok": True,
        "task_id": task_id,
        "status": "queued",
    }

@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = runner.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/api/models/scan")
async def scan_models(force: bool = False):
    global _cached_models, _last_scan_time
    now = time.time()
    
    if not force and _cached_models and (now - _last_scan_time < SCAN_INTERVAL):
        return _cached_models

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://openrouter.ai/api/v1/models")
            data = response.json()
            
            raw_models = data.get("data", [])
            free_models = []
            
            # Arquitecturas que sabemos que suelen soportar Tool Calling
            tool_friendly_keywords = ["tool", "function", "agent", "instruct", "coder", "qwen2.5", "qwen3", "llama-3.3", "gemma-3"]

            for m in raw_models:
                pricing = m.get("pricing", {})
                if pricing.get("prompt") == "0" and pricing.get("completion") == "0":
                    m_id = m.get("id", "")
                    m_name = m.get("name", m_id)
                    m_desc = m.get("description", "").lower()
                    
                    # Heurística para detectar soporte de tools
                    supports_tools = any(kw in m_id.lower() or kw in m_desc for kw in tool_friendly_keywords)
                    
                    # Algunos fallan aunque digan instruct, pero es mejor que nada
                    # Evitamos los "tiny" o modelos demasiado viejos para agents complejos
                    if "tiny" in m_id.lower() or "base" in m_id.lower():
                        priority = 1
                    elif supports_tools:
                        priority = 3
                    else:
                        priority = 2
                        
                    free_models.append({
                        "id": m_id,
                        "name": m_name,
                        "context_length": m.get("context_length", 0),
                        "supports_tools": supports_tools,
                        "priority": priority,
                        "description": m.get("description", "")[:200] + "..."
                    })
            
            # Siempre añadir el router oficial
            free_models.append({
                "id": "openrouter/free",
                "name": "Router: Free Models (Auto)",
                "context_length": 128000,
                "supports_tools": True,
                "priority": 4,
                "description": "Selección automática de OpenRouter entre modelos gratuitos."
            })
            
            # Ordenar por prioridad (desc) y nombre
            free_models.sort(key=lambda x: (-x["priority"], x["id"]))
            
            _cached_models = free_models
            _last_scan_time = now
            return _cached_models
            
    except Exception as e:
        print(f"Error scanning models: {e}")
        return _cached_models if _cached_models else []
