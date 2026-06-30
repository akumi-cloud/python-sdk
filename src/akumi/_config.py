# AUTO-GENERATED runtime, copied by akumi/codegen. Do not edit by hand.
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClientConfig:
    """Immutable client configuration. The api_key is sent only on the
    Authorization header by the transport and is never logged or placed in a
    query string."""

    api_key: str
    base_url: str = "https://api.akumi.cloud"
    max_retries: int = 2
    retry_on: tuple[int, ...] = field(default_factory=lambda: (429, 500, 502, 503, 504))
