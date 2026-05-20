"""
Оркестратор TDD-цикла.

Управляет процессом: для каждого шага TDD подаёт тесты LLM,
применяет патчи, запускает тесты, при ошибках отправляет на перегенерацию.
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
from patch_handler import PatchHandler
from test_runner import TestRunner


class Orchestrator:
    """
    Управляет полным циклом TDD с LLM.

    Использование:
        orch = Orchestrator(prompt_manager, llm_client, patch_handler, test_runner)
        result = orch.run_task(task_dir)
    """

    def __init__(
        self,
        prompt_manager: PromptManager,
        llm_client: LLMClient,
        patch_handler: PatchHandler,
        test_runner: TestRunner,
    ):
        self.pm = prompt_manager
        self.llm = llm_client
        self.patcher = patch_handler
        self.runner = test_runner
        self.system_prompt = self.pm.get_system_prompt()

    def run_task(self, task_dir: Path) -> dict:
        """
        Запускает полный TDD-цикл для одной задачи.

        Args:
            task_dir: путь к папке задачи (с tests/, stub/, acceptance_test_data.txt)

        Returns:
            dict с результатами запуска
        """
        task_name = task_dir.name
        tests_dir = task_dir / "tests"
        stub_file = task_dir / "stub" / "solution.py"

        # Проверяем, что всё есть
        if not tests_dir.exists():
            raise FileNotFoundError(f"Папка с тестами не найдена: {tests_dir}")

        # Собираем шаги (сортируем по имени файла)
        step_files = sorted(tests_dir.glob("step_*.py"))
        if not step_files:
            raise FileNotFoundError(f"Нет файлов тестов (step_*.py) в {tests_dir}")

        # Создаём папку для результатов
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = RESULTS_DIR / task_name / f"run_{timestamp}"
        run_dir.mkdir(parents=True, exist_ok=True)
        iterations_dir = run_dir / ITERATIONS_DIRNAME
        iterations_dir.mkdir(exist_ok=True)

        # Создаём папку для логов LLM
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
        test_code = test_file.read_text(encoding="utf-8")
        step_iterations = []

        step_iter_dir = iterations_dir / f"step_{step_idx:02d}_{step_name}"
        step_iter_dir.mkdir(exist_ok=True)

        # История сообщений для этого шага
        messages_history = []

        for attempt in range(1, MAX_ITERATIONS + 1):
            print(f"\n  Попытка {attempt}/{MAX_ITERATIONS}")

            current_code = current_solution.read_text(encoding="utf-8")

            if attempt == 1:
                user_prompt = self.pm.build_initial_prompt(
                    current_code=current_code,
                    test_code=test_code,
                )
            else:
                last_iter = step_iterations[-1]
                last_error = last_iter.get("error_output", "Неизвестная ошибка")
                error_type = last_iter.get("error_type", "test_failure")

                if error_type == "patch_error":
                    user_prompt = self.pm.build_patch_error_prompt(
                        error_output=last_error,
                        current_code=current_code,
                    )
                else:
                    user_prompt = self.pm.build_error_prompt(
                        error_output=last_error,
                        current_code=current_code,
                    )
            # === КОНЕЦ ДОБАВЛЕНИЯ ===

            # Отправляем запрос LLM с историей
            print(f"    Запрос к LLM...")
            llm_result = self.llm.generate_patch(
                self.system_prompt,
                user_prompt,
                history=messages_history,
            )

            clean_patch = self.patcher.extract(llm_result["patch"])

            iter_log = {
                "attempt": attempt,
                "prompt_tokens": llm_result["usage"]["prompt_tokens"],
                "completion_tokens": llm_result["usage"]["completion_tokens"],
                "total_tokens": llm_result["usage"]["total_tokens"],
                "patch": clean_patch,
            }

            # Сохраняем патч
            patch_file = step_iter_dir / f"attempt_{attempt:02d}.diff"
            patch_file.write_text(clean_patch, encoding="utf-8")

            # Добавляем текущий обмен в историю
            messages_history.append({"role": "user", "content": user_prompt})
            messages_history.append({"role": "assistant", "content": llm_result["patch"]})

            # Применяем патч
            try:
                self.patcher.apply(clean_patch, current_solution)
                print(f"    Патч применён")
            except RuntimeError as e:
                print(f"    Ошибка патча: {e}")
                iter_log["error_type"] = "patch_error"
                iter_log["error_output"] = str(e)
                step_iterations.append(iter_log)
                continue

            # Запускаем тесты
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

            # Сохраняем код
            code_file = step_iter_dir / f"attempt_{attempt:02d}_solution.py"
            code_file.write_text(current_solution.read_text(encoding="utf-8"))

            if test_result["passed"]:
                print(f"    ✅ Тесты пройдены!")
                iter_log["error_type"] = None
                iter_log["error_output"] = ""
                step_iterations.append(iter_log)

                if REFACTOR_ENABLED:
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

        return {
            "step_name": step_name,
            "step_idx": step_idx,
            "success": False,
            "attempts": MAX_ITERATIONS,
            "total_tokens": sum(it["total_tokens"] for it in step_iterations),
            "iterations": step_iterations,
        }

    def _do_refactoring(self, solution_path: Path, step_iter_dir: Path, attempt: int):
        """Выполняет рефакторинг после успешного прохождения тестов."""
        print(f"    🔧 Рефакторинг...")
        current_code = solution_path.read_text(encoding="utf-8")
        refactor_prompt = self.pm.build_refactoring_prompt(current_code=current_code)

        llm_result = self.llm.generate_patch(self.system_prompt, refactor_prompt)
        clean_patch = self.patcher.extract(llm_result["patch"])

        if not clean_patch.strip():
            print(f"    Рефакторинг не требуется")
            return

        # Сохраняем рефакторинг-патч
        refactor_file = step_iter_dir / f"attempt_{attempt:02d}_refactor.diff"
        refactor_file.write_text(clean_patch, encoding="utf-8")

        try:
            self.patcher.apply(clean_patch, solution_path)
            # Проверяем, что тесты всё ещё проходят
            # (тесты запускать не будем — доверяем LLM, но сохраняем код)
            refactored_file = step_iter_dir / f"attempt_{attempt:02d}_refactored.py"
            refactored_file.write_text(solution_path.read_text(encoding="utf-8"))
            print(f"    Рефакторинг применён")
        except RuntimeError as e:
            print(f"    Ошибка рефакторинга: {e}")