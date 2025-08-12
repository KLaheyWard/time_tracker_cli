from models.time_entry import TimeEntry
from ui.time_entry_view import TimeEntryView


class CurrentCycleTimeEntries():
    
    def __init__(self, time_entries: list[TimeEntry]):
        self.entries = time_entries
        
    def __str__(self):
        if len(self.entries) <= 0: 
            return 'There are no time entries!'
        result = TimeEntryView.headers() + '\n'
        for entry in self.entries:
            result = result + f"{TimeEntryView(entry)}\n"
            
        return result