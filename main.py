from models.file_handler import FileHandler
from models.file_storage import FileStorage
from models.time_entry import TimeEntry
from models.time_entry_store import TimeEntryStore

# set up
time_entry_file_handler = FileHandler("./data/test_time_entry.csv")
time_entry_storage = FileStorage(time_entry_file_handler, TimeEntry)
store = TimeEntryStore(time_entry_storage)

if __name__ == '__main__':
    new_entry = TimeEntry(id=3, cycle_id=1, start_time="2025-08-20 5:34")
    store.add_entry(new_entry)


