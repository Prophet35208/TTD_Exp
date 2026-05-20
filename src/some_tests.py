"""
Тесты для PatchHandler.
Проверяет все методы автоматической коррекции патчей.
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from patch_handler import PatchHandler


def test_extract_markdown():
    """Проверяет удаление markdown-обёртки."""
    handler = PatchHandler()
    
    input_text = """```diff
--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass
```"""
    result = handler.extract(input_text)
    assert "```" not in result
    assert "def hello():" in result
    print("✅ test_extract_markdown")


def test_extract_no_markdown():
    """Проверяет, что патч без markdown не меняется."""
    handler = PatchHandler()
    
    input_text = """--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass"""
    result = handler.extract(input_text)
    assert result == input_text.strip()
    print("✅ test_extract_no_markdown")


def test_remove_git_headers():
    """Проверяет удаление diff --git, new file mode, index."""
    patch = """diff --git a/solution.py b/solution.py
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass"""
    result = PatchHandler._remove_git_headers(patch)
    assert "diff --git" not in result
    assert "new file mode" not in result
    assert "index " not in result
    assert "--- /dev/null" in result
    print("✅ test_remove_git_headers")


def test_fix_git_prefixes():
    """Проверяет удаление префиксов a/ и b/."""
    patch = """--- a/solution.py
+++ b/solution.py
@@ -1,3 +1,4 @@
 def hello():
     pass
+    return True"""
    result = PatchHandler._fix_git_prefixes(patch)
    assert "a/solution.py" not in result
    assert "b/solution.py" not in result
    assert "--- solution.py" in result
    assert "+++ solution.py" in result
    print("✅ test_fix_git_prefixes")


def test_fix_missing_header():
    """Проверяет добавление --- /dev/null при отсутствии."""
    # Патч без ---
    patch = """+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass"""
    result = PatchHandler._fix_missing_header(patch)
    assert result.startswith("--- /dev/null\n")
    assert "+++ solution.py" in result
    print("✅ test_fix_missing_header")


def test_fix_missing_header_already_exists():
    """Проверяет, что существующий --- не дублируется."""
    patch = """--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass"""
    result = PatchHandler._fix_missing_header(patch)
    # Должен остаться без изменений
    assert result.count("--- /dev/null") == 1
    print("✅ test_fix_missing_header_already_exists")


def test_fix_hunk_headers_longer():
    """Проверяет исправление заголовка, где строк больше заявленного."""
    # Заявлено 3 строки, а по факту 4
    patch = """--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass
+    return True
+"""
    result = PatchHandler._fix_hunk_headers(patch)
    assert "@@ -0,0 +1,4 @@" in result
    print("✅ test_fix_hunk_headers_longer")


def test_fix_hunk_headers_shorter():
    """Проверяет исправление заголовка, где строк меньше заявленного."""
    # Заявлено 5 строк, а по факту 3
    patch = """--- /dev/null
+++ solution.py
@@ -0,0 +1,5 @@
+def hello():
+    pass
+    return True
"""
    result = PatchHandler._fix_hunk_headers(patch)
    assert "@@ -0,0 +1,3 @@" in result
    print("✅ test_fix_hunk_headers_shorter")


def test_fix_hunk_headers_correct():
    """Проверяет, что правильный заголовок не меняется."""
    patch = """--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def hello():
+    pass
+    return True"""
    result = PatchHandler._fix_hunk_headers(patch)
    assert "@@ -0,0 +1,3 @@" in result
    print("✅ test_fix_hunk_headers_correct")


def test_fix_hunk_headers_multiple_hunks():
    """Проверяет исправление нескольких ханков в одном патче."""
    patch = """--- solution.py
+++ solution.py
@@ -1,2 +1,2 @@
-def hello():
+def greet():
     pass
@@ -5,1 +5,2 @@
     return True
+    print("ok")
"""
    result = PatchHandler._fix_hunk_headers(patch)
    assert "@@ -1,1 +1,1 @@" in result   # 1 удалена, 1 добавлена
    assert "@@ -5,0 +5,1 @@" in result   # 0 удалено, 1 добавлена
    print("✅ test_fix_hunk_headers_multiple_hunks")


def test_apply_patch_creates_new_file():
    """Проверяет применение патча к пустому файлу."""
    handler = PatchHandler()
    
    patch = """--- /dev/null
