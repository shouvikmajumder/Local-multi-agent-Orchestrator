# Local Multi-Agent Orchestrator

A small **Planner → Coder → Reviewer** system that runs entirely on your machine via
Ollama. This is a *fill-in-the-blanks* scaffold: the structure, imports, and function
signatures are here, but every function body, agent prompt, and schema field is left as
comments for you to implement.

## How it works

The `orchestrator` (plain Python, not an AI) takes your request and calls three agents
in order. Each "agent" is just the same model with a different fixed system prompt:

1. **Planner** turns your request into a short plan.
2. **Coder** writes code for that plan.
3. **Reviewer** checks the code and either approves it or sends feedback back to the
   Coder. That revise-loop repeats until approved or until a max number of tries.

The orchestrator is the only thing that holds all the pieces — the agents never talk to
each other directly.

## Prerequisites

1. Install Ollama: <https://ollama.com>
2. Pull a model (this is the default in `config.py`):
   ```
   ollama pull qwen2.5-coder:7b
   ```
3. Make sure Ollama is running (open the app, or run `ollama serve`).

## Setup

Using **uv** (recommended):
```
uv venv
uv pip install -r requirements.txt
```

Or plain **venv + pip**:
```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

From inside the project folder:
```
python main.py
```

## Files — implement in this order

Build **bottom-up** so you can test each piece before moving on:

1. **`config.py`** — already filled in. Just change `MODEL` if your hardware differs.
2. **`llm_client.py`** — implement `chat()` first. Get it talking to Ollama and print a
   reply *before* building anything else. This is the foundation.
3. **`schemas.py`** — add the two fields to `ReviewResult`.
4. **`agents.py`** — write the three system prompts (the real creative work) and the
   three small functions that call the model.
5. **`orchestrator.py`** — wire the agents together into the loop.
6. **`main.py`** — get a request, run the orchestrator, print the result.

## Tip: test as you go

Don't write all six files then run. After `chat()` works, print its output. After two
agents chain together, read both outputs before adding the Reviewer and the loop. Small
steps make bugs obvious.

## Note on structured output (used by the Reviewer)

To make the Reviewer return reliable JSON (not prose), the exact argument depends on
versions. Start with `response_format={"type": "json_object"}` on the model call **and**
tell the model in its prompt to answer as JSON. Newer Ollama also accepts a full schema
via a `format` argument. If one path doesn't work, the other will.

## Not here yet (on purpose)

`asyncio`, an agent framework (LangGraph/CrewAI), quantization tuning, and vLLM. Get this
simple sequential version working first — those are all later upgrades that bolt on
cleanly once the core works.
