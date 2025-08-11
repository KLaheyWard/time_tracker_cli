from models.abstract.cycle_store import SingleValueStorageAbs
from models.file_handler import FileHandler


class CycleStorage(SingleValueStorageAbs):
    def __init__(self):
        self.file_handler = FileHandler('/data/current_cycle.txt')

    def get():
        raise NotImplementedError("Must implement SingleValueStorageAbs.get()")

    def update(new_value):
        raise NotImplementedError(
            "Must implement SingleValueStorageAbs.update()")
