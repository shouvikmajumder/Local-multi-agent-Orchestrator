"""
config.py

Central place for settings you'll tweak. Nothing here is "logic" — just values,
so this file is already filled in. Keeping settings in one place (instead of
hard-coding strings all over) is also what lets you keep agent prompts identical
later, which helps the model cache them.
"""

# Ollama exposes an OpenAI-compatible server at this local address.
# The "/v1" on the end is what makes the openai client talk to it correctly.
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Ollama ignores the API key, but the openai client requires *some* string,
# so we give it a dummy one.
OLLAMA_API_KEY = "ollama"

# The model you pulled with `ollama pull`. Change this to match your hardware:
#   - 8 GB GPU   ->  "qwen2.5-coder:7b"   (good default)
#   - 16 GB+     ->  "qwen3-coder:30b"    (stronger for longer agent loops)
#   - no GPU     ->  "phi4-mini"          (small, CPU-friendly)
MODEL = "qwen2.5-coder:7b"

# Safety net so the Coder <-> Reviewer loop can't run forever. After this many
# revision attempts, the orchestrator gives up and returns its best attempt.
MAX_REVISION_ROUNDS = 3
