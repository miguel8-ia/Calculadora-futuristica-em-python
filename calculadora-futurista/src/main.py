"""Ponto de entrada: python src/main.py"""

import sys

from calculator import Calculator
from interface import CalculatorUI


def _enable_high_dpi() -> None:
    """No Windows, evita que a janela fique borrada em telas de alta resolução."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, OSError):
            pass


def main() -> None:
    _enable_high_dpi()
    CalculatorUI(Calculator()).run()


if __name__ == "__main__":
    main()
