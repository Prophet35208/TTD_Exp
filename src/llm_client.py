"""
Клиент для взаимодействия с LLM через OpenAI-совместимый API.
Поддерживает локальные (Ollama) и облачные (OpenRouter) модели.
"""

import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI
import uuid


class LLMClient:
    def __init__(self, base_url: str, api_key: str, model: str, temperature: float = 0.0, log_dir: Path | None = None):
        self.model = model
        self.temperature = temperature
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.log_dir = log_dir
        self._call_counter = 0
        self.user_id = self._get_or_create_user_id()

    def _log_interaction(self, messages: list, response_text: str, usage: dict):
        """Сохраняет полный лог взаимодействия с LLM."""
        if not self.log_dir:
            return

        self._call_counter += 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        log_file = self.log_dir / f"llm_call_{self._call_counter:04d}_{timestamp}.json"

        log_entry = {
            "call_number": self._call_counter,
            "timestamp": timestamp,
            "model": self.model,
            "temperature": self.temperature,
            "messages": messages,
            "response": response_text,
            "usage": usage,
        }

        log_file.write_text(json.dumps(log_entry, indent=2, ensure_ascii=False), encoding="utf-8")

    def generate(self, system_prompt: str, user_prompt: str, history: list | None = None) -> dict:
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            extra_body={
                "reasoning": {"enabled": False}
            },
            user=self.user_id
        )

        usage = response.usage
        usage_data = {
            "prompt_tokens": usage.prompt_tokens if usage else 0,
            "completion_tokens": usage.completion_tokens if usage else 0,
            "total_tokens": usage.total_tokens if usage else 0,
        }

        response_text = response.choices[0].message.content or ""

        # Логируем взаимодействие
        self._log_interaction(messages, response_text, usage_data)

        return {
            "text": response_text,
            "usage": usage_data
        }

    def generate_patch(self, system_prompt: str, user_prompt: str, history: list | None = None) -> dict:
        result = self.generate(system_prompt, user_prompt, history)
        result["patch"] = result["text"]
        return result
    
    @staticmethod
    def _get_or_create_user_id() -> str:
        """Генерирует или загружает уникальный ID пользователя для OpenRouter."""
        config_dir = Path.home() / ".config" / "ttd_experiment"
        config_dir.mkdir(parents=True, exist_ok=True)
        id_file = config_dir / "machine_id"

        if id_file.exists():
            return id_file.read_text().strip()

        # Генерируем новый ID и сохраняем в файл
        user_id = f"ttd-user-{uuid.uuid4().hex[:16]}"
        id_file.write_text(user_id)
        return user_id