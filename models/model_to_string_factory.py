from __future__ import annotations
from typing import Any, Callable, Dict, Generic, List, TypeVar
import csv
import io

T = TypeVar("T")
Formatter = Callable[[Any], str]

class ModelToStringFactory(Generic[T]):
    """
    Convert a model instance into a delimited string (CSV by default).

    - fieldnames: order of fields in the output
    - formatters: optional per-field formatters (e.g., datetime -> '%Y-%m-%d %H:%M')
    - delimiter: CSV delimiter (default ',')
    - none_as_empty: if True, None -> '' ; else str(None)
    """
    def __init__(
        self,
        fieldnames: List[str],
        formatters: Dict[str, Formatter] | None = None,
        delimiter: str = ",",
        none_as_empty: bool = True,
    ):
        self.fieldnames = fieldnames
        self.formatters = formatters or {}
        self.delimiter = delimiter
        self.none_as_empty = none_as_empty

    def to_string(self, obj: T) -> str:
        """Serialize one model instance to a single CSV line (no trailing newline)."""
        row: Dict[str, str] = {}
        for name in self.fieldnames:
            val = getattr(obj, name, None)
            if val is None and self.none_as_empty:
                row[name] = ""
                continue
            fmt = self.formatters.get(name)
            if fmt:
                row[name] = fmt(val)
            else:
                # Nice default for Enums
                if hasattr(val, "name"):
                    row[name] = str(val.name)
                else:
                    row[name] = str(val)

        # Use csv.DictWriter to handle quoting/escaping
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=self.fieldnames, delimiter=self.delimiter, lineterminator="")
        # Write a single row without header
        writer.writerow(row)
        return buf.getvalue()
