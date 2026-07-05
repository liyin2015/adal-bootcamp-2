# FEAT: AdaL Customer Support Agent

**Status:** Design (not started) · **Owner:** Li Yin · **Date:** 2026-07-04

## Problem

Users landing on `adalagent.ai` have no way to get instant, accurate answers about AdaL — installation, CLI flags, SDK usage, model selection, troubleshooting. The docs exist at `docs.sylph.ai` (served from a Docusaurus build of `adal-official-docs/`), but there is no agent that can answer grounded questions from them. We want a lightweight, cheap, always-in-sync support agent embedded on the landing page.

## Goals

### Stage 1 (this design) — Docs-grounded support agent
- Answer AdaL questions **grounded in the live docs** — never hallucinate flags, commands, or features.
- **AdaL-only guardrails** — reject non-AdaL questions politely.
- **Version-aware** — the agent knows the current version and recent changelog; when a user describes something that doesn't match current docs, it checks the changelog and asks for the user's version rather than guessing.
- **Cheap at scale** — prompt-cache the stable parts (manifest + changelog + guardrails); only dynamic per-question work bills at full rate.
- **Always in sync** — when docs merge to `main`, the agent's knowledge updates within seconds (webhook-triggered rebuild), not minutes.
- **Tested locally first** via the AdaL SDK; deploy to AdaL Cloud + embed a chat widget on the landing page once it works.

### Stage 2 (extended goal) — Landing-page content index
- Extend the agent's knowledge to include the **landing page content** (`adalagent.ai` / the ai-girl-glow marketing site), not just the docs.
- Lets the agent answer pricing, "what is AdaL", feature positioning, and comparison questions using the same grounded approach.
- Same architecture — the landing-page content becomes an additional source in the manifest + index.

## Non-goals

- Not a general-purpose chatbot. Non-AdaL questions are rejected.
- Not a bug-filer or ticketing system (Stage 1). Feedback capture is a possible later addition.
- Not a replacement for `docs.sylph.ai` search UI — this is a conversational layer on top.

## Architecture

### Three-tier knowledge design (the core insight)

The agent's knowledge is split into three tiers by cost and stability:

| Tier | What | Where | Stability | Cost |
|------|------|-------|-----------|------|
| **1. Manifest** | Compact dict of all docs: `{path, title, one-line description, section count}` + current version + recent changelog | System prompt | Stable (changes only on docs deploy) | Prompt-cached (~free at scale) |
| **2. BM25 search** | Ranked search: "which doc sections match this question?" | `search_docs` tool (in-memory) | Rebuilt on docs deploy | Tiny — in-memory, <1ms |
| **3. Read section** | Full markdown of one doc section | `read_doc_section` tool (fetches raw md) | Live | On-demand, per question only |

**Why the combination beats any single approach:**
- BM25 alone → the agent doesn't know the full landscape; it's blind to docs that exist but didn't match keywords.
- Manifest alone → no ranking; the agent must guess or read everything.
- Both → the manifest gives the *map* (always knows what exists), BM25 finds the *relevant spot* fast, read fetches *exact content* only when needed. The agent never guesses, never over-fetches.

### Prompt caching (the scale lever)

```
[System prompt: persona + guardrails + manifest + changelog + current version]
                                                    ↑
                                          STABLE → prompt-cached (~10% cost)
                                                    ↓
[User message + tool results + answer]   ← DYNAMIC, small, full price
```

The system prompt (including manifest + changelog) rarely changes — only when docs deploy. So it's a cache hit for ~every user. With thousands of users, the stable knowledge costs ~nothing per user. Only the dynamic parts (the user's question + search results + answer) bill at full rate.

### Sync: webhook-triggered rebuild (live towards change)

AdaL is a fast-moving dev tool — stale docs = wrong answers. So the index rebuilds **on every docs merge**, not on a schedule:

```
docs merge to main (adal-official-docs)
  ↓
GitHub webhook (push event) ──▶ build endpoint
  ↓
git pull docs → build manifest + BM25 index + parse CHANGELOG.md + extract version tags
  ↓
publish index artifact (manifest.json + docs index + changelog) to a static location
  ↓
agent instances fetch the new artifact → knowledge is live
```

**Why a webhook (not CI-on-push or per-session rebuild):**
- A 1-2 minute CI delay is too long for a dev tool that ships multiple times per week. "Live towards change" is the right product bar.
- Per-session rebuild doesn't scale (repeated work, GitHub API calls per user).
- The webhook triggers one build that serves all users — the artifact is static and shared.

**Security:** the webhook endpoint must verify GitHub's HMAC signature, or anyone can trigger rebuilds. The build endpoint is the only piece of custom infrastructure.

