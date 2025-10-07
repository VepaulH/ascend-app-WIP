
from datetime import datetime
from .settings import settings

# OpenAI client (optional)
_has_openai = False
client = None
try:
    if settings.OPENAI_API_KEY:
        from openai import OpenAI
        client = OpenAI(api_key=settings.OPENAI_API_KEY)
        _has_openai = True
except Exception:
    _has_openai = False

def _heuristic_parse(text: str) -> dict:
    lower = text.lower()
    mood = None
    for m in ["happy", "good", "okay", "neutral", "sad", "stressed", "anxious", "excited"]:
        if m in lower:
            mood = m
            break
    habit = None
    for h in ["meditation", "meditated", "gym", "workout", "walk", "journaling", "reading", "study", "yoga"]:
        if h in lower:
            habit = "meditation" if "meditat" in lower else h
            break
    import re
    duration = None
    m = re.search(r"(\d+)\s*(min|mins|minutes)", lower)
    if m:
        duration = int(m.group(1))
    return {
        "mood": mood,
        "habit": habit,
        "duration": duration,
        "notes": text,
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": 1,
    }

def _torch_parse(text: str) -> dict | None:
    if not settings.USE_PYTORCH:
        return None
    try:
        from .ai_pytorch import parse_text_with_torch
        return parse_text_with_torch(text)
    except Exception:
        return None

def parse_text_to_entry(text: str) -> dict:
    # Prefer PyTorch path if enabled
    torch_result = _torch_parse(text)
    if torch_result is not None:
        return torch_result

    if not _has_openai:
        return _heuristic_parse(text)

    prompt = (
        "Extract a wellness log from the following text. "
        "Return strict JSON with fields: mood (string|null), habit (string|null), "
        "duration (int minutes|null), notes (string|null), timestamp (ISO8601|null).\n"
        f"Text: '''{text}'''"
    )
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a parser that returns only JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        content = completion.choices[0].message.content
        import json
        data = json.loads(content)
        data.setdefault("notes", text)
        data.setdefault("timestamp", datetime.utcnow().isoformat())
        data.setdefault("mood", None)
        data.setdefault("habit", None)
        data.setdefault("duration", None)
        data.setdefault("user_id", 1)
        return data
    except Exception:
        return _heuristic_parse(text)
