"""Interface gráfica futurista com ilusão de profundidade 3D (Tkinter puro)."""

from __future__ import annotations

import tkinter as tk
from tkinter import font as tkfont
from typing import Dict, Sequence

import config
from calculator import Calculator
from keyboard import bind_keyboard


# ----------------------------------------------------------------- utilitários
def _hex_to_rgb(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)


def blend(color_a: str, color_b: str, t: float) -> str:
    """Mistura duas cores hexadecimais (t=0 -> a, t=1 -> b)."""
    t = max(0.0, min(1.0, t))
    a, b = _hex_to_rgb(color_a), _hex_to_rgb(color_b)
    r, g, bl = (round(x + (y - x) * t) for x, y in zip(a, b))
    return f"#{r:02x}{g:02x}{bl:02x}"


def rounded_points(x1: float, y1: float, x2: float, y2: float,
                   r: float) -> list[float]:
    """Pontos de um retângulo arredondado (usar com smooth=True)."""
    r = max(0.0, min(r, (x2 - x1) / 2, (y2 - y1) / 2))
    return [x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
            x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
            x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2,
            x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1]


def pick_font(root: tk.Misc, candidates: Sequence[str]) -> str:
    """Retorna a primeira fonte instalada da lista."""
    installed = set(tkfont.families(root))
    return next((name for name in candidates if name in installed),
                "TkDefaultFont")


