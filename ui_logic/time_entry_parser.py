
from datetime import datetime

from constants.consts import UNPAID_BREAK_MIN
from constants.ui_consts import DATE_FORMAT, TIME_FORMAT
from enums import day_type
from utils.flag_parser import FlagParser


class TimeEntryInputParser():
    def __init__(self):
        parser = FlagParser()
        parser.register("start", dtype=self.parse_time, help_text="Start time HH:MM")
        parser.register("end", dtype=self.parse_time, help_text="End time HH:MM")
        parser.register("date", dtype=self.parse_date, help_text="Date YYYY-MM-DD")
        parser.register("break", dtype=int, default=UNPAID_BREAK_MIN, help_text="Unpaid break in minutes")
        parser.register("note", dtype=str, default='', help_text="Note about the work day")
        parser.register("type", dtype=str, default=day_type.DayTypeEnum.REGULAR.value, help_text='The Day Type for the work day')
        self.parser = parser
    
    def get(self):
        return self.parser
    
    def parse_time(self,time_str: str):
        try:
            return datetime.strptime(time_str, TIME_FORMAT).time()
        except ValueError:
            raise ValueError(f"Invalid time format: {time_str}")
    
    def parse_date(self, date_str: str):
        try:
            return datetime.strptime(date_str, DATE_FORMAT).date()
        except ValueError:
            raise ValueError(f"Invalid date format: {date_str}")
    
        
