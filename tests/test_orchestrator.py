"""
tests/test_orchestrator.py

Unit tests for the local multi-agent orchestrator.
All LLM calls are mocked — Ollama is never contacted.
"""

import io
import sys
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_response(content):
    """Build a minimal fake OpenAI chat-completion response."""
    message = MagicMock()
    message.content = content
    choice = MagicMock()
    choice.message = message
    response = MagicMock()
    response.choices = [choice]
    return response


# ---------------------------------------------------------------------------
# Test 1 — chat() raises ValueError when content is None
# ---------------------------------------------------------------------------

def test_chat_raises_on_none_content():
    """chat() must raise ValueError if the model returns content=None."""
    import llm_client

    with patch.object(llm_client.client.chat.completions, "create",
                      return_value=_make_response(None)):
        with pytest.raises(ValueError, match="content is None"):
            llm_client.chat("system", "user")


# ---------------------------------------------------------------------------
# Test 2 — chat_json() raises ValueError when content is None
# ---------------------------------------------------------------------------

def test_chat_json_raises_on_none_content():
    """chat_json() must raise ValueError if the model returns content=None."""
    import llm_client
    from schemas import ReviewResult

    with patch.object(llm_client.client.chat.completions, "create",
                      return_value=_make_response(None)):
        with pytest.raises(ValueError, match="content is None"):
            llm_client.chat_json("system", "user", ReviewResult)


# ---------------------------------------------------------------------------
# Test 3 — ReviewResult is valid when feedback is omitted
# ---------------------------------------------------------------------------

def test_review_result_feedback_default():
    """ReviewResult.feedback should default to '' when not supplied."""
    from schemas import ReviewResult

    result = ReviewResult.model_validate_json('{"approved": true}')
    assert result.approved is True
    assert result.feedback == ""


# ---------------------------------------------------------------------------
# Test 4 — agents.review() returns safe ReviewResult when chat_json raises
# ---------------------------------------------------------------------------

def test_review_returns_safe_result_on_parse_error():
    """agents.review() must catch chat_json errors and return approved=False."""
    import agents

    with patch("agents.llm_client.chat_json",
               side_effect=ValueError("bad json")):
        result = agents.review("some code")

    assert result.approved is False
    assert "parse error" in result.feedback.lower()


# ---------------------------------------------------------------------------
# Test 5 — Revision loop calls write_code MAX_REVISION_ROUNDS + 1 times
# ---------------------------------------------------------------------------

def test_revision_loop_exhausts_max_rounds():
    """
    When review never approves, write_code is called once initially and then
    once per revision round — total MAX_REVISION_ROUNDS + 1 times.
    """
    import config
    import orchestrator
    from schemas import ReviewResult

    with patch("orchestrator.agents.plan", return_value="plan"), \
         patch("orchestrator.agents.write_code", return_value="code") as mock_write, \
         patch("orchestrator.agents.review",
               return_value=ReviewResult(approved=False, feedback="fix this")):

        orchestrator.run("request")

    assert mock_write.call_count == config.MAX_REVISION_ROUNDS + 1


# ---------------------------------------------------------------------------
# Test 6 — Revision loop stops early when approved on first review
# ---------------------------------------------------------------------------

def test_revision_loop_stops_when_approved():
    """When review approves immediately, write_code is called exactly once."""
    import orchestrator
    from schemas import ReviewResult

    with patch("orchestrator.agents.plan", return_value="plan"), \
         patch("orchestrator.agents.write_code", return_value="code") as mock_write, \
         patch("orchestrator.agents.review",
               return_value=ReviewResult(approved=True)):

        orchestrator.run("request")

    assert mock_write.call_count == 1


# ---------------------------------------------------------------------------
# Test 7 — main() prints result on success
# ---------------------------------------------------------------------------

def test_main_prints_result_on_success(capsys):
    """main() should print the code returned by orchestrator.run()."""
    import main as main_module

    with patch("builtins.input", return_value="test request"), \
         patch("main.orchestrator.run", return_value="def foo(): pass"):

        main_module.main()

    captured = capsys.readouterr()
    assert "def foo(): pass" in captured.out


# ---------------------------------------------------------------------------
# Test 8 — main() exits with code 1 on error
# ---------------------------------------------------------------------------

def test_main_exits_with_code_1_on_error():
    """main() should call sys.exit(1) when orchestrator.run() raises."""
    import main as main_module

    with patch("builtins.input", return_value="request"), \
         patch("main.orchestrator.run", side_effect=RuntimeError("oops")):

        with pytest.raises(SystemExit) as exc_info:
            main_module.main()

    assert exc_info.value.code == 1
