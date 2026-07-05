# AdaL Customer Support Agent — v1 (web-search based)

A minimal support agent that answers AdaL questions by **web-searching the official docs** (`docs.sylph.ai`) and returning grounded answers with links.

This is the simplest possible version — no index, no webhook, no manifest. The agent uses the built-in `web_search` + `fetch_url` tools to search and read the live docs. Ship it, see if the answers are good, then decide if the grounded (index-based) version is needed.

## How it works

```
User asks an AdaL question
  ↓
Agent calls web_search("install AdaL docs.sylph.ai")
  ↓
Agent calls fetch_url on the matching docs page
  ↓
Agent answers, grounded in the real docs, with a link
```

## Guardrails

- **AdaL-only** — the system prompt rejects non-AdaL questions politely.
- **No invention** — the agent must search the docs before answering; it never guesses flags or commands.
- **Cite links** — every answer ends with the docs URL it used.

## Tools

Only **Web** (search + fetch) and **Read** (read_file, read_image) are enabled. Everything else is stripped:

```python
remove_tools = ["Bash", "Edit", "Search", "Image", "Video", "Consult"]
# → agent can ONLY web_search, fetch_url, read_file, read_image
```

The agent literally cannot edit files, run commands, or generate media — it can only search the web, fetch URLs (saved to temp storage), and read files back in sections.

**Fetch → read-in-sections pattern:** `fetch_url` saves a large doc page to temp storage; the agent then uses `read_file` with `start_line`/`end_line` to scan specific sections without re-fetching. Useful for long doc pages.

## Setup

```bash
# 1. Install the AdaL SDK
pip install adal-agent-sdk rich

# 2. Make sure AdaL CLI is installed and authed (run `adal` once)
adal --version

# 3. Run the agent
cd class-2/support-agent-v1
python support_agent.py            # interactive REPL
python support_agent.py --script   # run scripted test cases
```

All streaming SDK events are saved to `events.jsonl` (gitignored) for debugging and replay — every assistant delta, tool call, and lifecycle event is logged with a timestamp and turn label.

## Model

`google-gemini-3-flash-preview` — cheap and fast. Suitable for a v1 support widget. Swap for a stronger model in `support_agent.py` if grounding needs improvement.

## Test cases

Run `python support_agent.py --script` to validate against:

**Grounded (should search + answer with a link):**
1. How do I install AdaL?
2. What's the difference between `adal --mode engineer` and `adal`?
3. How do I remove the bash tool?
4. How do I authenticate the SDK in CI?
5. What models can I use?
6. How do I write a custom tool?

**Off-topic (should politely decline):**
7. Write me a Python web scraper.
8. What's the weather in Tokyo?
9. Explain how transformers work.

## Path to production

1. ✅ Local SDK test (this script)
2. ⬜ Create the same agent on AdaL Cloud (same prompt + `remove_tools`)
3. ⬜ Embed a chat widget on adalagent.ai (BFF proxy pattern)
4. ⬜ If answers aren't grounded enough → upgrade to the index-based design
   (see `docs/adal/fea_adal_customer_support_agent.md`)

## Why v1 is just web search

- **Simplest thing that works** — no infrastructure, no index, no webhook.
- The docs are already live and searchable at `docs.sylph.ai`; the agent just needs to find and read them.
- If v1 answers are accurate and fast enough, we may not need the index-based version at all.
- If they're not (hallucinations, missed pages, slow), the design doc has the grounded alternative ready to build.
