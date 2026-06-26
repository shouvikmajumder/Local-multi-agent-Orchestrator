"""
schemas.py

Pydantic models that describe the EXACT shape an agent's answer must take.
You validate an agent's raw output against one of these so the rest of your code
can trust it (e.g. `if result.approved:`) instead of guessing from free text.
"""

from pydantic import BaseModel


# The Reviewer should hand back a verdict your code can branch on — not a paragraph.
#
# TODO: give this model two fields:
#         approved : bool   -> True if the code is good enough as-is
#         feedback : str    -> what the Coder should change (use "" when approved)
#
# Once you add them, you'll be able to write `result.approved` and `result.feedback`
# in the orchestrator.
class ReviewResult(BaseModel):
    pass  # delete this line and add the two fields described above
