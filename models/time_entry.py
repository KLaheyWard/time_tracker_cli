from datetime import date, datetime, time, timedelta
from constants.ui_consts import DATE_FORMAT, TIME_FORMAT
from models.abstract.entry_abs import EntryAbs
from utils.time_parser import smart_parse_datetime
from constants.consts import NUM_HOURS_HOLIDAY_DAY, UNPAID_BREAK_MIN, NUM_HOURS_IN_CYCLE, NUM_DAYS_IN_CYCLE
from enums.day_type import DayTypeEnum

class TimeEntry(EntryAbs):
    """The data for a single day's time entry."""
    def __init__(self, id:int, cycle_id: int, start_time: str | datetime, end_time: str=None, note: str = '', day_type: DayTypeEnum=DayTypeEnum.REGULAR.value, unpaid_break_min:str=UNPAID_BREAK_MIN):
        try:
            if isinstance(start_time, str):
                self.start_time : datetime = smart_parse_datetime(start_time)
            else: 
                self.start_time = start_time
            if end_time != None:
                # used != None here because when end_time arg provided with None value, it evaluates as truthy?
                self.end_time : datetime = smart_parse_datetime(end_time)
            else: 
                self.end_time : datetime = self.determine_end_time_from_start(self.start_time, day_type)
        except ValueError as ve:
            # TODO: actually do something with this error
            print(ve)
        
        self._id = id
        self.cycle_id = cycle_id
        self.unpaid_break_min : int = unpaid_break_min or UNPAID_BREAK_MIN
        self.note : str = note or ''
        self.day_type = day_type
        
    @property
    def id(self):
        return self._id
    
    def set_id(self, new_id):
        self._id = int(new_id)
        
    @staticmethod
    def fields():
        return ["id", "cycle_id", "start_time", "end_time",
              "unpaid_break_min", "note", "day_type"]
        
    def determine_end_time_from_start(self, start_datetime, day_type : DayTypeEnum):
        # make sure the right num of time worked depending on the day type
        expected_min_worked = ((NUM_HOURS_IN_CYCLE / NUM_DAYS_IN_CYCLE) if day_type.lower() == DayTypeEnum.REGULAR.value else NUM_HOURS_HOLIDAY_DAY) * 60 + UNPAID_BREAK_MIN
        return start_datetime + timedelta(minutes=expected_min_worked)
        
    def get_minutes_worked(self):
        return self.end_time - self.start_time
    
    def __str__(self) -> str:
        start_str = self.start_time.strftime("%Y-%m-%d %H:%M")
        end_str = self.end_time.strftime("%Y-%m-%d %H:%M")
        return (f"TimeEntry(id: {self.id}, cycle_id: {self.cycle_id}, start: {start_str}, end: {end_str}, "
                f"day_type: {self.day_type}, unpaid_break_min: {self.unpaid_break_min}, "
                f"note: '{self.note}')")
        
    def update_time_entry(self, date_input: date | str = None, 
                      start_input: time | str = None, 
                      end_input: time | str = None):
        """
        Update self.start_time and self.end_time with:
        - date_input: str "YYYY-MM-DD" or datetime.date
        - start_input: str "HH:MM" or datetime.time
        - end_input: str "HH:MM" or datetime.time

        Rules:
        1. Preserve the original end time if not explicitly changed.
        2. Ensure end >= start. If end < start after updates, push end to next day.
        3. Start and end are at most 1 day apart.
        """

        # Strip seconds
        current_start = self.start_time.replace(second=0, microsecond=0)
        current_end = self.end_time.replace(second=0, microsecond=0)

        # --- Convert inputs ---
        if isinstance(date_input, str):
            new_date = datetime.strptime(date_input, DATE_FORMAT).date()
        elif isinstance(date_input, date):
            new_date = date_input
        else:
            new_date = None

        if isinstance(start_input, str):
            new_start_time = datetime.strptime(start_input, TIME_FORMAT).time()
        elif isinstance(start_input, time):
            new_start_time = start_input
        else:
            new_start_time = None

        if isinstance(end_input, str):
            new_end_time = datetime.strptime(end_input, TIME_FORMAT).time()
        elif isinstance(end_input, time):
            new_end_time = end_input
        else:
            new_end_time = None

        # --- Determine new start ---
        start_time = new_start_time or current_start.time()
        start_date = new_date or current_start.date()
        new_start = datetime.combine(start_date, start_time)

        # --- Determine new end ---
        if new_end_time is not None:
            # User explicitly set end time
            end_time = new_end_time
        else:
            # Keep original end time
            end_time = current_end.time()

        # If user changed date, we may need to adjust end's date to keep end >= start
        if new_date:
            end_date = new_date
            tentative_end = datetime.combine(end_date, end_time)
            if tentative_end < new_start:
                # push end to next day
                tentative_end += timedelta(days=1)
            new_end = tentative_end
        else:
            # Keep end's original date unless start pushes it before start
            tentative_end = datetime.combine(current_end.date(), end_time)
            if tentative_end < new_start:
                tentative_end += timedelta(days=1)
            new_end = tentative_end

        # --- Update instance ---
        self.start_time = new_start
        self.end_time = new_end
    
    