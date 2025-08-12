from models.time_entry import TimeEntry
from constants.ui_consts import TE_WIDTH_MAPPING as WIDTH

class TimeEntryView():
    def __init__(self, time_entry : TimeEntry):
        self.id = f"{time_entry.id:>{WIDTH['id']}}"
        self.cycle_id = f"{time_entry.cycle_id:>{WIDTH['cycle_id']}}"
        self.unpaid_min = f"{time_entry.unpaid_break_min:>{WIDTH['up_break']}}"
        self.start_time = f"{self.format_time(time_entry.start_time):>{WIDTH['time']}}"
        self.end_time = f"{self.format_time(time_entry.end_time):>{WIDTH['time']}}"
        self.day_of_week = f"{self.format_day_of_week(time_entry.start_time):>{WIDTH['day_of_week']}}"
        self.date = f"{self.format_date(time_entry.start_time):>{WIDTH['date']}}"
        self.note = f"{time_entry.note or '':<{WIDTH['note']}}"
    
    def format_time(self, dt):
        return dt.strftime("%H:%M")
    
    def format_day_of_week(self, dt):
        return dt.strftime("%A")
    
    def format_date(self, dt):
        return dt.strftime("%Y-%m-%d")
        
    def __str__(self):
        return f"{self.id} {self.cycle_id} {self.day_of_week} {self.date} {self.start_time} {self.end_time} {self.unpaid_min} {self.note}"
    
    @staticmethod
    def headers():
        return (
        f"{'ID':<{WIDTH['id']}} "
        f"{'Cycle':<{WIDTH['cycle_id']}} "
        f"{'Day':<{WIDTH['day_of_week']}} "
        f"{'Date':<{WIDTH['date']}} "
        f"{'Start':<{WIDTH['time']}} "
        f"{'End':<{WIDTH['time']}} "
        f"{'Brk':<{WIDTH['up_break']}} "
        f"{'Note':<{WIDTH['note']}}"
    )