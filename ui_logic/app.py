from datetime import datetime
from itertools import cycle
import os
import sys
from constants.consts import UNPAID_BREAK_MIN
from constants.ui_consts import DATE_FORMAT, DATETIME_FORMAT, TIME_FORMAT
from enums.day_type import DayTypeEnum
from models.bank import Bank
from models.bank_store import BankStore
from models.cycle_storage import CycleStorage
from models.cycle_store import CycleStore
from models.file_handler import FileHandler
from models.file_storage import FileStorage
from models.time_entry_store import TimeEntryStore
from models.time_entry import TimeEntry
from services.time_service import TimeService
from ui.current_cycle_time_entries import CurrentCycleTimeEntries
from ui.time_summary_view import TimeSummaryView
from utils.input_parser import all_but_first
from utils.time_calculator import calculate_banked
from utils.time_parser import smart_parse_datetime

NEW = 'new'
UPD = 'upd'
CYCLE_CHANGE = 'cyc'
VIEW_CYCLE = 'view'

class App():
    def __init__(self, app_root):
        self.app_root = app_root
        # time service
        self.time_service = TimeService(app_root)

    def start(self):
        while True:
            self.show_entries()
            self.get_user_action()

    def show_entries(self):
        curr_entries = self.time_service.get_current_time_entries()
        banked = self.time_service.get_banks()
        print(CurrentCycleTimeEntries(curr_entries))
        print(TimeSummaryView(bank_list=banked, current_cycle_entries=curr_entries))

    def show_user_actions(self):
        print('showing actions')

    def get_user_action(self):
        user_input = input("Action>")
        self.process_input(user_input)

    def process_input(self, input_str):
        input_list = input_str.split(" ")
        action = (input_list[0] or '').lower()
        args = all_but_first(input_list)
        
        match action:
            case "upd":
                self.process_update(args)
            case "new":
                self.process_new(args)
            case "q":
                self.process_quit()   
            case "cyc":
                self.process_new_cycle()     
            
    def process_quit(self):
        print('\nGoodbye!')
        sys.exit(0)
        
    def process_new_cycle(self):
        self.time_service.change_cycles()
        
    def process_new(self, user_input: list[str]):
        if (len(user_input)== 0):
            self.time_service.new_blank_time_entry()
        else:
            new_entry = self.create_time_entry_from_inputs(id=0, cycle_id=0, action=NEW, input_list=user_input)
            self.time_service.new_time_entry(new_entry)
            
                    
    
    def create_time_entry_from_inputs(self,action: str, id:int, cycle_id: int, input_list: list[str]):
        """Handles filling in provided time entry data """
        if action != UPD and action != NEW:
            print(f'hmmmmm... not sure what you mean by {action}')
            return
        
        entry_type = DayTypeEnum.REGULAR.value
        entry_start = None
        entry_end = None
        entry_note = ''
        entry_break = UNPAID_BREAK_MIN
        entry_date = None
        
        for cmd in input_list:
            cmd = cmd.lower().strip()
            # only command w/o : is day type
            if cmd.find(':') == -1:
                if cmd == DayTypeEnum.REGULAR.value:
                    entry_type = DayTypeEnum.REGULAR.value
                elif cmd == DayTypeEnum.HOLIDAY.value:
                    entry_type = DayTypeEnum.HOLIDAY.value 
                else:
                    print(f'unknown command {cmd}')
            else:
                fld,val = cmd.split(':',1)
                
                match fld:
                    case 'start':
                        entry_start = val
                    case 'end':
                        entry_end = val
                    case 'note':
                        entry_note = val
                    case 'date':
                        entry_date = val
                    case 'break':
                        entry_break = val
        
        if action == NEW:
            return self.create_new_time_entry_from_input(entry_date=entry_date, entry_start=entry_start, entry_end=entry_end, entry_note=entry_note, entry_type=entry_type, entry_break=entry_break)
        else:
            return self.create_updated_time_entry_from_input(entry_date=entry_date, entry_start=entry_start, entry_end=entry_end, entry_note=entry_note, entry_type=entry_type, entry_break=entry_break)
        
    def process_update(self, user_input: list[str]):
        """Initial handling of the upd command by the user with all other user inputs provided."""
        id_to_upd = int(user_input[0])
        entry_to_upd : TimeEntry = self.time_service.get_time_entry(id_to_upd)
        
        rest_of_inputs = all_but_first(user_input)
        
        updated_entry = self.create_time_entry_from_inputs(id=id_to_upd, cycle_id=entry_to_upd.cycle_id, action=UPD, input_list=rest_of_inputs)
        self.time_service.update_time_entry(updated_entry)
        
    def create_new_time_entry_from_input(self, entry_date, entry_start, entry_end, entry_break, entry_note, entry_type):
        """Creates a time entry based on user inputs.
        
        start_time and end_time are made up of date + time.
        When a date is specifed, we want to use it, else, the current date will be that of datetime.now.
        If a start time is specified, that time will be used, if not then datetime.now will be used for the time portion.

        """
        # determine now
        now = self.time_service.get_now(as_str=True)
        # start datetime string
        new_start = f'{entry_date or now.strftime(DATE_FORMAT)} {entry_start or  now.strftime(TIME_FORMAT)}' 
        # end datetime string
        new_end = None if not entry_end else f'{entry_date or now.strftime(DATE_FORMAT)} {entry_end or now.strftime(TIME_FORMAT)}' 
        
        return TimeEntry(id=id, cycle_id=self.time_service.get_current_cycle(),start_time=new_start, end_time=new_end, unpaid_break_min=entry_break, note=entry_note, day_type=entry_type)
    
    def create_updated_time_entry_from_input(self,entry_date, entry_start, entry_end, entry_break, entry_note, entry_type):
        """Retrieves entry to update, updates the values that were provided by the user, and returns the updated TimeEntry."""
        # original entry that we will be updating
        old_entry : TimeEntry= self.time_service.get_time_entry(id)
        old_date = old_entry.start_time.strftime(DATE_FORMAT)
        old_start = old_entry.start_time.strftime(TIME_FORMAT)
        old_end = old_entry.end_time.strftime(TIME_FORMAT)
        
        # updated values - want to retain original value if no new value provided
        upd_date = f'{entry_date if entry_date else old_date}'
        upd_start = f'{upd_date} {entry_start if entry_start else old_start}'
        upd_end = f'{upd_date} {entry_end if entry_end else old_end}'
        
        return TimeEntry(id=id, cycle_id=old_entry.cycle_id, start_time=upd_start, end_time=upd_end, note=entry_note, unpaid_break_min=entry_break, day_type=entry_type)
