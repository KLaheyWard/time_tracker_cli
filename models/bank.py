from itertools import cycle
from models.abstract.entry_abs import EntryAbs


class Bank(EntryAbs):
    def __init__(self, id : int, cycle_id: int, banked_time:float):
        self._id = id
        self.cycle_id = cycle_id
        self.banked_time = banked_time
        
    @property
    def id(self):
        return self._id
    
    @staticmethod
    def fields():
        return ["id", "cycle_id", "banked_time"]
        