+++ solution.py
@@ -0,0 +1,3 @@
+def calculate(a, b):
+    return a + b
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "solution.py"
        target.write_text("")
        
        handler.apply(patch, target)
        content = target.read_text()
        
        assert "def calculate(a, b):" in content
        assert "return a + b" in content
        print("✅ test_apply_patch_creates_new_file")


def test_apply_patch_modifies_existing_file():
    """Проверяет применение патча к существующему файлу."""
    handler = PatchHandler()
    
    original = """def calculate(a, b):
    return a + b
"""
    patch = """--- solution.py
+++ solution.py
@@ -1,2 +1,3 @@
-def calculate(a, b):
-    return a + b
+def calculate(a, b):
+    return a + b
+# new comment
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "solution.py"
        target.write_text(original)
        
        handler.apply(patch, target)
        content = target.read_text()
        
        assert "# new comment" in content, f"Ожидался '# new comment', но файл:\n{content}"
        print("✅ test_apply_patch_modifies_existing_file")


def test_apply_empty_patch():
    """Проверяет, что пустой патч не вызывает ошибок."""
    handler = PatchHandler()
    
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "solution.py"
        target.write_text("original")
        
        result = handler.apply("", target)
        assert result is True
        print("✅ test_apply_empty_patch")


def test_apply_patch_with_all_fixes():
    """Проверяет комплексное применение: патч с гитовскими заголовками, a/b префиксами, неверным ханком."""
    handler = PatchHandler()
    
    # Реальный патч от Llama 3.3 Nemotron
    patch = """diff --git a/solution.py b/solution.py
new file mode 100644
--- /dev/null
+++ b/solution.py
@@ -0,0 +1,34 @@
+def calculate(notation, expression):
+    tokens = expression.split()
+    stack = []
+    
+    if notation == 'prefix':
+        tokens = tokens[::-1]
+        for token in tokens:
+            if token in ['+', '-']:
+                a = stack.pop()
+                b = stack.pop()
+                if token == '+':
+                    res = a + b
+                else:
+                    res = a - b
+                stack.append(res)
+            else:
+                stack.append(float(token))
+    elif notation == 'postfix':
+        for token in tokens:
+            if token in ['+', '-']:
+                b = stack.pop()
+                a = stack.pop()
+                if token == '+':
+                    res = a + b
+                else:
+                    res = a - b
+                stack.append(res)
+            else:
+                stack.append(float(token))
+    else:
+        raise ValueError("Unknown notation")
+    
+    result = stack[0]
+    return int(result) if result.is_integer() else result
"""
    
    with tempfile.TemporaryDirectory() as tmpdir:
        target = Path(tmpdir) / "solution.py"
        target.write_text("")
        
        handler.apply(patch, target)
        content = target.read_text()
        
        assert "def calculate(notation, expression):" in content
        assert "float(token)" in content
        assert "is_integer()" in content
        print("✅ test_apply_patch_with_all_fixes")


if __name__ == "__main__":
    print("=" * 60)
    print("ТЕСТЫ PatchHandler")
    print("=" * 60)
    
    # Тесты extract
    test_extract_markdown()
    test_extract_no_markdown()
    
    # Тесты исправлений
    test_remove_git_headers()
    test_fix_git_prefixes()
    test_fix_missing_header()
    test_fix_missing_header_already_exists()
    
    # Тесты ханков
    test_fix_hunk_headers_longer()
    test_fix_hunk_headers_shorter()
    test_fix_hunk_headers_correct()
    test_fix_hunk_headers_multiple_hunks()
    
    # Тесты apply
    test_apply_empty_patch()
    test_apply_patch_creates_new_file()
    test_apply_patch_modifies_existing_file()
    test_apply_patch_with_all_fixes()
    
    print("\n" + "=" * 60)
    print("ВСЕ ТЕСТЫ ПРОЙДЕНЫ!")
    print("=" * 60)