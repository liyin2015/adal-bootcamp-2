"""AdaL Customer Support Agent — v1 (web-search based).

A minimal support agent that answers AdaL questions by **web-searching the
official docs** (docs.sylph.ai) and returning grounded answers with links.

Design:
  - Tools allowed: Web (web_search, fetch_url) + Read (read_file, read_image).
    fetch_url can write fetched content to temp storage; the agent then uses
    read_file to read it back in sections (useful for large doc pages).
  - Everything else stripped: Bash, Edit, Search, Image, Video, Consult.
    The agent cannot edit files, run commands, or generate media.
  - Cheap model (Gemini Flash).
  - All streaming SDK events are saved to events.jsonl for debugging/replay.

Run:
    cd class-2/support-agent-v1
    python support_agent.py            # interactive REPL
    python support_agent.py --script   # run scripted test cases

Prereqs:
    - AdaL CLI installed and authed (run `adal` once to cache credentials)
    - pip install adal-agent-sdk rich
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

from adal_agent_sdk import AdalAgentOptions, query

# Positive set: ONLY Web (web_search, fetch_url) + Read (read_file, read_image)
# are visible to the agent. Everything else is stripped — no Bash, Edit, Search,
# Image, Video, Consult. The agent can only search the web, fetch URLs (saved to
# temp storage), and read files back in sections.
ENABLED_DEFAULT_TOOLS = ["Web", "Read"]
MODEL = "google-gemini-3-flash-preview"  # cheap for v1
_PROMPT_FILE = Path(__file__).parent / "prompts" / "support_agent.md"
PROMPT_FILE = str(_PROMPT_FILE.resolve())  # SDK runtime needs an absolute path
EVENTS_LOG = Path("events.jsonl")  # append-only log of every SDK event


# Scripted test cases for --script mode.
TEST_CASES = [
    # --- grounded (should search docs + answer with a link) ---
    "How do I install AdaL?",
    "What's the difference between `adal --mode engineer` and just `adal`?",
    "How do I remove the bash tool so the agent can't run shell commands?",
    "How do I authenticate the AdaL SDK in CI without a browser login?",
    "What models can I use with AdaL?",
    "How do I write a custom tool?",
    # --- off-topic (should politely decline) ---
    "Write me a Python script to scrape a website.",
    "What's the weather in Tokyo?",
    "Explain how transformers work.",
]


def make_options() -> AdalAgentOptions:
    return AdalAgentOptions(
        workspace=".",
        prompt_file=PROMPT_FILE,
        permission_mode="yolo",        # auto-approve — Web + Read are read-only
        model=MODEL,
        enabled_default_tools=ENABLED_DEFAULT_TOOLS,  # agent can ONLY web_search, fetch_url, read_file, read_image
    )


def log_event(event: dict, label: str) -> None:
    """Append every SDK event to events.jsonl with a turn label + timestamp."""
    record = {
        "ts": time.time(),
        "turn": label,
        "event": event,
    }
    with EVENTS_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


async def ask(prompt: str, opts: AdalAgentOptions, label: str = "user") -> str:
    """Send one question, collect streamed assistant text, log every event.

    All SDK events (assistant deltas, tool starts/completions, command lifecycle)
    are appended to events.jsonl so the full turn can be inspected or replayed.
    """
    chunks: list[str] = []
    async for event in query(prompt=prompt, options=opts):
        log_event(event, label)
        etype = event.get("type")
        if etype == "assistant.delta":
            chunks.append(event.get("text", ""))
        elif etype == "tool.started":
            name = event.get("tool_name", "tool")
            tool_input = event.get("tool_input", {})
            # Show a short preview of what the agent is doing
            preview = ""
            if name == "web_search":
                preview = tool_input.get("query", "")
            elif name == "fetch_url":
                preview = tool_input.get("url", "")
            elif name == "read_file":
                preview = tool_input.get("file_path", "")
            print(f"\n  🔍 {name}({preview}) ...", file=sys.stderr)
        elif etype == "tool.completed":
            print(f"  ✓ done\n", file=sys.stderr)
        elif etype == "command.failed":
            err = event.get("error", "unknown error")
            print(f"\n  ✗ failed: {err}", file=sys.stderr)
            break
    return "".join(chunks)


async def repl() -> None:
    """Interactive REPL — chat back and forth in the terminal."""
    try:
        from rich.console import Console
        from rich.markdown import Markdown
        console = Console()
        pretty = True
    except Exception:
        console = None
        pretty = False

    print("AdaL Support Agent v1 (web-search based). Type 'quit' to exit.")
    print(f"Streaming events logged to: {EVENTS_LOG.resolve()}\n")
    opts = make_options()
    turn = 0
    while True:
        try:
            user = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye.")
            break
        if not user:
            continue
        if user.lower() in {"quit", "exit", "q"}:
            break

        turn += 1
        label = f"repl-{turn}"
        answer = await ask(user, opts, label=label)
        if pretty:
            console.print(Markdown(answer))
        else:
            print(answer)
        print()


async def scripted() -> None:
    """Run the scripted test cases and print answers for review."""
    opts = make_options()
    print(f"Streaming events logged to: {EVENTS_LOG.resolve()}\n")
    for i, case in enumerate(TEST_CASES, 1):
        print(f"\n{'='*70}")
        print(f"TEST {i}/{len(TEST_CASES)}: {case}")
        print("=" * 70)
        answer = await ask(case, opts, label=f"script-{i}")
        print("\n--- ANSWER ---")
        print(answer)
        print()


def main() -> None:
    if "--script" in sys.argv:
        asyncio.run(scripted())
    else:
        asyncio.run(repl())


if __name__ == "__main__":
    main()
