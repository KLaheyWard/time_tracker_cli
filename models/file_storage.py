from typing import Dict, Type
from models.abstract.entry_abs import EntryAbs
from models.abstract.storage_abs import StorageAbs
from models.file_handler import FileHandler
from models.model_to_string_factory import Formatter, ModelToStringFactory
from models.string_to_model_factory import StringToModelFactory


class FileStorage(StorageAbs):

    def __init__(self, file_handler: FileHandler, model_cls: Type[EntryAbs], string_formatters: Dict[str, Formatter] | None = None):
        super().__init__()
        self.file_handler = file_handler
        self.model_cls = model_cls
        self.str_factory = ModelToStringFactory(fieldnames=model_cls.fields(), formatters=string_formatters)
        self.model_factory = StringToModelFactory(
            model_cls=self.model_cls, fieldnames=self.model_cls.fields())

    def add(self, new_entry):
        transformed_entry = self.str_factory.to_string(new_entry)
        self.file_handler.write_line(transformed_entry)

    def update(self, id, new_entry):
        all_lines = self.file_handler.read_lines()
        all_entries = [self.model_factory.from_string(
            line) for line in all_lines]
        updated_lines = []

        for i in range(len(all_entries)):
            if int(id) == int(all_entries[i].id):
                updated_lines.append(self.str_factory.to_string(new_entry))
            else:
                updated_lines.append(all_lines[i])

        self.file_handler.rewrite(updated_lines)

    def delete(self, id):
        all_lines = self.file_handler.read_lines()
        all_entries = [self.model_factory.from_string(
            line) for line in all_lines]
        updated_lines = []

        for i in range(len(all_entries)):
            if int(id) != int(all_entries[i].id):
                updated_lines.append(all_lines[i])

        self.file_handler.rewrite(updated_lines)

    def get(self, id):
        if isinstance(id, str):
            id = int(id)
        all_lines = self.file_handler.read_lines()
        all_entries = [self.model_factory.from_string(
            line) for line in all_lines]
       
        return next((entry for entry in all_entries if int(entry.id) == id), None)
  

    def get_all(self):
        all_lines = self.file_handler.read_lines()
        return [self.model_factory.from_string(
            line) for line in all_lines]