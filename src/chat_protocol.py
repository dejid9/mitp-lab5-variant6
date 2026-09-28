"""Модуль форматирования сообщений и протокола локального чата."""

from datetime import datetime


def format_chat_message(sender: str, message: str) -> str:
    """Форматирует сообщение чата с указанием временной метки.

    Параметры:
        sender (str): Имя отправителя.
        message (str): Текст сообщения.

    Возвращает:
        str: Форматированная строка сообщения.
    """
    clean_sender = sender.strip() or "Аноним"
    clean_msg = message.strip()
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"[{timestamp}] {clean_sender}: {clean_msg}"


def parse_chat_message(formatted_line: str) -> tuple[str, str, str]:
    """Разбирает форматированную строку чата на (timestamp, sender, message)."""
    if not (formatted_line.startswith("[") and "] " in formatted_line):
        return "", "", formatted_line

    time_part, rest = formatted_line.split("] ", 1)
    timestamp = time_part.lstrip("[")
    if ": " in rest:
        sender, msg = rest.split(": ", 1)
    else:
        sender, msg = "Система", rest
    return timestamp, sender, msg
