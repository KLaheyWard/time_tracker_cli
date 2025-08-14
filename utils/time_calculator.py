from datetime import datetime
from constants.consts import NUM_HOURS_IN_CYCLE, UNPAID_BREAK_MIN
from models.time_entry import TimeEntry


def calculate_hours_worked(start : datetime, end : datetime, unpaid_break_min:int):
    # make sure its an int
    unpaid_break_min = int(unpaid_break_min)
    worked_seconds_with_break = (end - start).total_seconds()
    worked_seconds_minus_break = worked_seconds_with_break - (unpaid_break_min * 60)
    worked_hours = max(worked_seconds_minus_break / 3600, 0)
    return round(worked_hours, 2)

def calculate_banked(time_entries: list[TimeEntry]):
    """
    Returns negative if I owe time, positive if I've worked extra time.
    """
    total_worked = 0
    
    for entry in time_entries:
        worked = calculate_hours_worked(entry.start_time, entry.end_time, entry.unpaid_break_min)
        total_worked += worked
    
    return total_worked - NUM_HOURS_IN_CYCLE
