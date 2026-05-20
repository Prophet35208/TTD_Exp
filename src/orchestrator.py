"""
Оркестратор TDD-цикла.

Управляет процессом: для каждого шага TDD подаёт тесты LLM,
получает полный код, запускает тесты, при ошибках отправляет на перегенерацию.
"""

import time
import json
from pathlib import Path
from datetime import datetime

from config import (
    MAX_ITERATIONS,
    REFACTOR_ENABLED,
    RESULTS_DIR,
    FINAL_SOLUTION_FILENAME,
    REPORT_FILENAME,
    METRICS_FILENAME,
    ITERATIONS_DIRNAME,
    ACCEPTANCE_REPORT_FILENAME,
)
from prompt_manager import PromptManager
from llm_client import LLMClient
from test_runner import TestRunner


class Orchestrator:
    """
    Управляет полным циклом TDD с LLM.

    Использование:
        orch = Orchestrator(prompt_manager, llm_client, test_runner)
        result = orch.run_task(task_dir, step_file="step_01_test.py")
    """

    def __init__(
        self,
        prompt_manager: PromptManager,
        llm_client: LLMClient,
        test_runner: TestRunner,
    ):
        self.pm = prompt_manager
        self.llm = llm_client
        self.runner = test_runner
        self.system_prompt = self.pm.get_system_prompt()

    @staticmethod
    def _extract_code(response_text: str) -> str:
        """Извлекает чистый код из ответа LLM (убирает markdown-обёртку)."""
        import re
        text = response_text.strip()
        # Пробуем найти код внутри ```python, ```diff, или просто ```
        match = re.search(r"```(?:python|diff)?\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text

    def run_task(self, task_dir: Path, step_file: str = None) -> dict:
        """
        Запускает TDD-цикл для одного или всех шагов задачи.

        Args:
            task_dir: путь к папке задачи
            step_file: имя файла шага (например, "step_01_test.py"). 
                       Если None — выполняются все шаги по порядку.

        Returns:
            dict с результатами запуска
        """
        task_name = task_dir.name
        tests_dir = task_dir / "tests"
        stub_file = task_dir / "stub" / "solution.py"

        if not tests_dir.exists():
            raise FileNotFoundError(f"Папка с тестами не найдена: {tests_dir}")

        # Собираем шаги
        if step_file:
            step_files = [tests_dir / step_file]
            if not step_files[0].exists():
                raise FileNotFoundError(f"Файл тестов не найден: {step_files[0]}")
        else:
            step_files = sorted(tests_dir.glob("step_*.py"))
            if not step_files:
                raise FileNotFoundError(f"Нет файлов тестов (step_*.py) в {tests_dir}")

        # Создаём папку для результатов
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = RESULTS_DIR / task_name / f"run_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)
        iterations_dir = run_dir / ITERATIONS_DIRNAME
        iterations_dir.mkdir(exist_ok=True)

        # Папка для логов LLM-запросов
        llm_log_dir = run_dir / "llm_logs"
        llm_log_dir.mkdir(exist_ok=True)
        self.llm.log_dir = llm_log_dir

        # Начальный solution.py (из stub или пустой)
        current_solution = run_dir / "solution.py"
        if stub_file.exists():
            current_solution.write_text(stub_file.read_text(encoding="utf-8"))
        else:
            current_solution.write_text("")

        # История всех шагов
        all_steps = []
        total_start_time = time.time()

        # Главный цикл по шагам TDD
        for step_idx, test_file in enumerate(step_files, 1):
            step_name = test_file.stem
            print(f"\n{'='*60}")
            print(f"Шаг {step_idx}/{len(step_files)}: {step_name}")
            print(f"{'='*60}")

            step_result = self._run_step(
                step_name=step_name,
                step_idx=step_idx,
                test_file=test_file,
                current_solution=current_solution,
                run_dir=run_dir,
                iterations_dir=iterations_dir,
            )
            all_steps.append(step_result)

            if not step_result["success"]:
                print(f"\n[!] Шаг {step_name} не пройден за {MAX_ITERATIONS} попыток.")
                break

        total_time = time.time() - total_start_time

        # Итоговый отчёт
        report = {
            "task": task_name,
            "step_file": step_file,
            "timestamp": timestamp,
            "total_steps": len(step_files),
            "completed_steps": len([s for s in all_steps if s["success"]]),
            "all_passed": all(s["success"] for s in all_steps),
            "total_time_sec": round(total_time, 2),
            "steps": all_steps,
        }

        # Сохраняем отчёт
        report_path = run_dir / REPORT_FILENAME
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        # Сохраняем финальный solution.py
        final_path = run_dir / FINAL_SOLUTION_FILENAME
        final_path.write_text(current_solution.read_text(encoding="utf-8"))

        print(f"\n{'='*60}")
        print(f"Задача: {task_name}")
        if step_file:
            print(f"Шаг: {step_file}")
        print(f"Пройдено шагов: {report['completed_steps']}/{report['total_steps']}")
        print(f"Все тесты пройдены: {report['all_passed']}")
        print(f"Общее время: {report['total_time_sec']}с")
        print(f"Результаты сохранены в: {run_dir}")

        return report

    def _run_step(
        self,
        step_name: str,
        step_idx: int,
        test_file: Path,
        current_solution: Path,
        run_dir: Path,
        iterations_dir: Path,
    ) -> dict:
        """
        Выполняет один шаг TDD.

        Args:
            step_name: имя шага
            step_idx: номер шага
            test_file: путь к файлу с тестами
            current_solution: путь к текущему solution.py
            run_dir: папка результатов запуска
            iterations_dir: папка для логов итераций

        Returns:
            dict с результатом шага
        """
        test_code = test_file.read_text(encoding="utf-8")
        step_iterations = []

        # Папка для итераций этого шага
        step_iter_dir = iterations_dir / f"step_{step_idx:02d}_{step_name}"
        step_iter_dir.mkdir(exist_ok=True)

        # История сообщений для этого шага
        messages_history = []

        for attempt in range(1, MAX_ITERATIONS + 1):
            print(f"\n  Попытка {attempt}/{MAX_ITERATIONS}")

            # 1. Формируем промпт
            current_code = current_solution.read_text(encoding="utf-8")

            if attempt == 1:
                user_prompt = self.pm.build_initial_prompt(
                    current_code=current_code,
                    test_code=test_code,
                )
            else:
                last_iter = step_iterations[-1]
                last_error = last_iter.get("error_output", "Неизвестная ошибка")
                user_prompt = self.pm.build_error_prompt(
                    error_output=last_error,
                    current_code=current_code,
                )

            # 2. Отправляем запрос LLM (с историей)
            print(f"    Запрос к LLM...")
            llm_result = self.llm.generate_patch(
                self.system_prompt,
                user_prompt,
                history=messages_history,
            )

            # 3. Извлекаем новый код
            new_code = self._extract_code(llm_result["text"])

            iter_log = {
                "attempt": attempt,
                "prompt_tokens": llm_result["usage"]["prompt_tokens"],
                "completion_tokens": llm_result["usage"]["completion_tokens"],
                "total_tokens": llm_result["usage"]["total_tokens"],
                "code": new_code,
            }

            # Сохраняем ответ модели
            code_file = step_iter_dir / f"attempt_{attempt:02d}_response.py"
            code_file.write_text(new_code, encoding="utf-8")

            # Добавляем текущий обмен в историю
            messages_history.append({"role": "user", "content": user_prompt})
            messages_history.append({"role": "assistant", "content": new_code})

            # 4. Перезаписываем solution.py новым кодом
            current_solution.write_text(new_code, encoding="utf-8")
            print(f"    Код записан в solution.py")

            # 5. Запускаем тесты
            print(f"    Запуск тестов...")
            test_result = self.runner.run(current_solution, test_file)

            iter_log["tests_passed"] = test_result["passed"]
            iter_log["stdout"] = test_result["stdout"]
            iter_log["stderr"] = test_result["stderr"]

            # Сохраняем вывод тестов
            test_output_file = step_iter_dir / f"attempt_{attempt:02d}_test_output.txt"
            test_output_file.write_text(
                f"STDOUT:\n{test_result['stdout']}\n\nSTDERR:\n{test_result['stderr']}",
                encoding="utf-8"
            )

            # Сохраняем код после этой попытки
            solution_copy = step_iter_dir / f"attempt_{attempt:02d}_solution.py"
            solution_copy.write_text(current_solution.read_text(encoding="utf-8"))

            if test_result["passed"]:
                print(f"    ✅ Тесты пройдены!")
                iter_log["error_type"] = None
                iter_log["error_output"] = ""
                step_iterations.append(iter_log)

                # Рефакторинг (опционально)
                if REFACTOR_ENABLED:
                    self._current_test_file = test_file
                    self._do_refactoring(current_solution, step_iter_dir, attempt)

                return {
                    "step_name": step_name,
                    "step_idx": step_idx,
                    "success": True,
                    "attempts": attempt,
                    "total_tokens": sum(it["total_tokens"] for it in step_iterations),
                    "iterations": step_iterations,
                }
            else:
                error_output = test_result["stderr"] or test_result["stdout"]
                iter_log["error_type"] = "test_failure"
                iter_log["error_output"] = error_output
                print(f"    ❌ Тесты упали")

            step_iterations.append(iter_log)

        # Исчерпали лимит попыток
        return {
            "step_name": step_name,
            "step_idx": step_idx,
            "success": False,
            "attempts": MAX_ITERATIONS,
            "total_tokens": sum(it["total_tokens"] for it in step_iterations),
            "iterations": step_iterations,
        }

    def _do_refactoring(self, solution_path: Path, step_iter_dir: Path, attempt: int):
        """Выполняет рефакторинг с проверкой тестов."""
        print(f"    🔧 Рефакторинг...")
        current_code = solution_path.read_text(encoding="utf-8")
        refactor_prompt = self.pm.build_refactoring_prompt(current_code=current_code)

        llm_result = self.llm.generate_patch(self.system_prompt, refactor_prompt)
        new_code = self._extract_code(llm_result["text"])

        if not new_code.strip() or new_code.strip() == current_code.strip():
            print(f"    Рефакторинг не требуется")
            return

        # Сохраняем результат рефакторинга
        refactored_file = step_iter_dir / f"attempt_{attempt:02d}_refactored.py"
        refactored_file.write_text(new_code, encoding="utf-8")

        # Сохраняем старый код на случай отката
        backup_code = current_code

        # Применяем рефакторинг
        solution_path.write_text(new_code, encoding="utf-8")

        # Проверяем тесты
        if hasattr(self, '_current_test_file'):
            print(f"    Проверка тестов после рефакторинга...")
            test_result = self.runner.run(solution_path, self._current_test_file)

            if test_result["passed"]:
                print(f"    ✅ Тесты пройдены, рефакторинг успешен")
            else:
                print(f"    ❌ Тесты упали, откатываем рефакторинг")
                solution_path.write_text(backup_code, encoding="utf-8")
        else:
            print(f"    Рефакторинг применён (без проверки тестов)")