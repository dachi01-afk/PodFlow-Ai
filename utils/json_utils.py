import json
import re
from typing import Any


def strip_thinking_tags(text: str) -> str:
    """Remove <think>...</think> blocks from LLM output."""
    return re.sub(r'<think>[\s\S]*?</think>', '', text).strip()


def strip_markdown_code_blocks(text: str) -> str:
    """Remove markdown code block wrappers (```json ... ``` or ``` ... ```)."""
    return re.sub(r'```(?:json)?\s*\n?([\s\S]*?)\n?\s*```', r'\1', text).strip()


def extract_json_object(text: str) -> str:
    """Extract the first complete JSON object from text using brace counting."""
    start = text.find('{')
    if start == -1:
        raise ValueError("No JSON object found in output")

    depth = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        c = text[i]
        if escape:
            escape = False
            continue
        if c == '\\' and in_string:
            escape = True
            continue
        if c == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return text[start:i + 1]

    raise ValueError("No complete JSON object found (unmatched braces)")


def validate_json_output(text: str) -> dict[str, Any]:
    """Extract and validate JSON from LLM output, handling thinking tags and markdown."""
    if not text:
        raise ValueError("Empty response from LLM")

    cleaned = strip_thinking_tags(text)
    cleaned = strip_markdown_code_blocks(cleaned)

    json_str = extract_json_object(cleaned)

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")
