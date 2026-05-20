"""
Тест полного цикла через оркестратор.
Использует реальную задачу task_01_calculator.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    LLM_TEMPERATURE,
    PROMPTS_DIR,
    EXPERIMENTS_DIR,
    TEST_TIMEOUT,
    MAX_ITERATIONS,
    REFACTOR_ENABLED
)
from prompt_manager import PromptManager
from llm_client import LLMClient
from patch_handler import PatchHandler
from test_runner import TestRunner
from orchestrator import Orchestrator

# 1. Инициализация всех компонентов
pm = PromptManager(PROMPTS_DIR)
llm = LLMClient(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    model=LLM_MODEL,
    temperature=LLM_TEMPERATURE,
)
patcher = PatchHandler()
runner = TestRunner(timeout=TEST_TIMEOUT)

# 2. Создаём оркестратор
orch = Orchestrator(
    prompt_manager=pm,
    llm_client=llm,
    patch_handler=patcher,
    test_runner=runner,
)

# 3. Запускаем задачу
task_dir = EXPERIMENTS_DIR / "task_01"
print(f"Запуск задачи: {task_dir.name}")
print(f"Модель: {LLM_MODEL}")
print(f"Максимум итераций на шаг: {MAX_ITERATIONS}")
print(f"Рефакторинг: {'включён' if REFACTOR_ENABLED else 'выключен'}")

report = orch.run_task(task_dir)

# 4. Итоги
print(f"\n{'='*60}")
print(f"ИТОГИ:")
print(f"  Все шаги пройдены: {report['all_passed']}")
print(f"  Пройдено шагов: {report['completed_steps']}/{report['total_steps']}")
print(f"  Общее время: {report['total_time_sec']}с")