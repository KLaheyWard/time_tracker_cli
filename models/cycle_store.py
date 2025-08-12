from typing import Type
from models.abstract.single_value_store import SingleValueStoreAbs


class CycleStore(SingleValueStoreAbs):

    def __init__(self, storage: Type[SingleValueStoreAbs]):
        self.storage = storage
        
    def get(self):
        return self.storage.get()
    
    def update(self, new_value):
        self.update(new_value)    
        