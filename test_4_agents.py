from agents import agent_manager
from crewai import Task

task = Task(
    description="""
    Para un proyecto Godot de plataformas 2D:
    1. Crea estructura de README
    2. Sugiere assets 2D necesarios
    3. Da un ejemplo de escena básica
    """,
    agent=agent_manager,
    expected_output="Plan completo para el proyecto Godot.",
)

print("🚀 Probando los 4 agentes...")
result = agent_manager.execute_task(task)
print("\n📋 Respuesta del Manager:")
print(result)
