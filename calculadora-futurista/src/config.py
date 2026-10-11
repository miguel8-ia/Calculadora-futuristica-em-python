"""Configurações visuais e de layout da Calculadora Futurista 3D."""

APP_TITLE = "Calculadora Futurista 3D"
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
MIN_WINDOW_WIDTH = 480
MIN_WINDOW_HEIGHT = 600

# --- Paleta ---------------------------------------------------------------
BACKGROUND = "#05070D"
PANEL = "#0B1020"
ELEMENT = "#111A2E"
ACCENT = "#00E5FF"
ACCENT_SECONDARY = "#7C3AED"
TEXT = "#FFFFFF"
TEXT_MUTED = "#94A3B8"
DISPLAY_BG = "#070B16"
ERROR_COLOR = "#FF6B8A"
SHADOW = "#02030A"

# --- Fontes (a primeira instalada no sistema é usada) -----------------------
DISPLAY_FONTS = ("Orbitron", "Share Tech Mono", "Consolas", "Menlo",
                 "DejaVu Sans Mono", "Courier New")
UI_FONTS = ("Segoe UI", "Helvetica Neue", "DejaVu Sans", "Arial")

# --- Estilos dos botões -----------------------------------------------------
# face: cor principal | gloss: brilho da metade superior
# text: cor do texto  | border: cor da borda neon
BUTTON_STYLES = {
    "digit": {"face": "#16223D", "gloss": "#22335A",
              "text": TEXT, "border": "#26385F"},
    "function": {"face": "#13243A", "gloss": "#1D3552",
                 "text": ACCENT, "border": "#1F4A66"},
    "operator": {"face": "#2B1B5C", "gloss": "#3D2A7A",
                 "text": "#D8CCFF", "border": ACCENT_SECONDARY},
    "equals": {"face": "#00AFC4", "gloss": "#35D6E8",
               "text": "#031018", "border": ACCENT},
}

# --- Layout do teclado: (rótulo, ação, estilo) -------------------------------
BUTTON_LAYOUT = (
    (("C", "clear", "function"), ("⌫", "backspace", "function"),
     ("%", "percent", "function"), ("÷", "op:/", "operator")),
    (("7", "digit:7", "digit"), ("8", "digit:8", "digit"),
     ("9", "digit:9", "digit"), ("×", "op:*", "operator")),
    (("4", "digit:4", "digit"), ("5", "digit:5", "digit"),
     ("6", "digit:6", "digit"), ("−", "op:-", "operator")),
    (("1", "digit:1", "digit"), ("2", "digit:2", "digit"),
     ("3", "digit:3", "digit"), ("+", "op:+", "operator")),
    (("±", "sign", "function"), ("0", "digit:0", "digit"),
     (".", "decimal", "digit"), ("=", "equals", "equals")),
)
