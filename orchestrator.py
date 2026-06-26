"""
orchestrator.py

The conductor. This is plain Python, NOT an AI. It calls the agents in order,
carries each one's output to the next, and runs the revise-until-approved loop.
This is where the whole system comes together.
"""

import agents
import config


def run(user_request: str) -> str:
    """
    Take a user's request and return finished, reviewed code.

    The flow to implement (this matches the diagrams):

      1. PLAN
         Ask agents.plan(user_request) for a plan. Store it.

      2. CODE (first draft)
         Ask agents.write_code(plan) for the first version of the code. Store it.

      3. REVISION LOOP — repeat up to config.MAX_REVISION_ROUNDS times:
           a. REVIEW   -> call agents.review(code) to get a ReviewResult.
           b. If result.approved is True -> stop the loop, the code is done.
           c. Otherwise -> call agents.write_code(plan, result.feedback) again,
              passing the feedback so the Coder can fix it. Replace `code` with the
              new draft and continue the loop.

      4. RETURN
         Return the final `code` — either the approved version, or the best attempt
         after the last round if it never got approved.

    Key idea: the orchestrator is the ONLY thing holding the plan, the code, and the
    feedback all at once. The agents never see each other — you move the data
    between them right here.
    """
    plan_text = agents.plan(user_request)
    code = agents.write_code(plan_text)
    for _ in range(config.MAX_REVISION_ROUNDS):
        result = agents.review(code)
        if result.approved:
            break
        code = agents.write_code(plan_text, result.feedback)
    return code
