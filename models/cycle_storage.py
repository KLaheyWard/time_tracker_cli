
from models.abstract.single_value_storage import SingleValueStorageAbs
from models.file_handler import FileHandler


class CycleStorage(SingleValueStorageAbs):
    def __init__(self, file_handler: FileHandler):
        self.file_handler = file_handler

    def get(self):
        contents = self.file_handler.read_lines()
        return contents[0].strip()

    def update(self, new_value):
        self.file_handler.rewrite([new_value])