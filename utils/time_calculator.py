from datetime import datetime
from constants.consts import NUM_HOURS_IN_CYCLE, UNPAID_BREAK_MIN
from models.time_entry import TimeEntry


def calculate_min_worked(start : datetime, end : datetime, unpaid_break_min:int):
    # make sure its an int
    unpaid_break_min = int(unpaid_break_min)
    worked_seconds_with_break = (end - start).total_seconds()
    worked_seconds_minus_break = worked_seconds_with_break - (unpaid_break_min * 60)
    worked_min = max(worked_seconds_minus_break / 60, 0)
    return round(worked_min)

def calculate_banked(time_entries: list[TimeEntry]):
    """
    Returns negative if I owe time, positive if I've worked extra time.
    """
    total_worked = 0
    
    for entry in time_entries:
        worked = calculate_min_worked(entry.start_time, entry.end_time, entry.unpaid_break_min)
        total_worked += worked
    
    return total_worked - (NUM_HOURS_IN_CYCLE * 60)
