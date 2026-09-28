"""Модуль интеграции графиков matplotlib для Tkinter FigureCanvasTkAgg."""

import matplotlib
matplotlib.use("Agg")
from matplotlib.figure import Figure  # noqa: E402
import numpy as np  # noqa: E402


def create_parabola_figure(
    func_type: str = "x^2",
    x_min: float = -10.0,
    x_max: float = 10.0
) -> Figure:
    """Создаёт объект Figure matplotlib для встраивания в Tkinter.

    Поддерживает квадратичную параболу y=x^2, синус y=sin(x) и кубическую функцию.
    """
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)

    x = np.linspace(x_min, x_max, 400)
    if func_type == "x^2":
        y = x ** 2
        label = "$y = x^2$"
        title = "Квадратичная функция $y = x^2$"
    elif func_type == "sin(x)":
        y = np.sin(x)
        label = "$y = \\sin(x)$"
        title = "Тригонометрическая функция $y = \\sin(x)$"
    else:
        y = x ** 3
        label = "$y = x^3$"
        title = "Кубическая функция $y = x^3$"

    ax.plot(x, y, label=label, color="#1f77b4", linewidth=2.0)
    ax.set_title(title, fontsize=12, fontweight="bold")
    ax.set_xlabel("Ось X", fontsize=10)
    ax.set_ylabel("Ось Y", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.7)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.legend(loc="best")
    fig.tight_layout()
    return fig
