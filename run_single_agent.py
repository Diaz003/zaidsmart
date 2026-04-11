from agents import agent_general
from crewai import Task

# Tarea como objeto Task correcto
task = Task(
    description="""
    Explica en 3 puntos qué es un agente de IA y para qué sirve.
    Responde en español.
    """,
    agent=agent_general,
    expected_output="3 puntos explicando qué es un agente de IA.",
)

print("🤖 Probando primer agente...")
result = agent_general.execute_task(task)  # ← AGENTE ejecuta la TAREA
print("\n📄 Respuesta del agente:")
print(result)
