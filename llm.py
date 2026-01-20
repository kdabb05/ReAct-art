# llm.py
"""
OpenRouter LLM API integration for ReAct agent.
Reads API key from .openrouter_api_key in project root.
"""
import os
import requests

API_KEY_PATH = ".openrouter_api_key"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"  # You can change this if needed

class LLM:
    def __init__(self):
        self.api_key = self._read_api_key()

    def _read_api_key(self):
        try:
            with open(API_KEY_PATH, "r") as f:
                return f.read().strip()
        except Exception:
            raise RuntimeError(f"OpenRouter API key file '{API_KEY_PATH}' not found or unreadable.")

    def complete(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        data = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 512,
        }
        response = requests.post(API_URL, headers=headers, json=data)
        if response.status_code != 200:
            raise RuntimeError(f"OpenRouter API error: {response.status_code} {response.text}")
        result = response.json()
        return result["choices"][0]["message"]["content"]

llm = LLM()