# ------------------------------------------------------------------ componentes
class NeonButton(tk.Canvas):
    """Botão 3D: corpo com profundidade, brilho, hover e efeito de pressionar."""

    def __init__(self, master: tk.Misc, text: str, kind: str,
                 command, font_family: str) -> None:
        super().__init__(master, bg=config.PANEL, highlightthickness=0,
                         bd=0, cursor="hand2")
        self._text = text
        self._style = config.BUTTON_STYLES[kind]
        self._command = command
        self._font = tkfont.Font(family=font_family, weight="bold", size=-18)
        self._hover = False
        self._pressed = False
        self._glow = 0.0
        self._glow_target = 0.0
        self._sink = 0.0          # 0 = relevo normal, 1 = totalmente pressionado
        self._sink_target = 0.0
        self._after_id: str | None = None

        self.bind("<Configure>", lambda _e: self._draw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    # --- API pública
    def flash(self) -> None:
        """Simula um clique (usado quando a tecla correspondente é digitada)."""
        self._pressed = True
        self._update_targets()
        self.after(120, self._end_flash)

    def destroy(self) -> None:
        if self._after_id is not None:
            self.after_cancel(self._after_id)
            self._after_id = None
        super().destroy()

    # --- eventos
    def _end_flash(self) -> None:
        if self.winfo_exists():
            self._pressed = False
            self._update_targets()

    def _on_enter(self, _event: tk.Event) -> None:
        self._hover = True
        self._update_targets()

    def _on_leave(self, _event: tk.Event) -> None:
        self._hover = False
        self._pressed = False
        self._update_targets()

    def _on_press(self, _event: tk.Event) -> None:
        self._pressed = True
        self._update_targets()

    def _on_release(self, event: tk.Event) -> None:
        was_pressed = self._pressed
        self._pressed = False
        self._update_targets()
        inside = (0 <= event.x <= self.winfo_width()
                  and 0 <= event.y <= self.winfo_height())
        if was_pressed and inside:
            self._command()

    # --- animação (leve: ~60 quadros/s apenas enquanto algo está mudando)
    def _update_targets(self) -> None:
        self._glow_target = 1.0 if (self._hover or self._pressed) else 0.0
        self._sink_target = 1.0 if self._pressed else 0.0
        if self._after_id is None:
            self._after_id = self.after(0, self._tick)

    def _tick(self) -> None:
        self._after_id = None
        if not self.winfo_exists():
            return
        moving = False
        for name, target in (("_glow", self._glow_target),
                             ("_sink", self._sink_target)):
            current = getattr(self, name)
            diff = target - current
            if abs(diff) > 0.03:
                setattr(self, name, current + diff * 0.5)
                moving = True
            else:
                setattr(self, name, target)
        self._draw()
        if moving:
            self._after_id = self.after(16, self._tick)

    # --- desenho
    def _draw(self) -> None:
        w, h = self.winfo_width(), self.winfo_height()
        if w < 12 or h < 12:
            return
        self.delete("all")
        s = self._style
        margin = max(3.0, min(w, h) * 0.05)
        depth = max(3.0, h * 0.08)
        radius = min(w, h) * 0.24
        x1, x2 = margin, w - margin
        top, bottom = margin, h - margin
        sink = depth * 0.8 * self._sink
        face_top = top + sink
        face_bottom = bottom - depth + sink
        border = blend(s["border"], config.ACCENT, self._glow)

        if self._glow > 0.03:  # halo neon ao redor do botão
            ring = blend(config.PANEL, border, 0.55 * self._glow)
            self.create_polygon(
                rounded_points(x1 - 2, top - 2, x2 + 2, bottom + 2, radius + 2),
                smooth=True, fill="", outline=ring, width=2)

        # corpo (lateral escura que cria a profundidade)
        self.create_polygon(
            rounded_points(x1, top + depth, x2, bottom, radius),
            smooth=True, fill=blend(s["face"], "#000000", 0.6), outline="")
        # face
        face_fill = blend(s["face"], "#FFFFFF", 0.10 * self._glow)
        self.create_polygon(
            rounded_points(x1, face_top, x2, face_bottom, radius),
            smooth=True, fill=face_fill, outline="")
        # brilho (efeito vidro na metade de cima)
        gloss_bottom = face_top + (face_bottom - face_top) * 0.46
        self.create_polygon(
            rounded_points(x1 + 3, face_top + 3, x2 - 3, gloss_bottom,
                           radius * 0.8),
            smooth=True, outline="",
            fill=blend(s["gloss"], "#FFFFFF", 0.12 * self._glow))
        # borda neon
        self.create_polygon(
            rounded_points(x1, face_top, x2, face_bottom, radius),
            smooth=True, fill="", outline=border, width=2)

        self._font.configure(size=-max(12, int(min(w, h) * 0.34)))
        self.create_text((x1 + x2) / 2, (face_top + face_bottom) / 2,
                         text=self._text, font=self._font, fill=s["text"])


class DisplayPanel(tk.Canvas):
    """Display digital escuro com brilho sutil e alinhamento à direita."""

    def __init__(self, master: tk.Misc, font_family: str) -> None:
        super().__init__(master, bg=config.PANEL, highlightthickness=0, bd=0)
        self._value_font = tkfont.Font(family=font_family, weight="bold",
                                       size=-48)
        self._expr_font = tkfont.Font(family=font_family, size=-20)
        self._expression = ""
        self._value = "0"
        self._is_error = False
        self.bind("<Configure>", lambda _e: self._draw())

    def show(self, expression: str, value: str, is_error: bool = False) -> None:
        self._expression = expression
        self._value = value
        self._is_error = is_error
        self._draw()

    def _fit(self, font: tkfont.Font, text: str, max_px: int,
             available: float) -> None:
        font.configure(size=-max_px)
        width = font.measure(text)
        if width > available:
            font.configure(size=-max(12, int(max_px * available / width)))

    def _draw(self) -> None:
        w, h = self.winfo_width(), self.winfo_height()
        if w < 40 or h < 40:
            return
        self.delete("all")
        bg, m = config.DISPLAY_BG, 3
        self.create_polygon(rounded_points(m, m, w - m, h - m, 20),
                            smooth=True, fill=bg, width=2,
                            outline=blend(bg, config.ACCENT, 0.45))
        self.create_polygon(rounded_points(m + 5, m + 5, w - m - 5, h - m - 5, 16),
                            smooth=True, fill="",
                            outline=blend(bg, config.ACCENT, 0.12))
        for y in range(m + 14, h - m - 10, 4):  # linhas de varredura (scanlines)
            self.create_line(m + 14, y, w - m - 14, y,
                             fill=blend(bg, config.ACCENT, 0.04))

        pad = max(18, int(w * 0.04))
        right, available = w - m - pad, w - 2 * (m + pad)

        expr = self._expression
        self._fit(self._expr_font, expr, max(12, int(h * 0.12)), available)
        while expr and self._expr_font.measure(expr) > available:
            expr = expr[1:]
        self.create_text(right, h * 0.26, text=expr, anchor="e",
                         font=self._expr_font, fill=config.TEXT_MUTED)

        color = config.ERROR_COLOR if self._is_error else config.TEXT
        max_px = int(h * (0.22 if self._is_error else 0.38))
        self._fit(self._value_font, self._value, max(20, max_px), available)
        y = h * 0.64
        glow = blend(bg, color if self._is_error else config.ACCENT, 0.30)
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            self.create_text(right + dx, y + dy, text=self._value, anchor="e",
                             font=self._value_font, fill=glow)
        self.create_text(right, y, text=self._value, anchor="e",
                         font=self._value_font, fill=color)


class Backdrop(tk.Canvas):
    """Fundo com halos de luz e um piso em perspectiva (grade holográfica)."""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, bg=config.BACKGROUND, highlightthickness=0,
                         bd=0)
        self.bind("<Configure>", lambda _e: self._draw())

    def _halo(self, cx: float, cy: float, size: float, color: str,
              strength: float) -> None:
        steps = 14
        for i in range(steps, 0, -1):
            r = i * size
            t = strength * (steps - i + 1) / steps
            self.create_oval(cx - r, cy - r, cx + r, cy + r, outline="",
                             fill=blend(config.BACKGROUND, color, t))

    def _draw(self) -> None:
        w, h = self.winfo_width(), self.winfo_height()
        if w < 40 or h < 40:
            return
        self.delete("all")
        self._halo(w * 0.15, h * 0.12, max(w, h) * 0.045,
                   config.ACCENT_SECONDARY, 0.20)
        self._halo(w * 0.88, h * 0.92, max(w, h) * 0.04, config.ACCENT, 0.14)
        horizon, vx = h * 0.55, w / 2
        line = blend(config.BACKGROUND, config.ACCENT, 0.12)
        for k in range(-12, 13):
            self.create_line(vx + k * 8, horizon, vx + k * w * 0.12, h,
                             fill=line)
        for j in range(1, 12):
            y = horizon + (h - horizon) * (j / 11) ** 2
            self.create_line(0, y, w, y, fill=line)


