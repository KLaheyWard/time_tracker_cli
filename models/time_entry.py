from datetime import datetime, timedelta
from models.abstract.entry_abs import EntryAbs
from utils.time_parser import smart_parse_datetime
from constants.consts import UNPAID_BREAK_MIN, NUM_HOURS_IN_CYCLE, NUM_DAYS_IN_CYCLE
from enums.day_type import DayTypeEnum

class TimeEntry(EntryAbs):
    """The data for a single day's time entry."""
    def __init__(self, id:int, cycle_id: int, start_time: str | datetime, end_time: str=None, note: str = '', day_type: DayTypeEnum=DayTypeEnum.REGULAR, unpaid_break_min:str=UNPAID_BREAK_MIN):
        try:
            if isinstance(start_time, str):
                self.start_time : datetime = smart_parse_datetime(start_time)
            else: 
                self.start_time = start_time
            if end_time:
                self.end_time : datetime = smart_parse_datetime(end_time)
            else: 
                self.end_time : datetime = self.determine_end_time_from_start(self.start_time)
        except ValueError as ve:
            # TODO: actually do something with this error
            print(ve)
        
        self._id = id
        self.cycle_id = cycle_id
        self.unpaid_break_min : int = unpaid_break_min
        self.note : str = note
        self.day_type = day_type
        
    @property
    def id(self):
        return self._id
        
    @staticmethod
    def fields():
        return ["id", "cycle_id", "start_time", "end_time",
              "unpaid_break_min", "note", "day_type"]
        
    def determine_end_time_from_start(self, start_datetime):
        expected_min_worked = (NUM_HOURS_IN_CYCLE / NUM_DAYS_IN_CYCLE) * 60
        return start_datetime + timedelta(minutes=expected_min_worked)
        
    def get_minutes_worked(self):
        return self.end_time - self.start_time
    
    def __str__(self) -> str:
        start_str = self.start_time.strftime("%Y-%m-%d %H:%M")
        end_str = self.end_time.strftime("%Y-%m-%d %H:%M")
        return (f"TimeEntry(id: {self.id}, cycle_id: {self.cycle_id}, start: {start_str}, end: {end_str}, "
                f"day_type: {self.day_type}, unpaid_break_min: {self.unpaid_break_min}, "
                f"note: '{self.note}')")
    
    