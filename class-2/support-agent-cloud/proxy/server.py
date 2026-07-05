#!/usr/bin/env python3
"""Backend-for-frontend (BFF) proxy for the AdaL Support Agent demo.

Why this exists: the AdaL Cloud API requires a per-user Clerk JWT on every
request (Authorization: Bearer <token>). A public support widget must NEVER
embed that token in client HTML. This tiny server holds the token server-side
and does three things:

  1. On startup, ensures the AdaL Support Agent exists (creates it from
     agent/agent_config.json if absent) — no manual setup step.
  2. Serves the static site (site/).
  3. Proxies the two browser-facing calls to AdaL Cloud, injecting the Bearer
     token: POST /api/session (create session) and POST /api/chat (stream turn).

The browser only ever talks to THIS proxy — it never sees the token, the
upstream base URL, or even the agent id.

Config (env vars; never commit the token):
  ADAL_JWT       (required) the Clerk session JWT to run the demo under.
                 Read from the env or from proxy/.adal_jwt (gitignored).
  ADAL_BASE_URL  (default: the AdaL Cloud deployment) upstream API base.
  ADAL_MODEL     (default: google-gemini-3-flash-preview) per-session model.
  PORT / HOST    (default: 8500 / 127.0.0.1) where this proxy listens.

Run:
  ./run_local.sh            # or: uvicorn server:app --port 8500
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root (support-agent-cloud/.env)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("support-proxy")

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent  # support-agent-cloud/
_SITE_DIR = _ROOT / "site"

# Upstream AdaL Cloud API base.
BASE_URL = os.environ.get(
    "ADAL_BASE_URL",
    "https://cloud.adal.sylph.ai",
).rstrip("/")
MODEL = os.environ.get("ADAL_MODEL", "google-gemini-3-flash-preview")
HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8500"))
_VERIFY_TLS = "elb.amazonaws.com" not in BASE_URL


def _load_token() -> str:
    """Load the Clerk JWT from ADAL_JWT env or proxy/.adal_jwt (gitignored)."""
    token = os.environ.get("ADAL_JWT", "").strip()
    if not token:
        token_file = _HERE / ".adal_jwt"
        if token_file.exists():
            token = token_file.read_text(encoding="utf-8").strip()
    if not token:
        raise RuntimeError(
            "No ADAL_JWT provided. Set the ADAL_JWT env var or write the token to "
            f"{_HERE / '.adal_jwt'} (gitignored)."
        )
    return token


_TOKEN = _load_token()


def _auth_headers() -> dict[str, str]:
    return {"Content-Type": "application/json", "Authorization": f"Bearer {_TOKEN}"}


async def _ensure_agent() -> str:
    """Create the support agent if it doesn't already exist; return its id."""
    config_path = _ROOT / "agent" / "agent_config.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    name = config["name"]

    async with httpx.AsyncClient(timeout=30.0, verify=_VERIFY_TLS, follow_redirects=True) as client:
        resp = await client.get(f"{BASE_URL}/v1/agents", headers=_auth_headers())
        resp.raise_for_status()
        for agent in resp.json():
            if agent.get("name") == name:
                logger.info("Reusing existing agent %s (%s)", name, agent["id"])
                return agent["id"]
        resp = await client.post(
            f"{BASE_URL}/v1/agents", headers=_auth_headers(), json=config
        )
        resp.raise_for_status()
        agent_id = resp.json()["id"]
        logger.info("Created agent %s (%s)", name, agent_id)
        return agent_id


app = FastAPI(title="AdaL Support Agent BFF Proxy")

_AGENT_ID: str = ""


@app.on_event("startup")
async def _startup() -> None:
    global _AGENT_ID
    try:
        _AGENT_ID = await _ensure_agent()
        logger.info("Support proxy ready — upstream=%s model=%s agent=%s", BASE_URL, MODEL, _AGENT_ID)
    except Exception as exc:
        logger.warning("Agent setup deferred (will retry on first request): %s", exc)


async def _provision_in_background(session_id: str) -> None:
    """Fire-and-forget: provision the session worker after creation."""
    try:
        async with httpx.AsyncClient(
            timeout=180.0, verify=_VERIFY_TLS, follow_redirects=True
        ) as client:
            resp = await client.post(
                f"{BASE_URL}/v1/sessions/{session_id}/provision",
                headers=_auth_headers(),
            )
            if resp.status_code < 400:
                logger.info("provision[%s] worker ready", session_id)
            else:
                logger.warning("provision[%s] failed: %s %s", session_id, resp.status_code, resp.text[:200])
    except Exception as exc:
        logger.warning("provision[%s] error: %s", session_id, exc)


@app.post("/api/session")
async def create_session() -> dict:
    """Create a chat session and pre-warm its worker in the background."""
    global _AGENT_ID
    if not _AGENT_ID:
        _AGENT_ID = await _ensure_agent()
    async with httpx.AsyncClient(timeout=30.0, verify=_VERIFY_TLS, follow_redirects=True) as client:
        resp = await client.post(
            f"{BASE_URL}/v1/sessions",
            headers=_auth_headers(),
            json={"agent_config_id": _AGENT_ID, "title": "Support visitor", "model": MODEL},
        )
    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    session_id = resp.json()["id"]
    import asyncio
    asyncio.create_task(_provision_in_background(session_id))
    return {"session_id": session_id}


@app.post("/api/chat/{session_id}")
async def chat_stream(session_id: str, request: Request) -> StreamingResponse:
    """Proxy one streamed chat turn, forwarding the upstream SSE verbatim."""
    payload = await request.json()
    message = payload.get("message", "")

    async def event_source():
        async with httpx.AsyncClient(timeout=180.0, verify=_VERIFY_TLS, follow_redirects=True) as client:
            async with client.stream(
                "POST",
                f"{BASE_URL}/v1/sessions/{session_id}/chat/stream",
                headers=_auth_headers(),
                json={"message": message},
            ) as upstream:
                if upstream.status_code >= 400:
                    body = await upstream.aread()
                    yield f"event: error\ndata: {json.dumps({'status': upstream.status_code, 'error': body.decode('utf-8', 'replace')})}\n\n"
                    return
                async for chunk in upstream.aiter_raw():
                    if chunk:
                        yield chunk

    return StreamingResponse(event_source(), media_type="text/event-stream")


# Serve the static site at the root. Mounted last so /api/* wins.
app.mount("/", StaticFiles(directory=str(_SITE_DIR), html=True), name="site")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=HOST, port=PORT)
