"""Модульные тесты pytest для компонентов лабораторной работы №5."""

from src.chat_protocol import format_chat_message, parse_chat_message
from src.canvas_plot import create_parabola_figure


class TestChatProtocol:
    def test_format_message(self):
        msg = format_chat_message("Денис", "Тестовое сообщение")
        assert "Денис: Тестовое сообщение" in msg
        assert msg.startswith("[")

    def test_anonymous_sender(self):
        msg = format_chat_message("   ", "Привет")
        assert "Аноним: Привет" in msg

    def test_parse_message(self):
        formatted = "[12:30:45] Студент: Готово!"
        timestamp, sender, text = parse_chat_message(formatted)
        assert timestamp == "12:30:45"
        assert sender == "Студент"
        assert text == "Готово!"


class TestCanvasPlot:
    def test_parabola_figure(self):
        fig = create_parabola_figure("x^2", -5.0, 5.0)
        assert fig is not None
        assert len(fig.axes) == 1
        ax = fig.axes[0]
        assert "x^2" in ax.get_title()

    def test_trigonometric_figure(self):
        fig = create_parabola_figure("sin(x)", -3.14, 3.14)
        ax = fig.axes[0]
        assert "sin(x)" in ax.get_title()
