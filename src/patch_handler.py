"""
Обработчик unified diff патчей.
Извлекает патч из ответа LLM и применяет его к файлам.
"""

import re
from pathlib import Path
from unidiff import PatchSet
from unidiff.errors import UnidiffParseError


class PatchHandler:
    """
    Обрабатывает unified diff патчи от LLM.
    
    Использование:
        handler = PatchHandler()
        clean_patch = handler.extract(response_text)
        success = handler.apply(clean_patch, target_file)
    """

    @staticmethod
    def extract(response_text: str) -> str:
        """
        Извлекает чистый патч из ответа LLM.
        Модель может обернуть патч в ```diff ... ``` или ```python ... ```.
        """
        text = response_text.strip()
        match = re.search(r"```(?:diff)?\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text
    
    @staticmethod
    def _remove_git_headers(patch_content: str) -> str:
        """Удаляет гитовские заголовки (diff --git, new file mode, index и т.д.)"""
        lines = patch_content.splitlines(True)
        fixed = []
        for line in lines:
            if line.startswith((
                "diff --git", "index ", "new file mode", "deleted file mode",
                "old mode", "new mode", "similarity index",
                "rename from", "rename to", "Binary files"
            )):
                continue
            fixed.append(line)
        return "".join(fixed)
    
    @staticmethod
    def _fix_git_prefixes(patch_content: str) -> str:
        """Убирает префиксы a/ и b/ из путей в заголовках --- и +++"""
        lines = patch_content.splitlines(True)
        fixed = []
        for line in lines:
            if line.startswith("--- a/"):
                fixed.append("--- " + line[6:])
            elif line.startswith("+++ b/"):
                fixed.append("+++ " + line[6:])
            else:
                fixed.append(line)
        return "".join(fixed)
    
    @staticmethod
    def _fix_missing_header(patch_content: str) -> str:
        """Если патч создаёт/изменяет файл, но нет ---, добавляет заглушку."""
        lines = patch_content.splitlines(True)
        has_old = any(line.startswith("--- ") for line in lines)
        has_new = any(line.startswith("+++ ") for line in lines)

        if not has_old and has_new:
            fixed = []
            for line in lines:
                if line.startswith("+++ "):
                    fixed.append("--- /dev/null\n")
                fixed.append(line)
            return "".join(fixed)
        return patch_content
    
    @staticmethod
    def _fix_hunk_headers(patch_content: str) -> str:
        """Исправляет заголовки ханков с неправильным количеством строк."""
        lines = patch_content.splitlines(True)
        result = []
        i = 0

        while i < len(lines):
            line = lines[i]
            match = re.match(r'^@@ -(\d+),?(\d+)? \+(\d+),?(\d+)? @@', line)
            if match:
                hunk_lines = []
                i += 1
                while i < len(lines) and not lines[i].startswith(("@@", "---", "+++", "diff ")):
                    hunk_lines.append(lines[i])
                    i += 1

                real_removed = sum(1 for l in hunk_lines if l.startswith("-"))
                real_added = sum(1 for l in hunk_lines if l.startswith("+"))
                old_start = int(match.group(1))
                new_start = int(match.group(3))

                fixed_header = f"@@ -{old_start},{real_removed} +{new_start},{real_added} @@\n"
                result.append(fixed_header)
                result.extend(hunk_lines)
            else:
                result.append(line)
                i += 1

        return "".join(result)

    @staticmethod
    def apply(patch_content: str, target_file: Path) -> bool:
        if not patch_content.strip():
            return True

        # Последовательно исправляем типичные ошибки формата
        patch_content = PatchHandler._remove_git_headers(patch_content)
        patch_content = PatchHandler._fix_git_prefixes(patch_content)
        patch_content = PatchHandler._fix_missing_header(patch_content)
        patch_content = PatchHandler._fix_hunk_headers(patch_content)

        try:
            patch = PatchSet.from_string(patch_content)
        except UnidiffParseError as e:
            raise RuntimeError(
                f"Некорректный формат патча: {e}. "
                "Пожалуйста, перегенерируй патч с правильными заголовками ханков."
            )

        if len(patch) == 0:
            raise RuntimeError("Патч не содержит изменений. Перегенерируй патч.")

        original_lines = target_file.read_text(encoding="utf-8").splitlines(True)

        try:
            patched_lines = _apply_patchset(original_lines, patch[0])
        except Exception as e:
            raise RuntimeError(
                f"Не удалось применить патч: {e}. "
                "Возможно, контекстные строки не совпадают с текущим кодом. "
                "Убедись, что патч соответствует актуальной версии solution.py, и перегенерируй его."
            )

        target_file.write_text("".join(patched_lines), encoding="utf-8")
        return True
    
def _apply_patchset(original_lines, patched_file):
    """Применяет один PatchedFile к списку строк."""
    result = []
    original_idx = 0

    for hunk in patched_file:
        while original_idx < hunk.source_start - 1:
            if original_idx < len(original_lines):
                result.append(original_lines[original_idx])
            original_idx += 1

        for line in hunk:
            if line.is_added:
                result.append(line.value)
            elif line.is_removed:
                if original_idx < len(original_lines):
                    original_idx += 1
            elif line.is_context:
                if original_idx < len(original_lines):
                    result.append(original_lines[original_idx])
                original_idx += 1

    while original_idx < len(original_lines):
        result.append(original_lines[original_idx])
        original_idx += 1

    return result


def apply_patch_to_lines(original_lines, patched_file):
    """
    Применяет один PatchedFile к списку строк.
    """
    result = []
    original_idx = 0
    
    for hunk in patched_file:
        # Добавляем строки до начала ханка
        while original_idx < hunk.source_start - 1:
            if original_idx < len(original_lines):
                result.append(original_lines[original_idx])
            original_idx += 1
            
        # Применяем ханк
        for line in hunk:
            if line.is_added:
                result.append(line.value)
            elif line.is_removed:
                if original_idx < len(original_lines):
                    original_idx += 1
            elif line.is_context:
                if original_idx < len(original_lines):
                    result.append(original_lines[original_idx])
                original_idx += 1
                
    # Добавляем оставшиеся строки
    while original_idx < len(original_lines):
        result.append(original_lines[original_idx])
        original_idx += 1
        
    return result