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

# TODO: write instructions that make the model output ONLY a short, numbered plan
#       of steps for solving a coding task — the approach, not the code itself.
PLANNER_SYSTEM_PROMPT = """"""

# TODO: write instructions that make the model write the actual code for a given
#       plan. Tell it to return only the code, in a single block, nothing else.
CODER_SYSTEM_PROMPT = """"""

# TODO: write instructions that make the model judge the code and reply with a
#       verdict. It must say whether the code is correct/complete and, if not, give
#       specific feedback. Tell it to answer as JSON with keys "approved" and
#       "feedback" (this is what chat_json expects).
REVIEWER_SYSTEM_PROMPT = """"""


# --- Agent functions ------------------------------------------------------------

def plan(user_request: str) -> str:
    """
    Run the Planner on the user's request and return the plan text.
    Implement: call the model through llm_client.chat(...) with the Planner prompt
    and the user_request, and return what comes back.
    """
    pass


def write_code(plan_text: str, feedback: str = "") -> str:
    """
    Run the Coder and return the code it writes.
    Implement: build one user message from the plan (and, if `feedback` is non-empty,
    include the Reviewer's feedback so the Coder can fix the previous attempt), then
    call llm_client.chat(...) with the Coder prompt and return the result.
    """
    pass


def review(code: str) -> ReviewResult:
    """
    Run the Reviewer and return a ReviewResult (approved + feedback).
    Implement: call llm_client.chat_json(...) with the Reviewer prompt, the `code`,
    and the ReviewResult schema, and return the validated object.
    """
    pass
