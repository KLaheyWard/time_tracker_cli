import os
from typing import List


class FileHandler:
    def __init__(self, filepath: str, encoding: str = "utf-8"):
        """
        Initialize FileWriter.

        :param filepath: Path to the file to write to.
        :param encoding: File encoding. Default is utf-8.
        """
        self.filepath = filepath
        self.encoding = encoding
        # Ensure the file exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        open(self.filepath, "a", encoding=self.encoding).close()
        # Open the file
        self.file = open(self.filepath, 'a', encoding=self.encoding)

    def write_line(self, line: str):
        """Write a single line to the file, adding a newline."""
        self.ensure_newline_at_end()
        if not line.endswith("\n"):
            line += "\n"
            self.file.write(line)
            self.file.flush()

    def rewrite(self, lines: list[str]):
        """
        Completely overwrite the file with new lines.
        Ensures each line ends with a newline.
        Keeps the file open afterward in append mode.
        """
        self.file.close()
        with open(self.filepath, "w", encoding=self.encoding) as f:
            for line in lines:
                if not line.endswith("\n"):
                    line += "\n"
                f.write(line)
        # Reopen in append mode for further writes
        self.file = open(self.filepath, "a", encoding=self.encoding)

    def read_lines(self) -> List[str]:
        """Read all lines from the file and return them as a list of strings (no newline stripping)."""
        with open(self.filepath, "r", encoding=self.encoding) as f:
            return f.readlines()

    def close(self):
        """Close the file."""
        if not self.file.closed:
            self.file.close()
                    

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        
    def ensure_newline_at_end(self):
        """Ensure the file ends with a newline character."""
        self.file.flush()  # Make sure all writes are saved
        with open(self.filepath, "rb+") as f:
            f.seek(0, 2)  # Move to end of file
            if f.tell() == 0:
                return  # Empty file, nothing to do
            f.seek(-1, 2)  # Go to last byte
            last_char = f.read(1)
            if last_char != b"\n":
                f.write(b"\n")