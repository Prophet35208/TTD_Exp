"""
Запуск pytest во временной изолированной папке.
"""

import subprocess
import tempfile
import shutil
from pathlib import Path
import sys


class TestRunner:
    """
    Запускает тесты для solution.py во временной папке.

    Использование:
        runner = TestRunner()
        result = runner.run(solution_path, test_path)
        print(result["passed"])   # True/False
        print(result["stdout"])   # вывод pytest
    """

    def __init__(self, timeout: int = 30):
        """
        Args:
            timeout: таймаут на выполнение тестов в секундах
        """
        self.timeout = timeout

    def run(self, solution_path: Path, test_path: Path) -> dict:
        """
        Запускает pytest для проверки solution.py.

        Args:
            solution_path: путь к файлу solution.py
            test_path: путь к файлу с тестами (step_NN_test.py)

        Returns:
            dict с ключами:
                "passed" — True если все тесты пройдены
                "stdout" — вывод pytest
                "stderr" — ошибки pytest
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Копируем solution.py и тесты во временную папку
            shutil.copy(solution_path, tmpdir / "solution.py")
            shutil.copy(test_path, tmpdir / test_path.name)

            # Запускаем pytest
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", test_path.name, "-v", "--tb=short"],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                )
                return {
                    "passed": result.returncode == 0,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                }
            except subprocess.TimeoutExpired:
                return {
                    "passed": False,
                    "stdout": "",
                    "stderr": f"Тесты превысили лимит времени ({self.timeout}с)",
                }