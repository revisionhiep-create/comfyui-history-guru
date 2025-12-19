"""Helper utility functions."""
import hashlib
import json
from typing import Any, Dict, Optional


def generate_hash(text: str) -> str:
    """Generate SHA256 hash for text."""
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def safe_json_dumps(data: Any) -> str:
    """Safely serialize data to JSON."""
    try:
        return json.dumps(data, ensure_ascii=False)
    except (TypeError, ValueError):
        return json.dumps(str(data))


def safe_json_loads(text: str) -> Optional[Dict]:
    """Safely deserialize JSON text."""
    try:
        return json.loads(text)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None


def format_lora_string(loras: list) -> str:
    """Format LoRA list for display."""
    if not loras:
        return "None"
    
    return ", ".join([f"{lora['name']} ({lora['strength']:.2f})" for lora in loras])


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
