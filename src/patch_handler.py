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
    def apply(patch_content: str, target_file: Path) -> bool:
        """
        Применяет патч к файлу с помощью библиотеки unidiff.
        
        Args:
            patch_content: содержимое патча
            target_file: путь к файлу, который нужно изменить
            
        Returns:
            True, если патч успешно применён
        """
        if not patch_content.strip():
            return True
            
        # Читаем оригинальный файл
        original_lines = target_file.read_text(encoding="utf-8").splitlines(True)
        
        # Парсим патч
        try:
            patch = PatchSet.from_string(patch_content)
        except UnidiffParseError as e:
            raise RuntimeError(
                f"Некорректный формат патча: {e}. "
                "Пожалуйста, перегенерируй патч с правильными заголовками ханков."
    )
        
        # Применяем изменения к строкам
        patched_lines = apply_patch_to_lines(original_lines, patch[0])
        
        # Записываем результат
        target_file.write_text("".join(patched_lines), encoding="utf-8")
        return True


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