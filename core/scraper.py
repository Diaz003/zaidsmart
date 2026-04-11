import os
import re
from typing import List

import requests
from bs4 import BeautifulSoup

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/models"
OPENROUTER_FREE_PAGE = "https://openrouter.ai/models?q=free"
REQUEST_TIMEOUT = 10

EXCLUDED_MODELS = {
    "google/gemma-3-4b-it:free",
}

EXCLUDED_PREFIXES = (
    "nvidia/nemotron-3-super-",
)


def get_free_models() -> List[str]:
    """
    Return free OpenRouter model ids sorted for CrewAI.
    """
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY", "")
    headers = {
        "User-Agent": "ZAIDSMART/0.2.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        response = requests.get(OPENROUTER_API_URL, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()
        models = data.get("data", [])

        free_models = []
        for model in models:
            model_id = model.get("id", "")
            pricing = model.get("pricing", {})
            prompt_price = _safe_float(pricing.get("prompt", "1"))
            completion_price = _safe_float(pricing.get("completion", "1"))

            if prompt_price == 0 and completion_price == 0 and not _is_excluded(model_id):
                free_models.append(model_id)

        return _sort_by_priority(free_models)
    except Exception:
        try:
            scraped_models = _scrape_free_models(headers)
            if scraped_models:
                return _sort_by_priority(scraped_models)
        except Exception:
            pass

    return _fallback_list()


def _scrape_free_models(headers: dict) -> List[str]:
    response = requests.get(OPENROUTER_FREE_PAGE, headers=headers, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    candidate_links = []
    for link in soup.select('a[href^="/"]'):
        href = (link.get("href") or "").strip()
        if not href or href == "/" or href.startswith("/docs") or href.startswith("/api"):
            continue
        if href.count("/") != 2:
            continue
        candidate_links.append(href)

    models = []
    seen = set()

    for href in candidate_links:
        model_page = f"https://openrouter.ai{href}"
        try:
            model_response = requests.get(model_page, headers=headers, timeout=REQUEST_TIMEOUT)
            model_response.raise_for_status()
        except Exception:
            continue

        page_text = model_response.text
        if "$0/M" not in page_text and "$0.00/M" not in page_text:
            continue

        page_soup = BeautifulSoup(page_text, "html.parser")
        font_mono = page_soup.select_one("h3.font-mono")
        model_id = ""
        if font_mono:
            model_id = font_mono.get_text(strip=True)
        if not model_id:
            match = re.search(r"([a-z0-9_.-]+/[a-z0-9_.:-]+)", page_text, re.IGNORECASE)
            model_id = match.group(1) if match else ""

        if model_id and model_id not in seen and not _is_excluded(model_id):
            seen.add(model_id)
            models.append(model_id)

    return models


def _sort_by_priority(models: List[str]) -> List[str]:
    unique_models = []
    seen = set()
    for model in models:
        if not model or model in seen or _is_excluded(model):
            continue
        seen.add(model)
        unique_models.append(model)

    gemini = [model for model in unique_models if model.startswith("google/gemini-")]
    high = [
        model
        for model in unique_models
        if (
            model.startswith("meta-llama/")
            or model.startswith("nousresearch/")
        )
        and model not in gemini
        and model != "openrouter/free"
    ]
    rest = [
        model
        for model in unique_models
        if model not in gemini and model not in high and model != "openrouter/free"
    ]
    ordered = gemini + high + rest
    if "openrouter/free" in unique_models or "openrouter/free" not in ordered:
        ordered = [model for model in ordered if model != "openrouter/free"]
        ordered.append("openrouter/free")
    return ordered


def _fallback_list() -> List[str]:
    return _sort_by_priority(
        [
            "google/gemini-2.0-flash-lite:free",
            "google/gemini-flash-1.5-8b:free",
            "meta-llama/llama-3.1-8b-instruct:free",
            "nousresearch/hermes-3-llama-3.1-405b:free",
            "openrouter/free",
        ]
    )


def _is_excluded(model_id: str) -> bool:
    if not model_id:
        return True
    if model_id in EXCLUDED_MODELS:
        return True
    return any(model_id.startswith(prefix) for prefix in EXCLUDED_PREFIXES)


def _safe_float(value) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 1.0
