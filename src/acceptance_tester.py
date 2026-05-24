"""
Приёмочное тестирование чёрным ящиком.
Читает файл тестов, запускает программу, сверяет вывод.
Поддерживает программы из одного файла и из нескольких модулей 
"""

import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path


def parse_test_file(filepath: str) -> list[dict]:
    """
    Парсит файл с тестами.
    Разбивает на блоки по # TEST и извлекает mode, expression, expected.
    """
    tests = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    blocks = content.split("# TEST")
    
    for block in blocks[1:]:
        lines = block.strip().split("\n")
        
        test = {"name": lines[0].strip()}
        
        i = 1
        while i < len(lines):
            line = lines[i].strip()
            
            if line == ">>> MODE":
                i += 1
                if i < len(lines):
                    test["mode"] = lines[i].strip()
            elif line == ">>> EXPRESSION":
                i += 1
                if i < len(lines):
                    # Выражение может быть пустым
                    test["expression"] = lines[i]
            elif line == "<<< OUTPUT":
                i += 1
                if i < len(lines):
                    test["expected"] = lines[i].strip()
            i += 1
        
        if "mode" in test and "expression" in test and "expected" in test:
            tests.append(test)
    
    return tests


def run_single_test(program_path: str, mode: str, expression: str) -> str:
    """
    Запускает программу с заданными mode и expression.
    program_path — путь к папке с .py файлами или к одному solution.py.
    Возвращает содержимое Out.txt или сообщение об ошибке.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        
        # Создаём In.txt
        in_file = tmpdir / "In.txt"
        in_file.write_text(f"{mode}\n{expression}", encoding="utf-8")
        
        program_path = Path(program_path)
        
        # Определяем, что запускать
        if program_path.is_dir():
            # Копируем ВСЕ .py файлы из папки
            for py_file in program_path.glob("*.py"):
                shutil.copy(py_file, tmpdir / py_file.name)
            
            # Ищем точку входа: Main.py или solution.py
            main_candidates = ["Main.py", "main.py", "solution.py"]
            main_file = None
            for name in main_candidates:
                candidate = tmpdir / name
                if candidate.exists():
                    main_file = candidate
                    break
            
            if main_file is None:
                # Берём любой .py файл
                py_files = list(tmpdir.glob("*.py"))
                if py_files:
                    main_file = py_files[0]
                else:
                    return "ERROR: Не найдены .py файлы"
        else:
            # Один файл
            dest = tmpdir / "solution.py"
            shutil.copy(program_path, dest)
            main_file = dest
        
        # Запускаем
        try:
            result = subprocess.run(
                [sys.executable, str(main_file)],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=10,
            )
        except subprocess.TimeoutExpired:
            return "TIMEOUT"
        except Exception as e:
            return f"ERROR: {e}"
        
        out_file = tmpdir / "Out.txt"
        if out_file.exists():
            return out_file.read_text(encoding="utf-8").strip()
        
        return ""


def run_acceptance_tests(program_path: str, test_file: str) -> dict:
    """
    Запускает все тесты из файла.
    Возвращает словарь с результатами.
    """
    tests = parse_test_file(test_file)
    
    passed = 0
    failed = 0
    errors = []
    
    print(f"Программа: {program_path}")
    print(f"Тестовый файл: {test_file}")
    print(f"Всего тестов: {len(tests)}")
    print(f"{'='*60}")
    
    for i, test in enumerate(tests, 1):
        name = test.get("name", f"Тест {i}")
        mode = test.get("mode", "")
        expression = test.get("expression", "")
        expected = test.get("expected", "")
        
        result = run_single_test(program_path, mode, expression)
        
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        else:
            failed += 1
            errors.append({
                "name": name,
                "mode": mode,
                "expression": expression,
                "expected": expected,
                "got": result,
            })
        
        print(f"{status} Тест {i}: {name}")
        if result != expected:
            print(f"   Режим: '{mode}'")
            print(f"   Выражение: '{expression}'")
            print(f"   Ожидалось: '{expected}'")
            print(f"   Получено:  '{result}'")
    
    print(f"\n{'='*60}")
    print(f"ИТОГО: {passed}/{len(tests)} пройдено")
    print(f"Пройдено: {passed}")
    print(f"Провалено: {failed}")
    
    pass_rate = round(passed / len(tests) * 100, 2) if tests else 0
    
    print(f"Процент прохождения: {pass_rate}%")
    
    return {
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate,
        "errors": errors,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    program_path = sys.argv[1]
    test_file = sys.argv[2]
    
    if not os.path.exists(program_path):
        print(f"Ошибка: {program_path} не найден")
        sys.exit(1)
    
    if not os.path.exists(test_file):
        print(f"Ошибка: {test_file} не найден")
        sys.exit(1)
    
    run_acceptance_tests(program_path, test_file)