### Version-awareness (the differentiator)

The agent knows the current version and recent changelog (in the cached prompt). When a user describes a feature/flag/behavior that **doesn't match current docs**, the agent's reflex:

```
User mentions something not in current docs
  ↓
Check cached changelog (free — already in prompt)
  ↓
Found it? → "That was renamed/removed in vX.Y. What version are you on? Run `adal --version`."
Not found? → search_docs for alternate names → if still nothing, ask version + suggest upgrade
```

**The agent never guesses a version.** It confirms with the user when version matters. This is what makes a dev-tool support agent trustworthy — it knows what's current, what changed, and asks for your version instead of inventing.

## Tools (exactly 2, all built-ins stripped)

The agent gets only two custom tools. Every built-in tool group is removed so the agent literally cannot do anything except search and read AdaL docs.

| Tool | Returns | When used |
|------|---------|-----------|
| `search_docs(query)` | Top 5 ranked sections: `{title, path, snippet}` (BM25 over in-memory index) | When the question needs grounding beyond the manifest |
| `read_doc_section(path)` | Full markdown of one doc section | When the snippet isn't enough and the agent needs exact syntax/code |

```python
options = AdalAgentOptions(
    workspace=".",
    prompt_file="prompts/support_agent.md",
    permission_mode="yolo",          # tools are read-only — safe to auto-approve
    model="google-gemini-3-flash-preview",  # cheap for v1
    remove_tools=["Bash", "Edit", "Read", "Search", "Web", "Image", "Video", "Consult"],
    # → agent has ONLY search_docs + read_doc_section
)
```

## System Prompt (`prompts/support_agent.md`)

```
You are the AdaL support agent on adalagent.ai. Your ONLY job is to help
users learn and use AdaL — installation, CLI, SDK, Cloud Agents, custom
tools, custom prompts, models, and troubleshooting.

GUARDRAILS (enforce strictly):
- If a question is NOT about AdaL, politely decline: "I can only help with
  AdaL. For other topics, please reach out elsewhere." Do not answer, even
  if you know it.
- Never invent AdaL features, flags, or commands. If unsure, use the docs
  tools. If still unsure, say so and link to docs.sylph.ai.
- Keep answers short and copy-pasteable. This is support, not a tutorial.

BEHAVIOR:
- You have a manifest of all AdaL docs in your prompt. Use it to know what
  exists before searching.
- For any factual AdaL question, call search_docs first. Ground every answer.
- Call read_doc_section only when you need exact syntax or code from a section.

VERSION AWARENESS:
- You know the current AdaL version and recent changelog (in your prompt).
- If a user describes a feature, flag, or behavior that doesn't match current
  docs, FIRST check the changelog you already have — it may have been renamed
  or removed recently.
- If the changelog explains it, tell them what changed and in which version.
  Then ask: "What version are you on? Run `adal --version`."
- If you can't find it, search the docs. If still nothing, say you can't find
  it and suggest upgrading — give the install command.
- NEVER guess a version. ALWAYS confirm with the user if version matters.
```

## Directory structure (Stage 1)

```
class-2/support-agent/
├── README.md                       # how to run + test
├── requirements.txt                # adal-agent-sdk, httpx, rank-bm25, rich
├── prompts/
│   └── support_agent.md            # system prompt (persona + guardrails + version rules)
├── .adal/
│   └── tools.py                    # search_docs (BM25) + read_doc_section only
├── build/
│   ├── build_index.py              # git pull docs → manifest + BM25 index + changelog → publish artifact
│   └── webhook_endpoint.py         # receives GitHub webhook → runs build_index.py (HMAC-verified)
├── test_agent.py                   # local REPL + scripted tests (uses AdaL SDK)
└── test_cases.md                   # validation cases incl. off-topic rejections + version mismatches
```

## Test cases

### Grounded answers (should use docs)
1. "How do I install AdaL?"
2. "What's the difference between engineer mode and a worker agent?"
3. "How do I remove the bash tool so the agent can't run shell commands?"
4. "I get a truecolor error in macOS Terminal — how do I fix it?"
5. "How do I authenticate the SDK in CI without browser login?"
6. "What models can I use with AdaL?"
7. "How do I write a custom tool?"

### Off-topic (must reject)
8. "Write me a Python script to scrape a website."
9. "What's the weather in Tokyo?"
10. "Explain how transformers work."

### Version-awareness (should check changelog + ask version)
11. "How do I use `--enabled-default-tools`?" → agent recognizes this was renamed to `--remove-tools` (if in changelog), tells the user, asks version.
12. "The agent keeps asking for approval." → agent explains `--yolo` / `--allowed-tools`, mentions `--remove-tools` if recent, asks version.

