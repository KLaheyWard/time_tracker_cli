from __future__ import annotations
from typing import Any, Callable, Dict, Generic, List, Type, TypeVar
import csv
import io

T = TypeVar("T")
Converter = Callable[[str], Any]


class StringToModelFactory(Generic[T]):
    """
    Convert a delimited string into an instance of a given model class.

    - model_cls: The class to instantiate.
    - fieldnames: The names of the fields in the order they appear in the string.
    - converters: Optional per-field conversion functions.
    - delimiter: Defaults to ',' but can be changed.
    """

    def __init__(
        self,
        model_cls: Type[T],
        fieldnames: List[str],
        converters: Dict[str, Converter] | None = None,
        delimiter: str = ",",
    ):
        self.model_cls = model_cls
        self.fieldnames = fieldnames
        self.converters = converters or {}
        self.delimiter = delimiter

    def from_string(self, line: str) -> T:
        """Convert a single line string into a model instance."""
        reader = csv.reader(io.StringIO(line), delimiter=self.delimiter)
        row = next(reader, None)
        if row is not None:
            if len(row) != len(self.fieldnames):
                raise ValueError(
                    f"Column mismatch: expected {len(self.fieldnames)} fields, "
                    f"got {len(row)}."
                )

            kwargs: Dict[str, Any] = {}
            for field, value in zip(self.fieldnames, row):
                value = value.strip()
                if value == "":
                    kwargs[field] = None
                else:
                    converter = self.converters.get(field)
                    kwargs[field] = converter(value) if converter else value

            return self.model_cls(**kwargs)
