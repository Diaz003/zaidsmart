import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Falta OPENROUTER_API_KEY en .env")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

resp = client.chat.completions.create(
    model="openrouter/auto",
    messages=[
        {"role": "user", "content": "Respóndeme en una frase corta: ¿estás funcionando?"}
    ],
)

print(resp.choices[0].message.content)
