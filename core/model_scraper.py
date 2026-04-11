"""
core/model_scraper.py
Web scraping de modelos gratuitos de OpenRouter.
Usa la API JSON oficial primero; si falla, parsea el HTML como backup.
"""
import os
import json
import time
import requests
from functools import lru_cache

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")

# Modelos incompatibles conocidos (no soportan function calling / system prompts)
BLACKLIST = {
    "google/gemma-3-4b-it:free",         # Error 404 tool use / sin system prompt
    "nvidia/nemotron-3-super-120b-a12b:free",  # Devuelve XML en vez de JSON
}

_cache_time = 0
_cache_data = []
CACHE_TTL = 300  # 5 minutos


def get_free_models(force_refresh: bool = False) -> list[dict]:
    """
    Obtiene la lista de modelos gratuitos de OpenRouter.
    Primero intenta la API REST; si falla, hace scraping HTML.
    Devuelve lista ordenada: Gemini primero, openrouter/free al final.
    """
    global _cache_time, _cache_data

    if not force_refresh and _cache_data and (time.time() - _cache_time) < CACHE_TTL:
        return _cache_data

    models = _fetch_from_api()
    if not models:
        models = _fetch_from_html()

    # Filtrar blacklist
    models = [m for m in models if m.get("id") not in BLACKLIST]

    # Ordenar: Gemini primero, luego resto, openrouter/free al final
    def sort_key(m):
        model_id = m.get("id", "")
        if "openrouter/free" in model_id:
            return 99
        if "gemini" in model_id:
            return 0
        if "gemma" in model_id:
            return 1
        if "llama" in model_id:
            return 2
        return 5

    models.sort(key=sort_key)

    _cache_data = models
    _cache_time = time.time()
    return models


def _fetch_from_api() -> list[dict]:
    """Usa la API REST de OpenRouter para obtener modelos gratis."""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://zaidsmart.local",
            "X-Title": "ZAIDSMART Agentes",
        }
        resp = requests.get(
            "https://openrouter.ai/api/v1/models",
            headers=headers,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()
        all_models = data.get("data", [])

        free_models = []
        for m in all_models:
            pricing = m.get("pricing", {})
            input_cost  = float(pricing.get("prompt",     0) or 0)
            output_cost = float(pricing.get("completion", 0) or 0)
            if input_cost == 0.0 and output_cost == 0.0:
                free_models.append({
                    "id":           m.get("id", ""),
                    "name":         m.get("name", m.get("id", "")),
                    "context":      m.get("context_length", 0),
                    "provider":     m.get("id", "").split("/")[0] if "/" in m.get("id","") else "?",
                    "description":  m.get("description", "")[:200],
                })
        return free_models
    except Exception:
        return []


def _fetch_from_html() -> list[dict]:
    """Backup: parsea la página web de OpenRouter con BeautifulSoup."""
    try:
        from bs4 import BeautifulSoup
        resp = requests.get(
            "https://openrouter.ai/models?q=free",
            headers={"User-Agent": "Mozilla/5.0 ZAIDSMART-Scraper/1.0"},
            timeout=15
        )
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        models = []
        # Busca los enlaces de modelos
        for link in soup.select("a[href^='/']"):
            href = link.get("href", "")
            # Los modelos tienen formato /proveedor/modelo
            parts = href.strip("/").split("/")
            if len(parts) == 2 and ":free" in parts[1]:
                model_id = f"{parts[0]}/{parts[1]}"
                models.append({
                    "id":       model_id,
                    "name":     link.get_text(strip=True) or model_id,
                    "context":  0,
                    "provider": parts[0],
                    "description": "",
                })

        # Deduplicar
        seen = set()
        unique = []
        for m in models:
            if m["id"] not in seen:
                seen.add(m["id"])
                unique.append(m)
        return unique
    except Exception:
        return []


# Lista hardcoded de emergencia si todo falla
FALLBACK_MODELS = [
    {"id": "google/gemini-2.0-flash-lite:free",     "name": "Gemini 2.0 Flash Lite",     "context": 1000000, "provider": "google"},
    {"id": "google/gemini-flash-1.5-8b:free",       "name": "Gemini Flash 1.5 8B",       "context": 1000000, "provider": "google"},
    {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B Instruct",     "context": 131072,  "provider": "meta-llama"},
    {"id": "nousresearch/hermes-3-llama-3.1-405b:free","name":"Hermes 3 Llama 3.1 405B", "context": 131072,  "provider": "nousresearch"},
    {"id": "openrouter/free",                        "name": "Free Models Router",         "context": 200000,  "provider": "openrouter"},
]

