"""Главный модуль GUI на Tkinter, объединяющий задания варианта 6."""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.canvas_plot import create_parabola_figure
from src.chat_protocol import format_chat_message

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_CANVAS_AVAILABLE = True
except ImportError:
    MATPLOTLIB_CANVAS_AVAILABLE = False


class MainApplication(tk.Tk):
    """Главное графическое окно со всеми заданиями варианта 6."""

    def __init__(self) -> None:
        super().__init__()
        self.title("МИТП — Лабораторная работа №5 (Вариант 6)")
        self.geometry("820x620")
        self.minsize(700, 500)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка 1: Текстовое поле, кнопка, прогрессбар, выбор файла
        tab_base = ttk.Frame(notebook)
        notebook.add(tab_base, text="1. Базовые элементы и файлы")
        self._build_base_tab(tab_base)

        # Вкладка 2: График Matplotlib внутри Tkinter
        tab_plot = ttk.Frame(notebook)
        notebook.add(tab_plot, text="2. График Matplotlib в Tkinter")
        self._build_plot_tab(tab_plot)

        # Вкладка 3: Локальный чат
        tab_chat = ttk.Frame(notebook)
        notebook.add(tab_chat, text="3. Локальный чат")
        self._build_chat_tab(tab_chat)

    def _build_base_tab(self, parent: ttk.Frame) -> None:
        # Задание 2: Текстовое поле и кнопка
        frame_input = ttk.LabelFrame(
            parent, text="Задание 2: Текстовое поле и кнопка вывода", padding=10
        )
        frame_input.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(frame_input, text="Введите ваше имя или текст:").pack(
            anchor=tk.W, pady=2
        )
        self.entry_text = ttk.Entry(frame_input, width=45)
        self.entry_text.insert(0, "Вафин Денис (Группа 221141)")
        self.entry_text.pack(side=tk.LEFT, padx=5, pady=5)

        btn_show = ttk.Button(
            frame_input, text="Вывести текст", command=self._on_show_text
        )
        btn_show.pack(side=tk.LEFT, padx=5, pady=5)

        self.lbl_result = ttk.Label(
            frame_input, text="[Результат вывода появится здесь]", foreground="navy"
        )
        self.lbl_result.pack(side=tk.LEFT, padx=10, pady=5)

        # Задание 6: Прогрессбар
        frame_progress = ttk.LabelFrame(
            parent, text="Задание 6: Прогрессбар", padding=10
        )
        frame_progress.pack(fill=tk.X, padx=10, pady=5)

        self.progressbar = ttk.Progressbar(
            frame_progress, orient=tk.HORIZONTAL, length=400, mode="determinate"
        )
        self.progressbar.pack(fill=tk.X, pady=5)

        btn_box = ttk.Frame(frame_progress)
        btn_box.pack(fill=tk.X)
        ttk.Button(
            btn_box, text="+20% Шаг", command=self._step_progress
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_box, text="Запустить анимацию", command=self._animate_progress
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_box, text="Сброс", command=self._reset_progress
        ).pack(side=tk.LEFT, padx=5)
        self.lbl_progress = ttk.Label(btn_box, text="Текущий прогресс: 0%")
        self.lbl_progress.pack(side=tk.LEFT, padx=15)

        # Задание 8: Диалог выбора файла
        frame_file = ttk.LabelFrame(
            parent, text="Задание 8: Диалог выбора файла", padding=10
        )
        frame_file.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        file_ctrl = ttk.Frame(frame_file)
        file_ctrl.pack(fill=tk.X, pady=2)
        ttk.Button(
            file_ctrl, text="Открыть файл...", command=self._on_choose_file
        ).pack(side=tk.LEFT, padx=5)
        self.lbl_file_path = ttk.Label(
            file_ctrl, text="Файл не выбран", foreground="dimgray"
        )
        self.lbl_file_path.pack(side=tk.LEFT, padx=10)

        self.txt_file_preview = tk.Text(frame_file, height=8, wrap=tk.WORD)
        self.txt_file_preview.pack(fill=tk.BOTH, expand=True, pady=5)

    def _on_show_text(self) -> None:
        user_text = self.entry_text.get().strip()
        if user_text:
            self.lbl_result.config(text=f"Вы ввели: «{user_text}»")
        else:
            self.lbl_result.config(text="Поле ввода пусто!")

    def _step_progress(self) -> None:
        cur = self.progressbar["value"] + 20
        if cur > 100:
            cur = 100
        self.progressbar["value"] = cur
        self.lbl_progress.config(text=f"Текущий прогресс: {int(cur)}%")

    def _reset_progress(self) -> None:
        self.progressbar["value"] = 0
        self.lbl_progress.config(text="Текущий прогресс: 0%")

    def _animate_progress(self) -> None:
        def step():
            if self.progressbar["value"] < 100:
                self.progressbar["value"] += 5
                self.lbl_progress.config(
                    text=f"Текущий прогресс: {int(self.progressbar['value'])}%"
                )
                self.after(50, step)
        self._reset_progress()
        step()

    def _on_choose_file(self) -> None:
        chosen = filedialog.askopenfilename(
            title="Выберите текстовый файл",
            filetypes=[("Text Files", "*.txt *.md *.py *.json"), ("All Files", "*.*")]
        )
        if chosen:
            self.lbl_file_path.config(text=chosen)
            try:
                with open(chosen, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read(2048)
                self.txt_file_preview.delete("1.0", tk.END)
                self.txt_file_preview.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")

    def _build_plot_tab(self, parent: ttk.Frame) -> None:
        ctrl = ttk.Frame(parent, padding=5)
        ctrl.pack(fill=tk.X)

        ttk.Label(ctrl, text="Функция:").pack(side=tk.LEFT, padx=5)
        self.combo_func = ttk.Combobox(
            ctrl, values=["x^2", "sin(x)", "x^3"], state="readonly", width=10
        )
        self.combo_func.set("x^2")
        self.combo_func.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            ctrl, text="Построить / Обновить график", command=self._refresh_plot
        ).pack(side=tk.LEFT, padx=10)

        self.plot_container = ttk.Frame(parent)
        self.plot_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas_widget = None
        self._refresh_plot()

    def _refresh_plot(self) -> None:
        if not MATPLOTLIB_CANVAS_AVAILABLE:
            ttk.Label(
                self.plot_container, text="Matplotlib FigureCanvasTkAgg недоступен"
            ).pack()
            return

        fig = create_parabola_figure(func_type=self.combo_func.get())
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.plot_container)
        self.canvas_widget.draw()
        self.canvas_widget.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _build_chat_tab(self, parent: ttk.Frame) -> None:
        frame_chat = ttk.LabelFrame(
            parent, text="Локальный чат (Задание 10)", padding=10
        )
        frame_chat.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        top_bar = ttk.Frame(frame_chat)
        top_bar.pack(fill=tk.X, pady=2)
        ttk.Label(top_bar, text="Псевдоним:").pack(side=tk.LEFT, padx=5)
        self.entry_nickname = ttk.Entry(top_bar, width=20)
        self.entry_nickname.insert(0, "Денис (Вар.6)")
        self.entry_nickname.pack(side=tk.LEFT, padx=5)

        self.chat_history = tk.Text(frame_chat, height=14, wrap=tk.WORD)
        self.chat_history.pack(fill=tk.BOTH, expand=True, pady=5)

        bot_bar = ttk.Frame(frame_chat)
        bot_bar.pack(fill=tk.X, pady=5)
        self.entry_msg = ttk.Entry(bot_bar, width=50)
        self.entry_msg.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_msg.bind("<Return>", lambda e: self._send_chat_message())

        ttk.Button(
            bot_bar, text="Отправить", command=self._send_chat_message
        ).pack(side=tk.RIGHT, padx=5)

        # Welcome message
        self.chat_history.insert(
            tk.END,
            "[Система]: Добро пожаловать в локальный чат лабораторной работы №5!\n"
        )

    def _send_chat_message(self) -> None:
        msg = self.entry_msg.get().strip()
        if not msg:
            return
        nick = self.entry_nickname.get().strip() or "Аноним"
        formatted = format_chat_message(nick, msg)
        self.chat_history.insert(tk.END, formatted + "\n")
        self.chat_history.see(tk.END)
        self.entry_msg.delete(0, tk.END)
