import pytest
from string_utils import StringUtils

string_utils = StringUtils()

# Позитивные сценарии


def test_positive_string_with_text():
    """Проверка непустой строки с текстом"""
    assert string_utils.capitalize("Тест") == "Тест"


def test_capitalize_positive_text():
    """Проверка заглавной буквы в текстовой строке"""
    assert string_utils.capitalize("привет") == "Привет"


def test_positive_string_with_numbers():
    """Проверка строки с числами"""
    assert string_utils.capitalize("123") == "123"


def test_positive_string_with_spaces():
    """Проверка строки с пробелами"""
    assert string_utils.trim("04 апреля 2023") == "04 апреля 2023"


def test_trim_positive_tabs():
    """Проверка обрезки табуляции"""
    assert string_utils.trim("\tтекст\t") == "текст"


def test_delete_symbol_positive_single_char():
    """Удаление одного символа"""
    assert string_utils.delete_symbol("SkyPro", "k") == "SyPro"


def test_contains_positive_true():
    """Проверка: символ присутствует в строке"""
    assert string_utils.contains("SkyPro", "S") is True

# Негативные сценарии


def test_negative_empty_string():
    """Проверка пустой строки"""
    assert string_utils.capitalize("") == ""


def test_negative_string_with_space():
    """Проверка строки с пробелом"""
    assert string_utils.trim(" ") == " "


def test_trim_negative_only_spaces():
    """Проверка строки из пробелов"""
    assert string_utils.trim("    ") == ""


def test_negative_none_value():
    """Проверка передачи None"""
    with pytest.raises(TypeError):
        string_utils.capitalize(None)


def test_delete_symbol_negative_not_found():
    """Проверка: если символа нет, строка не изменяется"""
    assert string_utils.delete_symbol("SkyPro", "X") == "SkyPro"


def test_contains_negative_empty_string():
    """Проверка: пустая строка всегда возвращает False"""
    assert string_utils.contains("", "a") is False