# ------------------------------------------------------------ janela principal
class CalculatorUI:
    """Monta a janela e conecta botões e teclado à classe ``Calculator``."""

    def __init__(self, calculator: Calculator,
                 root: tk.Tk | None = None) -> None:
        self._calc = calculator
        self._root = root or tk.Tk()
        self._buttons: Dict[str, NeonButton] = {}
        self._setup_window()
        self._build_layout()
        bind_keyboard(self._root, self._on_key_action)
        self._refresh_display()

    def run(self) -> None:
        self._root.mainloop()

    # --- construção
    def _setup_window(self) -> None:
        root = self._root
        root.title(config.APP_TITLE)
        root.configure(bg=config.BACKGROUND)
        root.minsize(config.MIN_WINDOW_WIDTH, config.MIN_WINDOW_HEIGHT)
        x = (root.winfo_screenwidth() - config.WINDOW_WIDTH) // 2
        y = (root.winfo_screenheight() - config.WINDOW_HEIGHT) // 2
        root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}"
                      f"+{max(x, 0)}+{max(y, 0)}")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

    def _build_layout(self) -> None:
        root = self._root
        display_font = pick_font(root, config.DISPLAY_FONTS)
        ui_font = pick_font(root, config.UI_FONTS)

        Backdrop(root).grid(row=0, column=0, sticky="nsew")
        # sombra do painel: mesmo tamanho, deslocada 8 px (profundidade)
        tk.Frame(root, bg=config.SHADOW).grid(
            row=0, column=0, sticky="nsew", padx=(60, 36), pady=(46, 22))
        edge = blend(config.PANEL, config.ACCENT, 0.5)
        panel = tk.Frame(root, bg=config.PANEL, highlightthickness=2,
                         highlightbackground=edge, highlightcolor=edge)
        panel.grid(row=0, column=0, sticky="nsew", padx=(52, 44), pady=(38, 30))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=2, minsize=110)
        panel.grid_rowconfigure(2, weight=7)

        header = tk.Frame(panel, bg=config.PANEL)
        header.grid(row=0, column=0, sticky="ew", padx=22, pady=(14, 4))
        header.grid_columnconfigure(0, weight=1)
        tk.Label(header, text="FUTURA // CALC", bg=config.PANEL,
                 fg=config.ACCENT, font=(ui_font, 11, "bold")
                 ).grid(row=0, column=0, sticky="w")
        tk.Label(header, text="● ONLINE", bg=config.PANEL,
                 fg=config.ACCENT_SECONDARY, font=(ui_font, 10, "bold")
                 ).grid(row=0, column=1, sticky="e")

        self._display = DisplayPanel(panel, display_font)
        self._display.grid(row=1, column=0, sticky="nsew", padx=18,
                           pady=(4, 10))

        keypad = tk.Frame(panel, bg=config.PANEL)
        keypad.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 18))
        for r in range(len(config.BUTTON_LAYOUT)):
            keypad.grid_rowconfigure(r, weight=1, uniform="key_row")
        for c in range(4):
            keypad.grid_columnconfigure(c, weight=1, uniform="key_col")
        for r, row in enumerate(config.BUTTON_LAYOUT):
            for c, (label, action, kind) in enumerate(row):
                button = NeonButton(keypad, label, kind,
                                    lambda a=action: self._dispatch(a),
                                    ui_font)
                button.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
                self._buttons[action] = button

    # --- comportamento
    def _on_key_action(self, action: str) -> None:
        button = self._buttons.get(action)
        if button is not None:
            button.flash()
        self._dispatch(action)

    def _dispatch(self, action: str) -> None:
        name, _, arg = action.partition(":")
        calc = self._calc
        if name == "digit":
            calc.input_digit(arg)
        elif name == "op":
            calc.set_operator(arg)
        elif name == "decimal":
            calc.input_decimal()
        elif name == "equals":
            calc.calculate()
        elif name == "clear":
            calc.clear()
        elif name == "backspace":
            calc.backspace()
        elif name == "percent":
            calc.percent()
        elif name == "sign":
            calc.toggle_sign()
        self._refresh_display()

    def _refresh_display(self) -> None:
        self._display.show(self._calc.expression, self._calc.display,
                           self._calc.has_error)
