import shlex
from datetime import datetime

class FlagParser:
    def __init__(self):
        self.flags = {}

    def register(self, name, dtype=str, default=None, required=False, validator=None, is_bool=False, help_text=None):
        """
        Register a new flag.
        :param name: flag name (without dash)
        :param dtype: type to cast the value to
        :param default: default value if flag not provided
        :param required: if True, must be provided
        :param validator: function(value) -> bool
        :param is_bool: if True, flag is a switch (present = True)
        """
        self.flags[name] = {
            "dtype": dtype,
            "default": default,
            "required": required,
            "validator": validator,
            "is_bool": is_bool,
            "help": help_text
        }

    def parse(self, input_line):
        """
        Parse a string like "-start 07:30 -end 18:30"
        Returns a dict with flag values.
        """
        tokens = shlex.split(input_line)
        results = {}
        # to know when to skip the value associated with the flag 
        skip_next = False

        for i, token in enumerate(tokens):
            if skip_next:
                skip_next = False
                continue

            if token.startswith("-"):
                key = token.lstrip("-")
                if key not in self.flags:
                    raise ValueError(f"Unknown flag: {token}")

                config = self.flags[key]

                if config["is_bool"]:
                    results[key] = True
                else:
                    if i + 1 >= len(tokens):
                        raise ValueError(f"Flag '{key}' expects a value")
                    raw_value = tokens[i + 1]

                    try:
                        value = config["dtype"](raw_value)
                    except ValueError:
                        raise ValueError(f"Invalid value for '{key}', expected {config['dtype'].__name__}")

                    if config["validator"] and not config["validator"](value):
                        raise ValueError(f"Validation failed for '{key}' with value {value}")

                    results[key] = value
                    skip_next = True

        # fill defaults and check required
        for key, config in self.flags.items():
            if key not in results:
                if config["default"] is not None:
                    results[key] = config["default"]
                elif config["required"]:
                    raise ValueError(f"Missing required flag: {key}")
                elif config["is_bool"]:
                    results[key] = False  # absent boolean flags = False

        return results
