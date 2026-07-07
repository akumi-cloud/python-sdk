# Akumi Python SDK

The official Python client for [Akumi](https://akumi.cloud), the EU-sovereign,
OpenAI-compatible inference API. Built on httpx, with both a synchronous and an
asynchronous client. One `base_url` for every model, governed and metered, with
your regulated data kept in the EU.

- **Drop-in OpenAI-compatible.** Chat completions, embeddings, and models under one key.
- **EU-sovereign by default.** The egress guard fails closed on non-EU routing.
- **Governed, not just hosted.** PII firewall, per-request residency, and a metadata-only audit trail on every call.
- **Sync and async.** Streaming and automatic retries in both clients.

## Requirements

Python 3.9 or newer.

## Install

```bash
pip install akumi
```

## Quickstart

Create an API key under app.akumi.cloud -> Platform -> API keys:

```python
from akumi import Akumi

client = Akumi.from_api_key("mk_...")

result = client.chat.create(params={
    "model": "mistral/mistral-large-latest",
    "messages": [
        {"role": "user", "content": "Explain EU data residency in one sentence."},
    ],
})

print(result["choices"][0]["message"]["content"])
```

## Streaming

```python
for chunk in client.chat.create_streamed(params={
    "model": "mistral/mistral-large-latest",
    "messages": [{"role": "user", "content": "Write a haiku about Frankfurt."}],
}):
    print(chunk["choices"][0]["delta"].get("content", ""), end="")
```

## Async

```python
import asyncio
from akumi import AsyncAkumi

async def main():
    client = AsyncAkumi.from_api_key("mk_...")
    result = await client.chat.create(params={
        "model": "mistral/mistral-large-latest",
        "messages": [{"role": "user", "content": "Hello from the EU."}],
    })
    print(result["choices"][0]["message"]["content"])

asyncio.run(main())
```

## Embeddings

```python
embeddings = client.embeddings.create(params={
    "model": "mistral/mistral-embed",
    "input": "The quarterly report is ready for review.",
})

vector = embeddings["data"][0]["embedding"]
```

## More resources

- `client.models.list()` lists the models available to your key.
- `client.memory.forget(...)` and `client.memoryThreads.list()` manage long-term memory and threads.
- `client.auditLogs.list()` reads your metadata-only audit trail.

## Configuration

`from_api_key()` connects to `https://api.akumi.cloud/v1` and retries transient
failures (429, 502, 503, 504). Pass `base_url=` to target another host.

## Documentation

- Guides: https://akumi.cloud/docs
- API reference: https://akumi.cloud/docs/api-reference

## About

Generated from the Akumi OpenAPI specification, so it tracks the API
automatically. Issues: https://github.com/akumi-cloud/python-sdk.

MIT licensed.
