"""
Менеджер промптов для TTD Experiment Runner.

Загружает шаблоны из .md-файлов и заполняет плейсхолдеры переданными значениями.
"""

from pathlib import Path


class PromptManager:
    """
    Загружает и управляет шаблонами промптов.

    Использование:
        pm = PromptManager(prompts_dir)
        system = pm.load("system_prompt.md")
        filled = pm.fill("initial_step.md", current_code="...", test_code="...")
    """

    def __init__(self, prompts_dir: Path):
        """
        Args:
            prompts_dir: путь к папке с шаблонами .md
        """
        self.prompts_dir = Path(prompts_dir)
        if not self.prompts_dir.is_dir():
            raise FileNotFoundError(f"Папка с промптами не найдена: {self.prompts_dir}")

    def load(self, filename: str) -> str:
        """
        Загружает содержимое шаблона из файла.

        Args:
            filename: имя файла (например, "system_prompt.md")

        Returns:
            содержимое файла как строку
        """
        filepath = self.prompts_dir / filename
        if not filepath.is_file():
            raise FileNotFoundError(f"Шаблон не найден: {filepath}")
        return filepath.read_text(encoding="utf-8")

    def fill(self, filename: str, **kwargs) -> str:
        """
        Загружает шаблон и заполняет плейсхолдеры.

        Плейсхолдеры в шаблоне должны иметь формат {{key}}.

        Args:
            filename: имя файла шаблона
            **kwargs: пары ключ=значение для подстановки

        Returns:
            заполненный шаблон
        """
        template = self.load(filename)
        for key, value in kwargs.items():
            placeholder = f"{{{{{key}}}}}"
            template = template.replace(placeholder, str(value))
        return template

    def get_system_prompt(self) -> str:
        """Возвращает системный промпт без подстановок."""
        return self.load("system_prompt.md")

    def build_initial_prompt(self, current_code: str, test_code: str) -> str:
        """
        Формирует промпт для первого или очередного шага TDD.

        Args:
            current_code: текущее содержимое solution.py
            test_code: код тестов текущего шага

        Returns:
            заполненный промпт
        """
        return self.fill("initial_step.md",
                         current_code=current_code,
                         test_code=test_code)

    def build_patch_error_prompt(self, error_output: str, current_code: str) -> str:
        """
        Формирует промпт для исправления ошибки формата патча.

        Args:
            error_output: текст ошибки парсинга патча
            current_code: текущее содержимое solution.py

        Returns:
            заполненный промпт
        """
        return self.fill("patch_error.md",
                         error_output=error_output,
                         current_code=current_code)

    def build_error_prompt(self, error_output: str, current_code: str) -> str:
        """
        Формирует промпт для исправления ошибок.

        Args:
            error_output: вывод pytest с ошибками
            current_code: текущее содержимое solution.py

        Returns:
            заполненный промпт
        """
        return self.fill("error_feedback.md",
                         error_output=error_output,
                         current_code=current_code)

    def build_refactoring_prompt(self, current_code: str) -> str:
        """
        Формирует промпт для рефакторинга.

        Args:
            current_code: текущее содержимое solution.py

        Returns:
            заполненный промпт
        """
        return self.fill("refactoring.md", current_code=current_code)