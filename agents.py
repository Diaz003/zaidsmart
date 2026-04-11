import os
from dotenv import load_dotenv
from crewai import Agent

load_dotenv()

def get_base_llm_config():
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "openai_api_base": "https://openrouter.ai/api/v1",
        "temperature": 0.4,
    }

def resolve_model_id(model_id):
    """Resuelve alias como 'free' a modelos reales de OpenRouter."""
    # Solo interceptar si el ID es exactamente 'free' o 'openrouter/free' o está vacío
    generic_ids = ["free", "openrouter/free", "openrouter/", ""]
    clean_id = (model_id or "").strip().lower()
    
    if clean_id in generic_ids:
        # Selección de modelos gratuitos potentes que suelen estar online
        return "meta-llama/llama-3.3-70b-instruct:free" 
    
    return model_id

def create_agents(model_id="google/gemma-3-12b-it:free", step_callback=None):
    """
    Crea las instancias de los agentes dinámicamente usando el modelo elegido.
    Si se proporciona step_callback, se añade a todos los agentes para live-logs.
    """
    
    clean_id = resolve_model_id(model_id)
    # Asegurarnos de que el litellm use openrouter
    llm_string = clean_id if clean_id.startswith("openrouter/") else f"openrouter/{clean_id}"
    config = get_base_llm_config()

    agent_readme = Agent(
        name="Escritor Técnico",
        role="writer",
        goal="Crear y mantener READMEs y documentación clara de proyectos",
        backstory=(
            "Eres un redactor experto identificado como 'writer'. Tu objetivo es escribir archivos Markdown "
            "claros y estructurados. No delegas trabajo."
        ),
        llm=llm_string,
        llm_config=config,
        verbose=True,
        allow_delegation=False,
        step_callback=step_callback
    )

    agent_godot = Agent(
        name="Programador Godot",
        role="coder",
        goal="Escribir scripts de GDScript y organizar escenas eficientes en Godot Engine",
        backstory=(
            "Eres un desarrollador senior de Godot identificado como 'coder'. Conoces GDScript y la jerarquía de nodos. "
            "Tu código es limpio y optimizado."
        ),
        llm=llm_string,
        llm_config=config,
        verbose=True,
        allow_delegation=False,
        step_callback=step_callback
    )

    agent_assets = Agent(
        name="Especialista Multimedia",
        role="visuals",
        goal="Diseñar descripciones de assets, buscar recursos y organizar la parte visual",
        backstory=(
            "Eres un director de arte identificado como 'visuals'. Sabes qué assets (pixel art, sonidos, música) "
            "necesita un juego."
        ),
        llm=llm_string,
        llm_config=config,
        verbose=True,
        allow_delegation=False,
        step_callback=step_callback
    )

    # El manager delega a los demás, por lo que su rol es orquestar.
    agent_manager = Agent(
        name="Coordinador Maestro",
        role="manager",
        goal="Dividir objetivos complejos en tareas simples y supervisar a los especialistas",
        backstory=(
            "Eres el Coordinador Maestro (identificado como 'manager'). Tu equipo tiene 3 especialistas: "
            "1. 'writer' (para documentos y READMEs). "
            "2. 'coder' (para código y lógica de juego). "
            "3. 'visuals' (para assets y diseño visual). "
            "\nIMPORTANTE:\n"
            "- NUNCA te delegues trabajo a ti mismo (manager).\n"
            "- Usa EXÁCTAMENTE esos roles ('writer', 'coder', 'visuals') para delegar.\n"
            "- Cuando todos terminen, compila el resultado final."
        ),
        llm=llm_string,
        llm_config=config,
        verbose=True,
        allow_delegation=True,
        step_callback=step_callback
    )

    registry = {
        "readme": agent_readme,
        "godot": agent_godot,
        "assets": agent_assets,
    }
    
    return registry, agent_manager
