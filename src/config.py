"""
Центральный файл конфигурации для TTD Experiment Runner.

Все пути, настройки API и параметры экспериментов управляются отсюда.
"""

import os
from pathlib import Path

# -----------------------------------------------------------
# Базовые пути проекта
# -----------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # Корень проекта (ttd_experiment/)
EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"         # Папка с задачами
PROMPTS_DIR = PROJECT_ROOT / "prompts"                 # Шаблоны промптов
RESULTS_DIR = PROJECT_ROOT / "results"                 # Результаты запусков
STUB_FILENAME = "solution.py"                        # Имя файла-заглушки в каждой задаче

# -----------------------------------------------------------
# Настройки LLM (OpenAI-совместимый API)
# -----------------------------------------------------------
LLM_API_KEY = os.environ.get("LLM_API_KEY", "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")
LLM_BASE_URL = os.environ.get("LLM_BASE_URL", "https://openrouter.ai/api/v1")
LLM_MODEL = os.environ.get("LLM_MODEL", "deepseek/deepseek-v4-pro")
LLM_TEMPERATURE = 0.0                                  # Детерминированные ответы
LLM_MAX_TOKENS = 4096                                  # Максимальная длина ответа

# -----------------------------------------------------------
# Параметры TDD-цикла
# -----------------------------------------------------------
MAX_ITERATIONS = 5          # Максимальное количество попыток на один шаг
TEST_TIMEOUT = 30           # Таймаут на прогон pytest (секунды)
PATCH_TIMEOUT = 10          # Таймаут на применение патча (секунды)
REFACTOR_ENABLED = True     # Делать ли шаг рефакторинга после зелёных тестов

# -----------------------------------------------------------
# Имена папок внутри задачи
# -----------------------------------------------------------
TESTS_DIRNAME = "tests"         # Папка с пошаговыми тестами TDD
STUB_DIRNAME = "stub"           # Папка со скелетом кода
EXPECTED_DIRNAME = "expected"   # Папка с эталонным решением
ACCEPTANCE_FILENAME = "acceptance_test_data.txt"  # Файл приёмочных тестов
TASK_DESCRIPTION_FILENAME = "task_description.md"

# -----------------------------------------------------------
# Имена папок для результатов одного запуска
# -----------------------------------------------------------
FINAL_SOLUTION_FILENAME = "final_solution.py"
REPORT_FILENAME = "report.json"
METRICS_FILENAME = "metrics.json"
ACCEPTANCE_REPORT_FILENAME = "acceptance_report.json"
ITERATIONS_DIRNAME = "iterations"

# -----------------------------------------------------------
# Проверка обязательных переменных окружения
# -----------------------------------------------------------
def validate():
    """Выбрасывает исключение, если конфигурация некорректна."""
    if LLM_API_KEY == "sk-placeholder":
        raise RuntimeError("Установите переменную окружения OPENAI_API_KEY")
    if not EXPERIMENTS_DIR.exists():
        raise FileNotFoundError(f"Папка experiments не найдена: {EXPERIMENTS_DIR}")
    if not PROMPTS_DIR.exists():
        raise FileNotFoundError(f"Папка prompts не найдена: {PROMPTS_DIR}")