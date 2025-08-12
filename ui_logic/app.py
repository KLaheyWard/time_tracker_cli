from datetime import datetime
from itertools import cycle
import os
from constants.consts import UNPAID_BREAK_MIN
from enums.day_type import DayTypeEnum
from models.cycle_storage import CycleStorage
from models.cycle_store import CycleStore
from models.file_handler import FileHandler
from models.file_storage import FileStorage
from models.time_entry_store import TimeEntryStore
from models.time_entry import TimeEntry
from ui.current_cycle_time_entries import CurrentCycleTimeEntries
from utils.input_parser import all_but_first
from utils.time_parser import smart_parse_datetime

NEW = 'new'
UPD = 'upd'

class App():
    def __init__(self, app_root):
        self.app_root = app_root
        # file handlers
        self.cycle_handler = FileHandler(os.path.join(
            self.app_root, 'data', 'current_cycle.txt'))
        self.time_entry_handler = FileHandler(
            os.path.join(self.app_root, 'data', 'time_entries.csv'))
        # storage
        self.cycle_storage = CycleStorage(self.cycle_handler)
        self.time_entry_storage = FileStorage(
            file_handler=self.time_entry_handler, model_cls=TimeEntry)
        # stores
        self.cycle_store = CycleStore(self.cycle_storage)
        self.time_entry_store = TimeEntryStore(self.time_entry_storage)

    def start(self):
        print('starting app')
        self.show_entries()
        self.get_user_action()

    def get_entries(self, cycle_id: int):
        return self.time_entry_store.get_all_entries()

    def show_entries(self):

        curr_cycle = int(self.cycle_store.get() or 0)
        curr_entries = self.get_entries(curr_cycle)
        print(CurrentCycleTimeEntries(curr_entries))

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
            

    def process_new(self, user_input: list[str]):
        current_cycle = int(self.cycle_store.get())
        last_id = self.time_entry_store.get_latest_id()
        next_id = int(last_id) + 1
        if (len(user_input)== 0):
            new_entry=TimeEntry(id=next_id, cycle_id=current_cycle, start_time=datetime.now())
        else:
            new_entry = self.create_time_entry_from_inputs(id=next_id, cycle_id=current_cycle, action=NEW, input_list=user_input)
        self.time_entry_store.add_entry(new_entry)
            
                    
    
    def create_time_entry_from_inputs(self,action: str, id:int, cycle_id: int, input_list: list[str]):
        if action != UPD and action != NEW:
            print(f'hmmmmm... not sure what you mean by {action}')
            return
        
        entry_type = DayTypeEnum.REGULAR
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
            new_start = f'{entry_date if entry_date else datetime.now().strftime("%H:%M")} {entry_start}' 
            new_end = None if not entry_end else f'{entry_date if entry_date else datetime.now().strftime("%H:%M")} {entry_end}' 
            return TimeEntry(id=id, cycle_id=cycle_id,start_time=new_start, end_time=new_end, unpaid_break_min=entry_break, note=entry_note, day_type=entry_type)
        else:
            old_entry : TimeEntry= self.time_entry_store.get_entry(id)
            old_date = old_entry.start_time.strftime("%Y-%m-%d")
            old_start = old_entry.start_time.strftime("%H:%M")
            old_end = old_entry.end_time.strftime("%H:%M")
            
            upd_date = f'{entry_date if entry_date else old_date}'
            upd_start = f'{upd_date} {entry_start if entry_start else old_start}'
            upd_end = f'{upd_date} {entry_end if entry_end else old_end}'
            return TimeEntry(id=id, cycle_id=cycle_id, start_time=upd_start, end_time=upd_end, note=entry_note, unpaid_break_min=entry_break, day_type=entry_type)
        
    def process_update(self, user_input: list[str]):
        id_to_upd = int(user_input[0])
        entry_to_upd : TimeEntry = self.time_entry_store.get_entry(id_to_upd)
        cycle = entry_to_upd.cycle_id
        
        rest_of_inputs = all_but_first(user_input)
        
        updated_entry = self.create_time_entry_from_inputs(id=id_to_upd, cycle_id=cycle, action=UPD, input_list=rest_of_inputs)
        self.time_entry_store.update_entry(id_to_upd,updated_entry)
