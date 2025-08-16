from csv import Error
from datetime import datetime
import os
from xml.dom import NotFoundErr
from constants.ui_consts import DATETIME_FORMAT
from models.bank import Bank
from models.bank_store import BankStore
from models.cycle_storage import CycleStorage
from models.cycle_store import CycleStore
from models.file_handler import FileHandler
from models.file_storage import FileStorage
from models.time_entry import TimeEntry
from models.time_entry_store import TimeEntryStore
from utils.time_calculator import calculate_banked


class TimeService():
    def __init__(self, app_root):
        self.app_root = app_root
        # file handlers
        self.cycle_handler = FileHandler(os.path.join(
            self.app_root, 'data', 'current_cycle.txt'))
        self.time_entry_handler = FileHandler(
            os.path.join(self.app_root, 'data', 'time_entries.csv'))
        self.bank_handler = FileHandler(os.path.join(self.app_root, 'data', 'time_bank.csv')
                                        )
        # storage
        self.cycle_storage = CycleStorage(self.cycle_handler)
        self.time_entry_storage = FileStorage(
            file_handler=self.time_entry_handler, model_cls=TimeEntry, string_formatters={ "start_time": lambda dt: dt.strftime("%Y-%m-%d %H:%M"),
        "end_time": lambda dt: dt.strftime(DATETIME_FORMAT),})
        self.bank_storage = FileStorage(file_handler=self.bank_handler, model_cls=Bank)
        # stores
        self.cycle_store = CycleStore(self.cycle_storage)
        self.time_entry_store = TimeEntryStore(self.time_entry_storage)
        self.bank_store = BankStore(self.bank_storage)
    
    def get_time_entry(self, id: int | str):
        return self.time_entry_store.get_entry(id)
    
    def get_current_cycle(self):
        return int(self.cycle_store.get() or 0)
    
    def get_banks(self):
        return self.bank_store.get_all_entries()
    
    def change_cycles(self):
        current_cycle = self.get_current_cycle()
        next_cycle = current_cycle + 1
        self.cycle_store.update(next_cycle)
        cycle_entries = self.get_time_entries_for_cycle(current_cycle)
        time_to_bank = calculate_banked(cycle_entries)
        next_id = int(self.bank_store.get_latest_id())
        self.bank_store.add_entry(Bank(id=next_id, cycle_id=current_cycle, banked_min=time_to_bank))
    
    def new_blank_time_entry(self):
        current_cycle = self.get_current_cycle()
        next_id = self.next_time_entry_id()
        
        new_entry=TimeEntry(id=next_id, cycle_id=current_cycle, start_time=self.get_now(as_str=True))
        
        self.time_entry_store.add_entry(new_entry)
        
    def new_time_entry(self, time_entry: TimeEntry):
        current_cycle = self.get_current_cycle()
        next_id = self.next_time_entry_id()
        time_entry.set_id(next_id)
        time_entry.cycle_id = current_cycle
        self.time_entry_store.add_entry(time_entry)
        
    def get_time_entries_for_cycle(self, cycle_id: int):
        return [entry for entry in self.time_entry_store.get_all_entries() if int(entry.cycle_id) == cycle_id]

    def get_current_time_entries(self):
        cycle_id = self.get_current_cycle()
        return [entry for entry in self.time_entry_store.get_all_entries() if int(entry.cycle_id) == cycle_id]

    def get_now(self, as_str = False):
        now = datetime.now()
        if as_str:
            return now.strftime(DATETIME_FORMAT)
        return now
    
    def next_time_entry_id(self):
        last_id = self.time_entry_store.get_latest_id()
        return int(last_id) + 1
    
    def update_time_entry(self, updated_entry:TimeEntry):
        self.time_entry_store.update_entry(updated_entry.id, updated_entry)
        
    def delete_time_entry(self, entry_id):
        exists = self.time_entry_store.get_entry(entry_id)
        if not exists:
            raise NotFoundErr(f"Could not find entry with id {entry_id}")
        self.time_entry_store.delete_entry(entry_id)