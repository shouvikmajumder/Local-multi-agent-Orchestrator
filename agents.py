"""
agents.py

The three agents. Remember: an "agent" is nothing more than a fixed system prompt
plus a call to the model. All three share the same underlying model — only the
prompt (the "hat" it wears) is different.
"""

import llm_client
from schemas import ReviewResult


# --- System prompts -------------------------------------------------------------
# These are the heart of each agent and the main thing YOU design. Each one should
# describe the agent's single job and the exact format you want back. Keep each
# prompt fixed and self-contained.

PLANNER_SYSTEM_PROMPT = """You are a software planning assistant. When given a coding task, output ONLY a concise, numbered step-by-step plan describing the approach to solve it. Do not write any code. Do not add any explanation or commentary beyond the numbered steps."""

CODER_SYSTEM_PROMPT = """You are a software implementation assistant. When given a plan, write ONLY the implementation code. Output a single Python code block fenced with ```python. Do not include any explanation, prose, or commentary outside the code block."""

REVIEWER_SYSTEM_PROMPT = """You are a code review assistant. When given a Python code snippet, review it for correctness, completeness, and edge-case handling. Respond ONLY with a JSON object containing exactly two keys:
- "approved": true if the code is correct, complete, and handles edge cases; false otherwise.
- "feedback": a specific, actionable list of what should be fixed (use "" when approved).
Output no prose, no explanation — only the JSON object."""


# --- Agent functions ------------------------------------------------------------

def plan(user_request: str) -> str:
    return llm_client.chat(PLANNER_SYSTEM_PROMPT, user_request)


def write_code(plan_text: str, feedback: str = "") -> str:
    user_message = plan_text
    if feedback:
        user_message += f"\n\nPrevious attempt was rejected. Fix these issues:\n{feedback}"
    return llm_client.chat(CODER_SYSTEM_PROMPT, user_message)


def review(code: str) -> ReviewResult:
    try:
        return llm_client.chat_json(REVIEWER_SYSTEM_PROMPT, code, ReviewResult)
    except Exception as e:
        return ReviewResult(approved=False, feedback=f"Review parse error: {e}")
