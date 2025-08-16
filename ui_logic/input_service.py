from constants.consts import UNPAID_BREAK_MIN
from constants.ui_consts import DATE_FORMAT, NEW, TIME_FORMAT, UPD
from enums.day_type import DayTypeEnum
from models.time_entry import TimeEntry
from services.time_service import TimeService
from ui_logic.time_entry_parser import TimeEntryInputParser


class InputService():
    def __init__(self, app_root):
        self.te_parser = TimeEntryInputParser().get()
        self.time_service = TimeService(app_root)

    def parse(self, input_str:str):
        return self.te_parser.parse(input_str)
    
    def separate_cmd_from_flags(self, input_str: str):
        parts = input_str.split(' ', 1)
        try:
            action = parts[0]
        except:
            action = ''
        
        try:
            user_input_str = parts[1]
        except:
            user_input_str = ''
            
        return action, user_input_str\
            
    def create_time_entry_from_inputs(self,action: str, id:int, cycle_id: int, inputs: dict):
        """Handles filling in provided time entry data """
        if action != UPD and action != NEW:
            print(f'hmmmmm... not sure what you mean by {action}')
            return
        
        # Extract values from input_list
        entry_date = inputs.get("date")             # datetime.date
        entry_start = inputs.get("start")           # datetime.time
        entry_end = inputs.get("end")               # datetime.time
        entry_note = inputs.get("note", "")         # str, default ''
        entry_type = inputs.get("type", DayTypeEnum.REGULAR.value)  # str, default 'regular'
        entry_break = inputs.get("break", UNPAID_BREAK_MIN)  # int, default from constant
        
        if action == NEW:
            return self.create_new_time_entry_from_input(entry_date=entry_date, entry_start=entry_start, entry_end=entry_end, entry_note=entry_note, entry_type=entry_type, entry_break=entry_break)
        else:
            
            return self.create_updated_time_entry_from_input(id=id, entry_date=entry_date, entry_start=entry_start, entry_end=entry_end, entry_note=entry_note, entry_type=entry_type, entry_break=entry_break)
        
    def create_new_time_entry_from_input(self, entry_date, entry_start, entry_end, entry_break, entry_note, entry_type):
        """Creates a time entry based on user inputs.
        
        start_time and end_time are made up of date + time.
        When a date is specifed, we want to use it, else, the current date will be that of datetime.now.
        If a start time is specified, that time will be used, if not then datetime.now will be used for the time portion.

        """
        # determine now
        now = self.time_service.get_now()
        # start datetime string
        new_start = f'{entry_date or now.strftime(DATE_FORMAT)} {entry_start or  now.strftime(TIME_FORMAT)}' 
        # end datetime string
        new_end = None if not entry_end else f'{entry_date or now.strftime(DATE_FORMAT)} {entry_end or now.strftime(TIME_FORMAT)}' 
        
        return TimeEntry(id=id, cycle_id=self.time_service.get_current_cycle(),start_time=new_start, end_time=new_end, unpaid_break_min=entry_break, note=entry_note, day_type=entry_type)
    
    def create_updated_time_entry_from_input(self,id, entry_date, entry_start, entry_end, entry_break, entry_note, entry_type):
        """Retrieves entry to update, updates the values that were provided by the user, and returns the updated TimeEntry."""
        # original entry that we will be updating
        old_entry : TimeEntry= self.time_service.get_time_entry(id)
        # handle if entry not found
        old_date = old_entry.start_time.strftime(DATE_FORMAT)
        old_start = old_entry.start_time.strftime(TIME_FORMAT)
        old_end = old_entry.end_time.strftime(TIME_FORMAT)
        
        # updated values - want to retain original value if no new value provided
        upd_date = f'{entry_date if entry_date else old_date}'
        upd_start = f'{upd_date} {entry_start if entry_start else old_start}'
        upd_end = f'{upd_date} {entry_end if entry_end else old_end}'
        
        return TimeEntry(id=id, cycle_id=old_entry.cycle_id, start_time=upd_start, end_time=upd_end, note=entry_note, unpaid_break_min=entry_break, day_type=entry_type)