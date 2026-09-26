import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import math

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class EngineeringCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Инженерный калькулятор")
        self.root.geometry("480x700")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#141414")

        self.expression = ""
        self.input_text = tk.StringVar()
        self.history_text = tk.StringVar()
        self.memory = 0
        self.use_degrees = True

        self.create_display()
        self.create_buttons()
        self.create_history()

        self.root.bind("<Key>", self.key_press)
        self.root.bind("<Control-c>", self._copy)
        self.root.bind("<Control-v>", self._paste)
        self.root.bind("<Control-x>", self._cut)
        self.root.bind("<Control-a>", self._select_all)

    def _focused(self):
        return self.root.focus_get()

    def _copy(self, event=None):
        w = self._focused()
        try:
            if isinstance(w, tk.Entry):
                text = w.selection_get() if w.selection_present() else w.get()
            elif isinstance(w, tk.Text):
                text = w.get("sel.first", "sel.last") if w.tag_ranges("sel") else w.get("1.0", "end-1c")
            else:
                return
            if text:
                self.root.clipboard_clear()
                self.root.clipboard_append(text)
                self.root.update()
        except Exception:
            pass

    def _paste(self, event=None):
        w = self._focused()
        try:
            text = self.root.clipboard_get()
        except Exception:
            return
        try:
            if isinstance(w, tk.Entry):
                if w.selection_present():
                    w.delete("sel.first", "sel.last")
                w.insert("insert", text)
            elif isinstance(w, tk.Text):
                if w.tag_ranges("sel"):
                    w.delete("sel.first", "sel.last")
                w.insert("insert", text)
        except Exception:
            pass

    def _cut(self, event=None):
        w = self._focused()
        try:
            if isinstance(w, tk.Entry):
                if not w.selection_present():
                    return
                text = w.selection_get()
                w.delete("sel.first", "sel.last")
            elif isinstance(w, tk.Text):
                if not w.tag_ranges("sel"):
                    return
                text = w.get("sel.first", "sel.last")
                w.delete("sel.first", "sel.last")
            else:
                return
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.root.update()
        except Exception:
            pass

    def _select_all(self, event=None):
        w = self._focused()
        try:
            if isinstance(w, tk.Entry):
                w.select_range(0, "end")
                w.icursor("end")
            elif isinstance(w, tk.Text):
                w.tag_add("sel", "1.0", "end-1c")
                w.mark_set("insert", "1.0")
                w.see("insert")
        except Exception:
            pass

    def create_display(self):
        history_frame = ctk.CTkFrame(self.root, fg_color="#1e1e1e", height=32, corner_radius=6)
        history_frame.pack(fill="x", padx=12, pady=(12, 0))
        history_frame.pack_propagate(False)

        tk.Label(
            history_frame,
            textvariable=self.history_text,
            font=("Consolas", 11),
            bg="#1e1e1e",
            fg="#8888aa",
            anchor="e"
        ).pack(fill="both", expand=True, padx=10)

        display_frame = ctk.CTkFrame(self.root, fg_color="#26262a", height=90, corner_radius=8)
        display_frame.pack(fill="x", padx=12, pady=(6, 12))
        display_frame.pack_propagate(False)

        self.display_widget = tk.Entry(
            display_frame,
            textvariable=self.input_text,
            font=("Consolas", 28, "bold"),
            bg="#26262a",
            fg="#f5f5f5",
            bd=0,
            justify="right",
            insertbackground="#f5f5f5"
        )
        self.display_widget.pack(fill="both", expand=True, padx=12, pady=12)
        self.display_widget.focus_set()

        mode_frame = ctk.CTkFrame(self.root, fg_color="#141414")
        mode_frame.pack(fill="x", padx=12, pady=(0, 8))

        self.mode_btn = ctk.CTkButton(
            mode_frame,
            text="DEG",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            fg_color="#32323a",
            hover_color="#44444e",
            text_color="#64c8ff",
            width=70,
            height=30,
            corner_radius=6,
            command=self.toggle_mode
        )
        self.mode_btn.pack(side="left", padx=2)

        ctk.CTkLabel(
            mode_frame,
            text="Режим углов:",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#8888aa"
        ).pack(side="left", padx=6)

    def create_buttons(self):
        btn_frame = ctk.CTkFrame(self.root, fg_color="#141414")
        btn_frame.pack(fill="both", expand=True, padx=12, pady=6)

        colors = {
            "num": "#37373d", "op": "#4a4a52", "func": "#2d2d34",
            "eq": "#3c5f73", "clear": "#553434", "mem": "#3a3a2e",
        }
        hover_colors = {
            "num": "#4a4a52", "op": "#5c5c66", "func": "#3d3d46",
            "eq": "#4a728c", "clear": "#6b4242", "mem": "#4a4a3a",
        }

        buttons = [
            ("sin", "func", 0, 0, 1), ("cos", "func", 0, 1, 1), ("tan", "func", 0, 2, 1),
            ("ln", "func", 0, 3, 1), ("log", "func", 0, 4, 1),

            ("asin", "func", 1, 0, 1), ("acos", "func", 1, 1, 1), ("atan", "func", 1, 2, 1),
            ("sinh", "func", 1, 3, 1), ("cosh", "func", 1, 4, 1),

            ("tanh", "func", 2, 0, 1), ("x²", "func", 2, 1, 1), ("√", "func", 2, 2, 1),
            ("1/x", "func", 2, 3, 1), ("!", "func", 2, 4, 1),

            ("π", "func", 3, 0, 1), ("e", "func", 3, 1, 1), ("EXP", "func", 3, 2, 1),
            ("±", "func", 3, 3, 1), ("%", "func", 3, 4, 1),

            ("MC", "mem", 4, 0, 1), ("MR", "mem", 4, 1, 1), ("MS", "mem", 4, 2, 1),
            ("M+", "mem", 4, 3, 1), ("M-", "mem", 4, 4, 1),

            ("C", "clear", 5, 0, 2), ("⌫", "clear", 5, 2, 1), ("(", "op", 5, 3, 1), (")", "op", 5, 4, 1),

            ("7", "num", 6, 0, 1), ("8", "num", 6, 1, 1), ("9", "num", 6, 2, 1),
            ("/", "op", 6, 3, 1), ("^", "op", 6, 4, 1),

            ("4", "num", 7, 0, 1), ("5", "num", 7, 1, 1), ("6", "num", 7, 2, 1),
            ("*", "op", 7, 3, 1), ("%", "op", 7, 4, 1),

            ("1", "num", 8, 0, 1), ("2", "num", 8, 1, 1), ("3", "num", 8, 2, 1),
            ("-", "op", 8, 3, 1), ("+", "op", 8, 4, 1),

            ("0", "num", 9, 0, 2), (".", "num", 9, 2, 1), ("=", "eq", 9, 3, 2),
        ]

        for i in range(5):
            btn_frame.grid_columnconfigure(i, weight=1, uniform="col", minsize=80)
        for i in range(10):
            btn_frame.grid_rowconfigure(i, weight=1, uniform="row", minsize=52)

        for text, color_key, row, col, colspan in buttons:
            btn = ctk.CTkButton(
                btn_frame,
                text=text,
                font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
                fg_color=colors[color_key],
                hover_color=hover_colors[color_key],
                text_color="#f0f0f0",
                corner_radius=6,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, columnspan=colspan, sticky="nsew", padx=3, pady=3)

    def create_history(self):
        history_frame = ctk.CTkFrame(self.root, fg_color="#141414", height=80)
        history_frame.pack(fill="x", padx=12, pady=(6, 12))
        history_frame.pack_propagate(False)

        tk.Label(
            history_frame,
            text="История:",
            font=("Consolas", 11),
            bg="#141414",
            fg="#666688",
            anchor="w"
        ).pack(fill="x")

        self.history_box = tk.Text(
            history_frame,
            height=3,
            font=("Consolas", 11),
            bg="#1a1a1e",
            fg="#a0a0b0",
            bd=0,
            wrap="word",
            insertbackground="#a0a0b0"
        )
        self.history_box.pack(fill="both", expand=True)
        self.history_box.configure(state="disabled")

    def toggle_mode(self):
        self.use_degrees = not self.use_degrees
        self.mode_btn.configure(text="DEG" if self.use_degrees else "RAD")

    def to_radians(self, value):
        return math.radians(value) if self.use_degrees else value

    def to_degrees(self, value):
        return math.degrees(value) if self.use_degrees else value

    def add_history(self, text):
        self.history_box.configure(state="normal")
        self.history_box.insert("end", text + "\n")
        self.history_box.see("end")
        self.history_box.configure(state="disabled")

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
            elif value == "MC":
                self.memory = 0
            elif value == "MR":
                self.expression += str(self.memory)
                self.input_text.set(self.expression)
            elif value == "MS":
                try:
                    self.memory = float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except Exception:
                    self.memory = 0
            elif value == "M+":
                try:
                    self.memory += float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except Exception:
                    pass
            elif value == "M-":
                try:
                    self.memory -= float(eval(self.expression, {"__builtins__": None}, self.math_funcs()))
                except Exception:
                    pass
            elif value in ("sin", "cos", "tan", "asin", "acos", "atan", "sinh", "cosh", "tanh"):
                self.expression += f"{value}("
                self.input_text.set(self.expression)
            elif value == "ln":
                self.expression += "log("
                self.input_text.set(self.expression)
            elif value == "log":
                self.expression += "log10("
                self.input_text.set(self.expression)
            else:
                self.expression += str(value)
                self.input_text.set(self.expression)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def math_funcs(self):
        return {
            "sin": lambda x: math.sin(self.to_radians(x)),
            "cos": lambda x: math.cos(self.to_radians(x)),
            "tan": lambda x: math.tan(self.to_radians(x)),
            "asin": lambda x: self.to_degrees(math.asin(x)),
            "acos": lambda x: self.to_degrees(math.acos(x)),
            "atan": lambda x: self.to_degrees(math.atan(x)),
            "sinh": math.sinh, "cosh": math.cosh, "tanh": math.tanh,
            "sqrt": math.sqrt, "log": math.log, "log10": math.log10,
            "factorial": math.factorial,
            "pi": math.pi, "e": math.e,
            "abs": abs, "round": round,
        }

    def calculate(self):
        try:
            open_count = self.expression.count("(") - self.expression.count(")")
            if open_count > 0:
                self.expression += ")" * open_count

            result = eval(self.expression, {"__builtins__": None}, self.math_funcs())

            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.add_history(f"{self.expression} = {result}")
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


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = EngineeringCalculator(root)
    root.mainloop()
