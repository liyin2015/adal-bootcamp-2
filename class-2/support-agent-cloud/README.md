# AdaL Support Agent — Cloud Widget Demo

A floating customer-support chat widget (Intercom/Zendesk style) that talks to
**AdaL Cloud**. The agent answers AdaL product questions using web search +
fetch against the official docs at docs.sylph.ai.

## Architecture

```
Browser (widget)  →  BFF Proxy (FastAPI)  →  AdaL Cloud API
                     holds JWT server-side
```

The proxy:
1. On startup, ensures the `AdaL Support Agent` exists (creates from `agent/agent_config.json` if absent).
2. Serves `site/index.html` (the floating chat widget).
3. Proxies `POST /api/session` and `POST /api/chat/{id}` to AdaL Cloud, injecting the Bearer JWT.

The browser never sees the token, the upstream URL, or the agent id.

## Quick Start (local)

```bash
# Provide JWT (never commit it)
export ADAL_JWT="eyJ..."
# OR: echo "eyJ..." > proxy/.adal_jwt

./run_local.sh
# → http://127.0.0.1:8500/
```

## Deploy to AWS App Runner

```bash
ADAL_JWT="eyJ..." ./deploy_aws.sh
```

## Environment Variables

| Var | Default | Description |
|-----|---------|-------------|
| `ADAL_JWT` | — (required) | Clerk session JWT |
| `ADAL_BASE_URL` | `https://cloud.adal.sylph.ai` | Upstream API |
| `ADAL_MODEL` | `google-gemini-3-flash-preview` | Model per session |
| `PORT` | `8500` | Proxy listen port |
| `HOST` | `127.0.0.1` | Proxy listen host |

## Files

```
├── README.md
├── agent/
│   └── agent_config.json     # /v1/agents POST body
├── proxy/
│   ├── server.py             # BFF (FastAPI)
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .gitignore
├── site/
│   └── index.html            # Floating chat widget
├── run_local.sh
└── deploy_aws.sh
```

## Agent Configuration

The agent is configured with:
- **`remove_tools`**: Strips Bash, Edit, Search, Image, Video, Consult — leaving only Web (web_search + fetch_url) and Read (read_file).
- **`system_prompt`**: Instructs the agent to search docs.sylph.ai for answers, cite sources, and refuse off-topic questions.
