"""
Анализатор покрытия кода тестами.
Запускает pytest через coverage.py для всех тестов в указанной папке.
"""

import subprocess
import sys
import shutil
import tempfile
from pathlib import Path


def run_coverage_analysis(source_path: str, tests_dir: str):
    """
    Запускает тесты и анализирует покрытие кода.

    Args:
        source_path: путь к solution.py (код, который анализируем)
        tests_dir: путь к папке с тестовыми файлами (.py)
    """
    source = Path(source_path).resolve()
    tests = Path(tests_dir).resolve()

    if not source.exists():
        print(f"Файл {source} не найден")
        return

    if not tests.exists() or not tests.is_dir():
        print(f"Папка {tests} не найдена")
        return

    # Создаём временную папку, копируем туда файлы кода и все тесты
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Копируем solution.py
        shutil.copy(source, tmpdir / source.name)

        # Копируем все .py файлы из папки тестов
        for test_file in tests.glob("*.py"):
            shutil.copy(test_file, tmpdir / test_file.name)

        print(f"Анализируемый файл: {source}")
        print(f"Папка с тестами: {tests}")
        print(f"{'='*60}")

        # Запускаем pytest через coverage
        cmd_run = [
            sys.executable, "-m", "coverage", "run",
            "--source", str(tmpdir),
            "-m", "pytest", str(tmpdir), "-v"
        ]

        result = subprocess.run(cmd_run, capture_output=True, text=True, cwd=tmpdir)

        print(result.stdout)
        if result.returncode != 0:
            print("Некоторые тесты упали:")
            print(result.stderr)

        # Отчёт о покрытии — ТОЛЬКО для файлов кода (не тестов)
        print(f"{'='*60}")
        print("ОТЧЁТ О ПОКРЫТИИ КОДА")
        print(f"{'='*60}")

        # Исключаем файлы, начинающиеся с test_
        cmd_report = [
            sys.executable, "-m", "coverage", "report", "-m",
            "--omit", str(tmpdir / "test_*.py")
        ]
        subprocess.run(cmd_report, cwd=tmpdir)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python coverage_analyzer.py <solution.py> <папка_с_тестами>")
        print("Пример: python coverage_analyzer.py black_tests/llm_solution/solution.py black_tests/cov_tests/")
        sys.exit(1)

    run_coverage_analysis(sys.argv[1], sys.argv[2])