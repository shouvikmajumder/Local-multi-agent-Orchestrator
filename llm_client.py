"""
llm_client.py

The ONLY place in your project that talks to the model. Every agent goes through
here. Keeping it in one file means that swapping Ollama for vLLM later (or any other
OpenAI-compatible server) is a one-file change — you'd only edit the client below.
"""

from openai import OpenAI

import config


# Create one client, pointed at Ollama instead of the internet.
#
# TODO: build an OpenAI(...) client and store it in a module-level variable named
#       `client`. Pass it base_url=config.OLLAMA_BASE_URL and
#       api_key=config.OLLAMA_API_KEY.
#
# client = ...


def chat(system_prompt: str, user_content: str) -> str:
    """
    Send ONE turn to the model and return its reply as plain text.

    Steps to implement:
      1. Build a `messages` list with two dicts:
           - {"role": "system", "content": system_prompt}  (the agent's fixed instructions)
           - {"role": "user",   "content": user_content}    (the task for this turn)
      2. Call client.chat.completions.create(model=config.MODEL, messages=messages).
      3. Pull out and return the assistant's text:
           response.choices[0].message.content
    """
    pass  # implement the three steps above


def chat_json(system_prompt: str, user_content: str, schema: type) -> object:
    """
    Like chat(), but forces the model to return JSON and validates it against a
    Pydantic schema. The Reviewer uses this so you get a trustworthy
    {approved, feedback} object instead of prose.

    Steps to implement:
      1. Same `messages` list as chat().
      2. Call create(...) the same way, but also pass
           response_format={"type": "json_object"}
         so the model is told to emit JSON. (Also make sure the system prompt itself
         tells the model to answer as JSON — see the README note on structured output.)
      3. Take the returned text (response.choices[0].message.content) and turn it into
         a validated object with:  schema.model_validate_json(text)
      4. Return that validated object.
    """
    pass  # implement the four steps above
