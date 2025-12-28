from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    GRAY = "gray"
    BRTRED = "bright red"
    BRTGREEN = "bright green"
    BRTYELLOW = "bright yellow"
    BRTBLUE = "bright blue"
    BRTMAGENTA = "bright magenta"
    BRTCYAN = "bright cyan"
    BRTWHITE = "bright white"

ANSI_COLORS = {
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
    "white": 37,
    "gray": 90,
    "bright red": 91,
    "bright green": 92,
    "bright yellow": 93,
    "bright blue": 94,
    "bright magenta": 95,
    "bright cyan": 96,
    "bright white": 97,
}

def color_text(text: str, color: Color) -> str:
    code = ANSI_COLORS.get(color.value)
    if code is None:
        return text
    return f"\033[{code}m{text}\033[0m"