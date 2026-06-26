"""
llm_client.py

The ONLY place in your project that talks to the model. Every agent goes through
here. Keeping it in one file means that swapping Ollama for vLLM later (or any other
OpenAI-compatible server) is a one-file change — you'd only edit the client below.
"""

import json

import pydantic
from openai import OpenAI

import config


# Create one client, pointed at Ollama instead of the internet.
client = OpenAI(
    base_url=config.OLLAMA_BASE_URL,
    api_key=config.OLLAMA_API_KEY,
    timeout=120.0,
)


def chat(system_prompt: str, user_content: str) -> str:
    """
    Send ONE turn to the model and return its reply as plain text.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    response = client.chat.completions.create(model=config.MODEL, messages=messages)
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Model returned no text content (content is None).")
    return content


def chat_json(system_prompt: str, user_content: str, schema: type) -> object:
    """
    Like chat(), but forces the model to return JSON and validates it against a
    Pydantic schema. The Reviewer uses this so you get a trustworthy
    {approved, feedback} object instead of prose.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content
    if content is None:
        raise ValueError("Model returned no text content (content is None).")
    try:
        return schema.model_validate_json(content)
    except (pydantic.ValidationError, json.JSONDecodeError) as e:
        raise ValueError(f"Model returned unparseable JSON: {e}") from e
