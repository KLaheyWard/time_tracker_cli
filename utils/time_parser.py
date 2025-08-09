from __future__ import annotations
from datetime import datetime, date

def smart_parse_datetime(s: str) -> datetime:
    """
    Parse a date/time string into a datetime using only the Python standard library.

    Supports:
      - Full datetime (several common formats)
      - Time-only -> combined with today's date
      - Shorthand numeric times: '830' -> 08:30, '83' -> 08:30
      - Optional AM/PM markers: '830p', '8 pm', '0830AM', etc.
    """
    s = s.strip()

    # --- 1) Fast path: ISO-ish formats Python already knows well
    try:
        # Handles 'YYYY-MM-DD', 'YYYY-MM-DD HH:MM[:SS[.ffffff]]', ISO 'T', etc.
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        pass

    # --- 2) Try a bunch of common datetime formats
    formats = [
        # Y-M-D
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d %I:%M %p",
        "%Y-%m-%d",
        # M/D/Y
        "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M", "%m/%d/%Y %I:%M %p", "%m/%d/%Y",
        # D/M/Y
        "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y %I:%M %p", "%d/%m/%Y",
        # Y/M/D
        "%Y/%m/%d %H:%M:%S", "%Y/%m/%d %H:%M", "%Y/%m/%d %I:%M %p", "%Y/%m/%d",
        # D-M-Y
        "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M", "%d-%m-%Y %I:%M %p", "%d-%m-%Y",
        # Month name variants
        "%b %d, %Y %H:%M:%S", "%b %d, %Y %H:%M", "%b %d, %Y %I:%M %p", "%b %d, %Y",
        "%B %d, %Y %H:%M:%S", "%B %d, %Y %H:%M", "%B %d, %Y %I:%M %p", "%B %d, %Y",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    # --- 3) Time-only attempts (use today's date for missing date)
    today = date.today()
    time_formats = [
        "%H:%M:%S", "%H:%M",
        "%I:%M:%S %p", "%I:%M %p", "%I %p",
        "%H",  # e.g., "9"
    ]
    for fmt in time_formats:
        try:
            t = datetime.strptime(s, fmt).time()
            return datetime.combine(today, t)
        except ValueError:
            continue

    # --- 4) Shorthand numeric times (optionally with am/pm suffix like 'p' or 'pm')
    lower = s.lower().replace(".", "").replace(" ", "")
    ampm = None
    if lower.endswith(("am", "pm", "a", "p")):
        if lower.endswith(("am", "pm")):
            ampm = lower[-2:]  # 'am' or 'pm'
            core = lower[:-2]
        else:
            ampm = {"a": "am", "p": "pm"}[lower[-1]]
            core = lower[:-1]
    else:
        core = lower

    if core.isdigit():
        h, m = _digits_to_hour_minute(core)
        if ampm:
            # Convert 12-hour to 24-hour
            if ampm == "am":
                if h == 12: h = 0
            else:  # pm
                if h < 12: h += 12
        try:
            return datetime.combine(today, datetime.strptime(f"{h:02d}:{m:02d}", "%H:%M").time())
        except ValueError:
            pass

    raise ValueError(f"Could not parse datetime from: {s!r}")

def _digits_to_hour_minute(d: str) -> tuple[int, int]:
    """
    Interpret digit-only shorthand time strings:
      '830' -> 8:30
      '0830' -> 08:30
      '83' -> 8:30
      '8' -> 8:00
    """
    n = len(d)
    if n == 4:          # HHMM
        return int(d[:2]), int(d[2:])
    elif n == 3:        # HMM
        return int(d[0]), int(d[1:])
    elif n == 2:        # H? => H:(tens*10)
        return int(d[0]), int(d[1]) * 10
    elif n == 1:        # H
        return int(d), 0
    else:
        # Fallback: try last two as minutes, rest as hour (e.g., '12345' -> 123:45) if you want.
        raise ValueError("Unrecognized numeric time length.")
