# AUTO-GENERATED runtime, copied by akumi/codegen. Do not edit by hand.
from __future__ import annotations

import asyncio
import json
import time
from collections.abc import AsyncGenerator, Generator
from typing import Any

import httpx

from ._config import ClientConfig
from ._errors import map_error
from ._sse import parse_sse_line


def _build_url(base_url: str, path: str, query: dict[str, Any] | None) -> str:
    url = base_url.rstrip("/") + path
    if query:
        pairs = {key: value for key, value in query.items() if value is not None}
        if pairs:
            url = url + "?" + str(httpx.QueryParams(pairs))
    return url


def _decode(text: str) -> dict[str, Any]:
    if text == "":
        return {}
    decoded = json.loads(text)
    return decoded if isinstance(decoded, dict) else {}


def _error_body(text: str) -> dict[str, Any]:
    if text == "":
        return {}
    try:
        decoded = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return decoded if isinstance(decoded, dict) else {}


class SyncTransport:
    """Synchronous HTTP transport: bearer auth, JSON, retries with backoff,
    status-to-exception mapping, and incremental SSE reads. The api_key is sent
    only on the Authorization header and is never logged."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client = httpx.Client()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "SyncTransport":
        return self

    def __exit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        self.close()

    def request(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None,
        body: dict[str, Any] | None,
    ) -> dict[str, Any]:
        response = self._dispatch(method, path, query, body)
        return _decode(response.text)

    def stream(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
    ) -> Generator[dict[str, Any], None, None]:
        url = _build_url(self._config.base_url, path, None)
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "text/event-stream",
        }
        content = json.dumps(body) if body is not None else None
        if content is not None:
            headers["Content-Type"] = "application/json"
        with self._client.stream(method, url, headers=headers, content=content) as response:
            if response.status_code >= 400:
                response.read()
                raise map_error(response.status_code, _error_body(response.text))
            for line in response.iter_lines():
                event = parse_sse_line(line)
                if event is not None:
                    yield event

    def _dispatch(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None,
        body: dict[str, Any] | None,
    ) -> httpx.Response:
        url = _build_url(self._config.base_url, path, query)
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "application/json",
        }
        content = json.dumps(body) if body is not None else None
        if content is not None:
            headers["Content-Type"] = "application/json"

        attempt = 0
        while True:
            response = self._client.request(method, url, headers=headers, content=content)
            if response.status_code < 400:
                return response

            should_retry = attempt < self._config.max_retries and response.status_code in self._config.retry_on
            if should_retry:
                attempt += 1
                time.sleep(0.25 * (2 ** (attempt - 1)))
                continue

            raise map_error(response.status_code, _error_body(response.text))


class AsyncTransport:
    """Asynchronous HTTP transport. Same behavior as SyncTransport over
    httpx.AsyncClient. The api_key is sent only on the Authorization header."""

    def __init__(self, config: ClientConfig) -> None:
        self._config = config
        self._client = httpx.AsyncClient()

    async def aclose(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncTransport":
        return self

    async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object) -> None:
        await self.aclose()

    async def arequest(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None,
        body: dict[str, Any] | None,
    ) -> dict[str, Any]:
        response = await self._adispatch(method, path, query, body)
        return _decode(response.text)

    async def astream(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        url = _build_url(self._config.base_url, path, None)
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "text/event-stream",
        }
        content = json.dumps(body) if body is not None else None
        if content is not None:
            headers["Content-Type"] = "application/json"
        async with self._client.stream(method, url, headers=headers, content=content) as response:
            if response.status_code >= 400:
                await response.aread()
                raise map_error(response.status_code, _error_body(response.text))
            async for line in response.aiter_lines():
                event = parse_sse_line(line)
                if event is not None:
                    yield event

    async def _adispatch(
        self,
        method: str,
        path: str,
        query: dict[str, Any] | None,
        body: dict[str, Any] | None,
    ) -> httpx.Response:
        url = _build_url(self._config.base_url, path, query)
        headers = {
            "Authorization": f"Bearer {self._config.api_key}",
            "Accept": "application/json",
        }
        content = json.dumps(body) if body is not None else None
        if content is not None:
            headers["Content-Type"] = "application/json"

        attempt = 0
        while True:
            response = await self._client.request(method, url, headers=headers, content=content)
            if response.status_code < 400:
                return response

            should_retry = attempt < self._config.max_retries and response.status_code in self._config.retry_on
            if should_retry:
                attempt += 1
                await asyncio.sleep(0.25 * (2 ** (attempt - 1)))
                continue

            raise map_error(response.status_code, _error_body(response.text))
