import logging
import random
import string
from django.core.cache import cache

logger = logging.getLogger(__name__)


def generate_invite_code(length: int = 6) -> str:
    """
    Генерирует случайный код приглашения, состоящий из букв и цифр.

    Аргументы:
        length (int): Длина генерируемого кода приглашения. По умолчанию 6.

    Возвращает:
        str: Случайно сгенерированный код приглашения.
    """
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_verify_code(*args, **kwargs) -> int:
    """
    Генерирует случайный код для проверки, состоящий из 4 цифр.

    Аргументы:
        *args: Дополнительные позиционные аргументы (не используются).
        **kwargs: Дополнительные именованные аргументы (не используются).

    Возвращает:
        int: Случайно сгенерированный 4-значный код проверки.
    """
    return random.randint(1000, 9999)


def temp_stor_for_codes(phone_number: str, code: int | bool = None, process="add") -> int | bool:
    """
    Управляет временным хранилищем кодов в кэше для целей аутентификации.

    Аргументы:
        phone_number (str): Номер телефона, связанный с кодом.
        code (int | bool): Код, который нужно сохранить, получить или удалить. По умолчанию None.
        process (str): Действие, которое нужно выполнить:
            - "add": Сохранить код в кэше.
            - "get": Получить код из кэша.
            - "remove": Удалить код из кэша.
          По умолчанию "add".

    Возвращает:
        int | bool:
            - При `process="get"` возвращает сохранённый код или None, если код не найден.
            - При `process="add"` или `process="remove"` возвращает True.
    """
    if process == "add":
        # Сохранение кода в кэше с таймаутом 1 час (3600 секунд).
        cache.set(f"auth_code_{phone_number}", code, timeout=3600)
    elif process == "get":
        # Получение кода из кэша.
        return cache.get(f"auth_code_{phone_number}")
    elif process == "remove":
        # Удаление кода из кэша.
        cache.delete(f"auth_code_{phone_number}")
    return True

