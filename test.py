import tkinter as tk
from tkinter import messagebox
import math

class EngineeringCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🧮 Инженерный калькулятор")
        self.root.geometry("420x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#141414")

        # Переменные
        self.expression = ""
        self.input_text = tk.StringVar()
        self.history_text = tk.StringVar()
        self.memory = 0

        # Флаг для градусов/радиан
        self.use_degrees = True

        # Создание интерфейса
        self.create_display()
        self.create_buttons()
        self.create_history()

        # Привязка клавиатуры
        self.root.bind("<Key>", self.key_press)

    # ===== ДИСПЛЕЙ =====
    def create_display(self):
        # История (мелкий текст сверху)
        history_frame = tk.Frame(self.root, bg="#1e1e1e", height=30)
        history_frame.pack(fill="x", padx=10, pady=(10, 0))
        history_frame.pack_propagate(False)

        history_label = tk.Label(
            history_frame,
            textvariable=self.history_text,
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#8888aa",
            anchor="e"
        )
        history_label.pack(fill="both", expand=True, padx=8)

        # Основной дисплей
        display_frame = tk.Frame(self.root, bg="#26262a", height=80)
        display_frame.pack(fill="x", padx=10, pady=(5, 10))
        display_frame.pack_propagate(False)

        display = tk.Entry(
            display_frame,
            textvariable=self.input_text,
            font=("Consolas", 26, "bold"),
            bg="#26262a",
            fg="#f5f5f5",
            bd=0,
            justify="right",
            insertbackground="#f5f5f5"
        )
        display.pack(fill="both", expand=True, padx=10, pady=10)
        display.focus_set()

        # Переключатель градусы/радианы
        mode_frame = tk.Frame(self.root, bg="#141414")
        mode_frame.pack(fill="x", padx=10, pady=(0, 5))

        self.mode_btn = tk.Button(
            mode_frame,
            text="DEG",
            font=("Consolas", 10, "bold"),
            bg="#32323a",
            fg="#64c8ff",
            bd=0,
            width=6,
            command=self.toggle_mode
        )
        self.mode_btn.pack(side="left", padx=2)

        tk.Label(
            mode_frame,
            text="Режим углов:",
            font=("Consolas", 10),
            bg="#141414",
            fg="#8888aa"
        ).pack(side="left", padx=5)

    # ===== КНОПКИ =====
    def create_buttons(self):
        # Контейнер для кнопок
        btn_frame = tk.Frame(self.root, bg="#141414")
        btn_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Цвета
        colors = {
            "num": "#37373d",      # цифры
            "op": "#4a4a52",       # операторы
            "func": "#2d2d34",     # функции
            "eq": "#3c5f73",       # равно
            "clear": "#553434",    # очистка
            "mem": "#3a3a2e",      # память
        }

        # Раскладка кнопок (текст, цвет, row, col, colspan)
        buttons = [
            # Ряд 1: научные функции
            ("sin", colors["func"], 0, 0, 1),
            ("cos", colors["func"], 0, 1, 1),
            ("tan", colors["func"], 0, 2, 1),
            ("ln", colors["func"], 0, 3, 1),
            ("log", colors["func"], 0, 4, 1),

            # Ряд 2: обратные функции
            ("asin", colors["func"], 1, 0, 1),
            ("acos", colors["func"], 1, 1, 1),
            ("atan", colors["func"], 1, 2, 1),
            ("sinh", colors["func"], 1, 3, 1),
            ("cosh", colors["func"], 1, 4, 1),

            # Ряд 3: гиперболические и прочее
            ("tanh", colors["func"], 2, 0, 1),
            ("x²", colors["func"], 2, 1, 1),
            ("√", colors["func"], 2, 2, 1),
            ("1/x", colors["func"], 2, 3, 1),
            ("!", colors["func"], 2, 4, 1),

            # Ряд 4: константы и память
            ("π", colors["func"], 3, 0, 1),
            ("e", colors["func"], 3, 1, 1),
            ("EXP", colors["func"], 3, 2, 1),
            ("±", colors["func"], 3, 3, 1),
            ("%", colors["func"], 3, 4, 1),

            # Ряд 5: память и очистка
            ("MC", colors["mem"], 4, 0, 1),
            ("MR", colors["mem"], 4, 1, 1),
            ("MS", colors["mem"], 4, 2, 1),
            ("M+", colors["mem"], 4, 3, 1),
            ("M-", colors["mem"], 4, 4, 1),

            # Ряд 6: очистка и операторы
            ("C", colors["clear"], 5, 0, 2),
            ("⌫", colors["clear"], 5, 2, 1),
            ("(", colors["op"], 5, 3, 1),
            (")", colors["op"], 5, 4, 1),

            # Ряд 7: цифры и деление
            ("7", colors["num"], 6, 0, 1),
            ("8", colors["num"], 6, 1, 1),
            ("9", colors["num"], 6, 2, 1),
            ("/", colors["op"], 6, 3, 1),
            ("^", colors["op"], 6, 4, 1),

            # Ряд 8
            ("4", colors["num"], 7, 0, 1),
            ("5", colors["num"], 7, 1, 1),
            ("6", colors["num"], 7, 2, 1),
            ("*", colors["op"], 7, 3, 1),
            ("%", colors["op"], 7, 4, 1),

            # Ряд 9
            ("1", colors["num"], 8, 0, 1),
            ("2", colors["num"], 8, 1, 1),
            ("3", colors["num"], 8, 2, 1),
            ("-", colors["op"], 8, 3, 1),
            ("+", colors["op"], 8, 4, 1),

            # Ряд 10
            ("0", colors["num"], 9, 0, 2),
            (".", colors["num"], 9, 2, 1),
            ("=", colors["eq"], 9, 3, 2),
        ]

        # Настройка сетки
        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1, minsize=70)
        for i in range(10):
            btn_frame.grid_rowconfigure(i, weight=1, minsize=45)

        # Создание кнопок
        for text, color, row, col, colspan in buttons:
            btn = tk.Button(
                btn_frame,
                text=text,
                font=("Consolas", 12, "bold"),
                bg=color,
                fg="#f0f0f0",
                bd=0,
                activebackground="#5a5a66",
                activeforeground="#ffffff",
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=2, pady=2)

            # Эффект наведения
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=self.lighten(c)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))

    # ===== ИСТОРИЯ =====
    def create_history(self):
        history_frame = tk.Frame(self.root, bg="#141414", height=60)
        history_frame.pack(fill="x", padx=10, pady=(5, 10))
        history_frame.pack_propagate(False)

        tk.Label(
            history_frame,
            text="История:",
            font=("Consolas", 10),
            bg="#141414",
            fg="#666688",
            anchor="w"
        ).pack(fill="x")

        self.history_box = tk.Text(
            history_frame,
            height=3,
            font=("Consolas", 10),
            bg="#1a1a1e",
            fg="#a0a0b0",
            bd=0,
            wrap="word",
            state="disabled"
        )
        self.history_box.pack(fill="both", expand=True)

    # ===== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ =====
    def lighten(self, hex_color):
        """Осветлить цвет для hover-эффекта"""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, r + 25)
        g = min(255, g + 25)
        b = min(255, b + 25)
        return f"#{r:02x}{g:02x}{b:02x}"

    def toggle_mode(self):
        """Переключение между градусами и радианами"""
        self.use_degrees = not self.use_degrees
        self.mode_btn.config(text="DEG" if self.use_degrees else "RAD")

    def to_radians(self, value):
        """Перевод в радианы, если выбран режим DEG"""
        return math.radians(value) if self.use_degrees else value

    def to_degrees(self, value):
        """Перевод из радиан в градусы, если выбран режим DEG"""
        return math.degrees(value) if self.use_degrees else value

    def add_history(self, text):
        """Добавить запись в историю"""
        self.history_box.config(state="normal")
        self.history_box.insert("end", text + "\n")
        self.history_box.see("end")
        self.history_box.config(state="disabled")

    # ===== ОБРАБОТКА НАЖАТИЙ =====
    def on_button_click(self, value):
        try:
            if value == "C":
                self.expression = ""
                self.input_text.set("")
                self.history_text.set("")

            elif value == "⌫":
                self.expression = self.expression[:-1]
                self.input_text.set(self.expression)

            elif value == "=":
                self.calculate()

            elif value == "π":
                self.expression += str(math.pi)
                self.input_text.set(self.expression)

            elif value == "e":
                self.expression += str(math.e)
                self.input_text.set(self.expression)

            elif value == "x²":
                self.expression += "**2"
                self.input_text.set(self.expression)

            elif value == "√":
                self.expression += "sqrt("
                self.input_text.set(self.expression)

            elif value == "1/x":
                self.expression = "1/(" + self.expression + ")"
                self.input_text.set(self.expression)

            elif value == "!":
                self.expression += "factorial("
                self.input_text.set(self.expression)

            elif value == "±":
                if self.expression.startswith("-"):
                    self.expression = self.expression[1:]
                else:
                    self.expression = "-" + self.expression
                self.input_text.set(self.expression)

            elif value == "EXP":
                self.expression += "e"
                self.input_text.set(self.expression)

            # ===== ПАМЯТЬ =====
            elif value == "MC":
                self.memory = 0

            elif value == "MR":
                self.expression += str(self.memory)
                self.input_text.set(self.expression)

            elif value == "MS":
                try:
                    self.memory = float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except:
                    self.memory = 0

            elif value == "M+":
                try:
                    self.memory += float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except:
                    pass

            elif value == "M-":
                try:
                    self.memory -= float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except:
                    pass

            # ===== ТРИГОНОМЕТРИЯ =====
            elif value in ("sin", "cos", "tan"):
                self.expression += f"{value}("
                self.input_text.set(self.expression)

            elif value in ("asin", "acos", "atan"):
                self.expression += f"{value}("
                self.input_text.set(self.expression)

            elif value in ("sinh", "cosh", "tanh"):
                self.expression += f"{value}("
                self.input_text.set(self.expression)

            elif value == "ln":
                self.expression += "log("
                self.input_text.set(self.expression)

            elif value == "log":
                self.expression += "log10("
                self.input_text.set(self.expression)

            # ===== ОБЫЧНЫЕ СИМВОЛЫ =====
            else:
                self.expression += str(value)
                self.input_text.set(self.expression)

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # ===== ФУНКЦИИ ДЛЯ EVAL =====
    def math_funcs(self):
        """Безопасный набор математических функций"""
        return {
            "sin": lambda x: math.sin(self.to_radians(x)),
            "cos": lambda x: math.cos(self.to_radians(x)),
            "tan": lambda x: math.tan(self.to_radians(x)),
            "asin": lambda x: self.to_degrees(math.asin(x)),
            "acos": lambda x: self.to_degrees(math.acos(x)),
            "atan": lambda x: self.to_degrees(math.atan(x)),
            "sinh": math.sinh,
            "cosh": math.cosh,
            "tanh": math.tanh,
            "sqrt": math.sqrt,
            "log": math.log,
            "log10": math.log10,
            "factorial": math.factorial,
            "pi": math.pi,
            "e": math.e,
            "abs": abs,
            "round": round,
        }

    # ===== ВЫЧИСЛЕНИЕ =====
    def calculate(self):
        try:
            # Автоматически закрываем скобки
            open_count = self.expression.count("(") - self.expression.count(")")
            if open_count > 0:
                self.expression += ")" * open_count

            # Вычисление
            result = eval(self.expression, {"__builtins__": None}, self.math_funcs())

            # Форматирование результата
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            # История
            self.add_history(f"{self.expression} = {result}")

            # Отображение
            self.history_text.set(self.expression + " =")
            self.expression = str(result)
            self.input_text.set(self.expression)

        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            self.expression = ""
            self.input_text.set("")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Некорректное значение: {e}")
            self.expression = ""
            self.input_text.set("")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {e}")
            self.expression = ""
            self.input_text.set("")

    # ===== КЛАВИАТУРА =====
    def key_press(self, event):
        key = event.char
        keysym = event.keysym

        if key in "0123456789+-*/.()":
            self.expression += key
            self.input_text.set(self.expression)

        elif key == "\r" or keysym == "Return":
            self.calculate()

        elif keysym == "BackSpace":
            self.expression = self.expression[:-1]
            self.input_text.set(self.expression)

        elif keysym == "Escape":
            self.expression = ""
            self.input_text.set("")

        elif key == "=":
            self.calculate()


# ===== ЗАПУСК =====
if __name__ == "__main__":
    root = tk.Tk()
    app = EngineeringCalculator(root)
    root.mainloop()