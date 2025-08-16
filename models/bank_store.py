
from typing import Type
from models.abstract.storage_abs import StorageAbs
from models.abstract.store_abs import StoreAbs
from models.bank import Bank


class BankStore(StoreAbs):

    def __init__(self, storage: Type[StorageAbs]):
        self.storage = storage

    def add_entry(self, entry: Bank):
        last_id = int(self.get_latest_id())
        entry.set_id(last_id + 1)
        self.storage.add(entry)

    def update_entry(self, id, new_entry: Bank):
        self.storage.update(id, new_entry)

    def delete_entry(self, id):
        return self.storage.delete(id)

    def get_entry(self, id):
        return self.storage.get(id)

    def get_all_entries(self):
        return self.storage.get_all()
    
    
    def get_latest_id(self):
        entries = self.storage.get_all()
        return 0 if len(entries) == 0 else max(entries, key=lambda entry: int(entry.id)).id
        