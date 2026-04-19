import re
from pathlib import Path
from typing import Union

from .models import Scenario


def parse_dataset(text: str) -> list[Scenario]:
    """Parse markdown dataset into list of Scenario objects.

    Expected format:
    ## gl_001 — description
    ### Response A
    text...
    ### Response B
    text...
    ---
    """
    scenarios = []
    # Split on h2 scenario headers: ## gl_NNN — description
    blocks = re.split(r"\n## (gl_\d+) — (.+)\n", text)
    # blocks[0] is pre-header content; then triplets of (id, description, body)
    i = 1
    while i + 2 < len(blocks):
        scenario_id = blocks[i].strip()
        description = blocks[i + 1].strip()
        body = blocks[i + 2]
        responses = _parse_responses(body)
        scenarios.append(
            Scenario(id=scenario_id, description=description, responses=responses)
        )
        i += 3
    return scenarios


def _parse_responses(body: str) -> dict[str, str]:
    """Parse response sections from scenario body.

    Expected format:
    ### Response A
    text...
    ### Response B
    text...
    ---
    """
    responses = {}
    parts = re.split(r"\n### Response ([A-E])\n", body)
    # parts[0] is pre-first-response content; then pairs of (letter, text)
    i = 1
    while i + 1 < len(parts):
        letter = parts[i].strip()
        text = parts[i + 1].strip()
        # Stop at the --- separator
        text = text.split("\n---")[0].strip()
        if text:
            responses[letter] = text
        i += 2
    return responses


def parse_file(path: Union[str, Path]) -> list[Scenario]:
    """Parse a markdown file into list of Scenario objects."""
    return parse_dataset(Path(path).read_text(encoding="utf-8"))
