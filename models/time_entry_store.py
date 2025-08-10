from typing import Type
from models.abstract.storage_abs import StorageAbs
from models.abstract.store_abs import StoreAbs
from models.time_entry import TimeEntry


class TimeEntryStore(StoreAbs):

    def __init__(self, storage: Type[StorageAbs]):
        self.storage = storage

    def add_entry(self, entry: TimeEntry):
        self.storage.add(entry)

    def update_entry(self, id, new_entry: TimeEntry):
        self.storage.update(id, new_entry)

    def delete_entry(self, id):
        return self.storage.delete(id)

    def get_entry(self, id):
        return self.storage.get(id)

    def get_all_entries(self):
        return self.storage.get_all()
