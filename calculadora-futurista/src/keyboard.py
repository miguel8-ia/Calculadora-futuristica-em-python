"""Mapeamento do teclado físico para as ações da calculadora."""

from __future__ import annotations

import tkinter as tk
from typing import Callable

CHAR_ACTIONS = {
    **{str(n): f"digit:{n}" for n in range(10)},
    "+": "op:+", "-": "op:-", "*": "op:*", "x": "op:*", "X": "op:*",
    "/": "op:/", ".": "decimal", ",": "decimal", "=": "equals", "%": "percent",
}

KEYSYM_ACTIONS = {
    "Return": "equals", "KP_Enter": "equals",
    "BackSpace": "backspace", "Escape": "clear", "Delete": "clear",
}


def bind_keyboard(widget: tk.Misc, on_action: Callable[[str], None]) -> None:
    """Faz as teclas pressionadas chamarem ``on_action(ação)``."""

    def handler(event: tk.Event) -> None:
        action = KEYSYM_ACTIONS.get(event.keysym) or CHAR_ACTIONS.get(event.char)
        if action:
            on_action(action)

    widget.bind("<Key>", handler)
