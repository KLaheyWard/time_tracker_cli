RESET = "\033[0m"
STYLES = {"bold": "\033[1m", "underline": "\033[4m"}
COLOURS = {
    "black": "\033[30m", "red": "\033[31m", "green": "\033[32m",
    "yellow": "\033[33m", "blue": "\033[34m", "magenta": "\033[35m",
    "cyan": "\033[36m", "white": "\033[37m",
    # bright colors
    "bright_black": "\033[90m", "bright_red": "\033[91m",
    "bright_green": "\033[92m", "bright_yellow": "\033[93m",
    "bright_blue": "\033[94m", "bright_magenta": "\033[95m",
    "bright_cyan": "\033[96m", "bright_white": "\033[97m"
}

def log(*parts):
    line = ""
    for p in parts:
        # Plain string
        if isinstance(p, str):
            line += p
            continue

        # Tuple
        text = p[0] if len(p) > 0 else ""
        colour = p[1] if len(p) > 1 else None
        style = p[2] if len(p) > 2 else None
        bg = p[3] if len(p) > 3 else None

        styled = ""
        if style in STYLES:
            styled += STYLES[style]
        if colour in COLOURS:
            styled += COLOURS[colour]
        # TODO: add background if needed
        styled += text + RESET
        line += styled
    print(line)
