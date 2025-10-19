import json
from pathlib import Path

def parse_foundry_response_dict(data: dict) -> str:
    """Reuse the same parsing heuristics from the main script to return text."""
    texts = []
    if isinstance(data, dict):
        choices = data.get("choices") or []
        for c in choices:
            msg = c.get("message") or {}
            content = msg.get("content") or c.get("text") or c.get("delta")
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict):
                        if "text" in block and isinstance(block["text"], str):
                            texts.append(block["text"])
                        elif "content" in block and isinstance(block["content"], str):
                            texts.append(block["content"])
            elif isinstance(content, str):
                texts.append(content)
    if not texts:
        try:
            first = data.get("choices", [None])[0]
            if first:
                msg = first.get("message") or first.get("delta") or first.get("text")
                if isinstance(msg, str):
                    texts.append(msg)
                elif isinstance(msg, dict) and isinstance(msg.get("content"), str):
                    texts.append(msg.get("content"))
        except Exception:
            pass
    return "\n".join(t.strip() for t in texts if t).strip()


def parse_foundry_response_file(path: str) -> str:
    p = Path(path)
    with p.open('r', encoding='utf-8') as f:
        data = json.load(f)
    return parse_foundry_response_dict(data)
