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


def color_text(str_phrase: str, color: Color) -> str:
    match color.value:
        case "red":
            return f"\033[31m{str_phrase}\033[0m"
        case "green":
            return f"\033[32m{str_phrase}\033[0m"
        case "yellow":
            return f"\033[33m{str_phrase}\033[0m"
        case "blue":
            return f"\033[34m{str_phrase}\033[0m"
        case "magenta":
            return f"\033[35m{str_phrase}\033[0m"
        case "cyan":
            return f"\033[36m{str_phrase}\033[0m"
        case "white":
            return f"\033[37m{str_phrase}\033[0m"
        case "gray":
            return f"\033[90m{str_phrase}\033[0m"
        case "bright red":
            return f"\033[91m{str_phrase}\033[0m"
        case "bright green":
            return f"\033[92m{str_phrase}\033[0m"
        case "bright yellow":
            return f"\033[93m{str_phrase}\033[0m"
        case "bright blue":
            return f"\033[94m{str_phrase}\033[0m"
        case "bright magenta":
            return f"\033[95m{str_phrase}\033[0m"
        case "bright cyan":
            return f"\033[96m{str_phrase}\033[0m"
        case "bright white":
            return f"\033[97m{str_phrase}\033[0m"
