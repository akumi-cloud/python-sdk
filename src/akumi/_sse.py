# AUTO-GENERATED runtime, copied by akumi/codegen. Do not edit by hand.
from __future__ import annotations

import json
from typing import Any

DONE_SENTINEL = "[DONE]"


def parse_sse_line(line: str) -> dict[str, Any] | None:
    """Decode a single SSE line. Returns the parsed event object, or None when
    the line is not a data line, is blank, or is the [DONE] sentinel."""
    if not line.startswith("data:"):
        return None

    data = line[len("data:"):].strip()
    if data == "" or data == DONE_SENTINEL:
        return None

    decoded = json.loads(data)
    return decoded if isinstance(decoded, dict) else None
