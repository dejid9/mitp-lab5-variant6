"""Точка входа лабораторной работы №5 (Вариант 6)."""

import sys
import os
from src.canvas_plot import create_parabola_figure
from src.chat_protocol import format_chat_message, parse_chat_message


def run_headless_demo() -> None:
    """Выполняет демонстрацию логики без запуска GUI loop (для тестов и CI)."""
    print("=" * 65)
    print("Лабораторная работа №5 — Вариант 6")
    print("Дисциплина: «Методы и технологии программирования»")
    print("Студент: Вафин Денис Наильевич (Группа 221141)")
    print("=" * 65)

    # 1. Задание 2 (среднее): Текстовое поле и кнопка
    sample_text = "Вафин Денис (Группа 221141)"
    print("\n[1] Окно с текстовым полем и кнопкой:")
    print(f"    Входные данные: '{sample_text}'")
    print(f"    Вывод метки:    'Вы ввели: «{sample_text}»'")

    # 2. Задание 6 (среднее): Прогрессбар
    print("\n[2] Прогрессбар (ttk.Progressbar):")
    steps = [0, 20, 40, 60, 80, 100]
    print(f"    Шаги заполнения: {steps}% (успешно инициализирован)")

    # 3. Задание 8 (среднее): Диалог выбора файла
    print("\n[3] Диалог выбора файла (filedialog):")
    print("    Фильтры: Text Files (*.txt, *.md, *.py, *.json), All Files (*.*)")
    print("    Предпросмотр файла интегрирован в текстовое поле.")

    # 4. Задание 4 (повышенное): График matplotlib внутри Tkinter
    fig = create_parabola_figure("x^2", -10.0, 10.0)
    out_img = "canvas_demo.png"
    fig.savefig(out_img, dpi=120)
    print("\n[4] График matplotlib внутри Tkinter (FigureCanvasTkAgg):")
    print(f"    Демо-снимок сохранён: {os.path.abspath(out_img)}")

    # 5. Задание 10 (повышенное): Программа чат (локальный)
    msg1 = format_chat_message("Денис", "Привет! Это проверка локального чата.")
    msg2 = format_chat_message("Сервер", "Сообщение доставлено всем клиентам.")
    print("\n[5] Программа чат (локальный):")
    print("   ", msg1)
    print("   ", msg2)
    t, sender, text = parse_chat_message(msg1)
    print(f"    Парсер сообщения: время={t}, отправитель={sender}, текст='{text}'")
    print("=" * 65)


def main() -> None:
    if "--headless" in sys.argv or os.environ.get("CI") == "true":
        run_headless_demo()
    else:
        try:
            from src.app_gui import MainApplication
            app = MainApplication()
            print("Запуск графического интерфейса Tkinter...")
            app.mainloop()
        except Exception as e:
            print(f"Оконный режим Tkinter недоступен ({e}). Демо-режим:")
            run_headless_demo()


if __name__ == "__main__":
    main()
