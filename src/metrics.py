"""
Анализ качества кода.
Вычисляет цикломатическую сложность, LOC, дублирование, предупреждения линтеров.
Поддерживает одиночные файлы и папки с .py файлами.
"""

import subprocess
import sys
import json
from pathlib import Path


def get_complexity(filepath: str) -> dict:
    """Возвращает среднюю и максимальную цикломатическую сложность."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "radon", "cc", filepath, "-j"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return {"avg": None, "max": None, "error": result.stderr}
        
        data = json.loads(result.stdout)
        complexities = []
        for file_data in data.values():
            for block in file_data:
                complexities.append(block.get("complexity", 0))
        
        if not complexities:
            return {"avg": 0, "max": 0, "per_function": 0}
        
        return {
            "avg": round(sum(complexities) / len(complexities), 2),
            "max": max(complexities),
            "per_function": len(complexities)
        }
    except Exception as e:
        return {"avg": None, "max": None, "per_function": 0, "error": str(e)}


def get_loc(filepath: str) -> dict:
    """Возвращает количество строк кода."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "radon", "raw", filepath],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode != 0:
            return {"total_loc": None, "error": result.stderr}
        
        for line in result.stdout.split("\n"):
            if "LOC:" in line:
                loc = int(line.split("LOC:")[1].strip())
                return {"total_loc": loc}
        
        return {"total_loc": None, "error": "Не удалось извлечь LOC"}
    except Exception as e:
        return {"total_loc": None, "error": str(e)}


def get_flake8_warnings(filepath: str) -> dict:
    """Возвращает количество предупреждений flake8."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "flake8", filepath, "--max-line-length=120"],
            capture_output=True, text=True, timeout=10
        )
        warnings = [l for l in result.stdout.strip().split("\n") if l]
        return {
            "count": len(warnings),
            "warnings": warnings if len(warnings) <= 10 else warnings[:10] + [f"... и ещё {len(warnings) - 10}"]
        }
    except Exception as e:
        return {"count": None, "error": str(e)}


def get_pylint_issues(filepath: str) -> dict:
    """Возвращает количество замечаний pylint."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pylint", filepath, "--output-format=json"],
            capture_output=True, text=True, timeout=30
        )
        if not result.stdout.strip():
            return {"count": 0, "issues": []}
        
        data = json.loads(result.stdout)
        return {
            "count": len(data),
            "issues": [
                {
                    "type": issue.get("type", ""),
                    "message": issue.get("message", ""),
                    "line": issue.get("line", 0)
                }
                for issue in data[:10]
            ]
        }
    except Exception as e:
        return {"count": None, "error": str(e)}


def analyze_file(filepath: str) -> dict:
    """Анализирует один файл."""
    return {
        "file": str(Path(filepath).resolve()),
        "complexity": get_complexity(filepath),
        "loc": get_loc(filepath),
        "flake8": get_flake8_warnings(filepath),
        "pylint": get_pylint_issues(filepath),
    }


def analyze_directory(dirpath: str) -> dict:
    """
    Анализирует все .py файлы в папке.
    Возвращает агрегированные метрики.
    """
    dirpath = Path(dirpath)
    py_files = list(dirpath.glob("*.py"))
    
    if not py_files:
        print(f"В папке {dirpath} нет .py файлов")
        return {}
    
    results = []
    total_loc = 0
    all_complexities = []
    total_flake8 = 0
    total_pylint = 0
    
    print(f"Папка: {dirpath}")
    print(f"Найдено файлов: {len(py_files)}")
    print(f"{'='*60}")
    
    for py_file in sorted(py_files):
        print(f"\nФайл: {py_file.name}")
        print(f"{'-'*40}")
        
        metrics = analyze_file(str(py_file))
        results.append(metrics)
        
        loc = metrics["loc"].get("total_loc", 0) or 0
        total_loc += loc
        
        if metrics["complexity"].get("avg") is not None:
            all_complexities.append(metrics["complexity"]["avg"])
        
        total_flake8 += metrics["flake8"].get("count", 0) or 0
        total_pylint += metrics["pylint"].get("count", 0) or 0
        
        print(f"  Сложность: средняя {metrics['complexity'].get('avg', 'N/A')}, макс {metrics['complexity'].get('max', 'N/A')}")
        print(f"  LOC: {loc}")
        print(f"  flake8: {metrics['flake8'].get('count', 'N/A')}")
        print(f"  pylint: {metrics['pylint'].get('count', 'N/A')}")
    
    # Агрегация
    avg_complexity = round(sum(all_complexities) / len(all_complexities), 2) if all_complexities else None
    max_complexity = max((r["complexity"].get("max", 0) or 0) for r in results) if results else None
    
    print(f"\n{'='*60}")
    print(f"ИТОГО по папке:")
    print(f"  Файлов: {len(py_files)}")
    print(f"  Суммарно LOC: {total_loc}")
    print(f"  Средняя сложность: {avg_complexity}")
    print(f"  Максимальная сложность: {max_complexity}")
    print(f"  Всего flake8: {total_flake8}")
    print(f"  Всего pylint: {total_pylint}")
    
    return {
        "directory": str(dirpath),
        "files_count": len(py_files),
        "total_loc": total_loc,
        "avg_complexity": avg_complexity,
        "max_complexity": max_complexity,
        "total_flake8": total_flake8,
        "total_pylint": total_pylint,
        "per_file": results,
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python metrics.py <файл_или_папка>")
        print("Примеры:")
        print("  python metrics.py black_tests/llm_solution/solution.py")
        print("  python metrics.py black_tests/friend_solution/")
        sys.exit(1)
    
    path = sys.argv[1]
    path_obj = Path(path)
    
    if not path_obj.exists():
        print(f"Путь {path} не найден")
        sys.exit(1)
    
    if path_obj.is_dir():
        analyze_directory(path)
    else:
        metrics = analyze_file(path)
        print(f"\nФайл: {metrics['file']}")
        print(f"{'='*60}")
        print(f"Цикломатическая сложность:")
        print(f"  Средняя: {metrics['complexity'].get('avg', 'N/A')}")
        print(f"  Максимальная: {metrics['complexity'].get('max', 'N/A')}")
        print(f"  Функций: {metrics['complexity'].get('per_function', 'N/A')}")
        print(f"Строк кода (LOC): {metrics['loc'].get('total_loc', 'N/A')}")
        print(f"Предупреждений flake8: {metrics['flake8'].get('count', 'N/A')}")
        print(f"Замечаний pylint: {metrics['pylint'].get('count', 'N/A')}")