## Stage 2 — Landing-page content index (extended goal)

Once Stage 1 is working and deployed, extend the agent's knowledge to include the **landing page content** at `adalagent.ai` (the ai-girl-glow marketing site).

### What this adds
- The agent can answer: "What is AdaL?", "How much does it cost?", "How does AdaL compare to Claude Code?", "What can AdaL build?" — using grounded landing-page content, not just docs.
- Same three-tier architecture: the landing page becomes an additional source in the manifest + index.

### How
- The landing page content (hero copy, pricing, feature sections, comparisons) is ingested into the same index as an additional source type: `{source: "landing", path, title, snippet}`.
- The manifest grows to include landing-page sections alongside docs sections, tagged by source so the agent knows whether it's citing docs or marketing.
- The webhook/build pipeline extends to also ingest landing-page content (from the ai-girl-glow repo or a scraped snapshot).

### Why deferred
- Stage 1 (docs) is the higher-value, higher-risk surface — getting grounded, version-aware docs answers right is the core trust-builder.
- Landing-page content changes less frequently and is less likely to cause "wrong answer" harm, so it's lower urgency.
- The architecture is designed to extend cleanly — adding a source type doesn't change the tools or the prompt structure.

## Build pipeline (Stage 1, detailed)

### `build/build_index.py`
1. `git pull` the `adal-official-docs/docs/` (private repo, read-only token in env).
2. Walk all `.md` files → for each: extract title, first heading, first paragraph → build manifest entry.
3. Build a BM25 index over all sections (using `rank-bm25`).
4. Parse `CHANGELOG.md` → extract recent N versions + their change entries.
5. Extract latest version (from CHANGELOG or git tags).
6. Serialize: `manifest.json` + `bm25_index.pkl` + `changelog.json` → publish to a static location (S3 / CloudFront / committed to repo).
7. Agent instances fetch these artifacts on startup; the webhook signals a fresh build.

### `build/webhook_endpoint.py`
- A minimal FastAPI endpoint that:
  1. Verifies the GitHub webhook signature (HMAC SHA-256 with the webhook secret).
  2. On verified `push` to `main` (docs path), runs `build_index.py`.
  3. Returns 200 immediately; build runs async.
- Deployed alongside the agent (or as a small serverless function).

## Deployment path

1. **Local SDK test** (Stage 1a) — `test_agent.py` runs the agent via the SDK with cached CLI auth. Validate against `test_cases.md`.
2. **Cloud agent** (Stage 1b) — create the agent on AdaL Cloud (same prompt + tools + `remove_tools`). The custom tools' index-fetch + BM25 runs inside the cloud agent's runtime.
3. **Webhook build pipeline** (Stage 1c) — deploy `build_index.py` + webhook endpoint. Wire the GitHub webhook.
4. **Landing-page widget** (Stage 1d) — embed a chat widget on `adalagent.ai` (same BFF proxy pattern as the customer sales agent) that streams chat from the AdaL Cloud agent.
5. **Stage 2** — extend the index to include landing-page content.

## Open questions

1. **Docs repo access:** Is `SylphAI-Inc/adal` private? The build pipeline needs a read-only token. (Confirm.)
2. **Static artifact location:** S3 + CloudFront, or commit the artifact to a repo and serve via GitHub raw / jsDelivr? (Recommend S3 for private-docs confidentiality; the index artifact itself isn't sensitive but S3 is cleaner.)
3. **Webhook host:** Does AdaL Cloud give us an HTTP surface to receive the webhook, or do we run a tiny separate function (e.g., AWS Lambda) for the build trigger? (Confirm infra availability.)
4. **Model for v1:** `google-gemini-3-flash-preview` (cheap) — confirm, or prefer a stronger model for better grounding?
5. **Stage 2 source:** Ingest landing-page content from the ai-girl-glow repo directly, or from a scraped snapshot of the live `adalagent.ai`? (Repo is cleaner; scraping handles dynamic content.)

## Risks

- **BM25 miss** — keyword search won't catch semantic matches (e.g., "stop agent from running shell" → `--remove-tools`). Mitigation: the manifest gives the agent the full landscape so it can read sections even when BM25 misses; upgrade to semantic search later if needed.
- **Webhook downtime** — if the build endpoint is down, the index goes stale. Mitigation: also run the build on a schedule (every hour) as a fallback, so staleness is bounded even if the webhook fails.
- **Changelog parsing** — `CHANGELOG.md` format may vary. Mitigation: the parser is tolerant; if it can't extract a version, the agent still works (just less version-aware).
- **Prompt-cache invalidation** — when docs deploy, the manifest changes, so the cache key changes and the next user pays the full system-prompt cost once. Acceptable — it happens on docs deploy, not per user.
