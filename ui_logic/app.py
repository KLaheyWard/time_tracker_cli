from datetime import datetime
from itertools import cycle
import os
import sys
from xml.dom import NotFoundErr
from constants.consts import UNPAID_BREAK_MIN
from constants.ui_consts import DATE_FORMAT, DATETIME_FORMAT, NEW, TIME_FORMAT, UPD
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
from ui_logic.input_service import InputService
from ui_logic.time_entry_parser import TimeEntryInputParser
from utils.input_parser import all_but_first
from utils.time_calculator import calculate_banked
from utils.time_parser import smart_parse_datetime


class App():
    def __init__(self, app_root):
        self.app_root = app_root
        # time service
        self.time_service = TimeService(app_root)
        self.input_service = InputService(app_root)

    def start(self):
        print('For all commands, enter: help')
        while True:
            self.show_entries()
            self.get_user_action()

    def show_entries(self):
        curr_entries = self.time_service.get_current_time_entries()
        banked = self.time_service.get_banks()
        print(CurrentCycleTimeEntries(curr_entries))
        print(TimeSummaryView(bank_list=banked, current_cycle_entries=curr_entries))

    def show_user_actions(self):
        print('Actions:')
        print(' Delete a time entry: del <ID>')
        print(' Add new without flags: new')
        print(' Add new with custom values: new -<flag> <value>')
        print(' Update a time entry: upd <entry ID> -<flag> <value>')
        print('\n Flags:')
        print(' -start the start time in the format HH:MM')
        print(' -end the end time in the format HH:MM')
        print(' -date in the format YYYY-MM-DD')
        print(' -break the number of unpaid break minutes like MM')
        print(' -note text with or without "')
        print(' -type with value of \"regular\" or \"holiday\"')
        print('\nExample command with flags')
        print('\n upd 5 -date 2025-12-25 -type holiday -note Christmas day')
        print('\n This updates time entry with ID of 5 to have a date of 2025-12-25')
        print(' specifies it\'s a holiday, and adds a note "Christmas day" to the entry.')
        print('\n')

    def get_user_action(self):
        user_input = input("\nAction>")
        self.process_input(user_input)
    
    def process_input(self, input_str : str):
        action,user_input_str = self.input_service.separate_cmd_from_flags(input_str)
        
        match action:
            case "upd":
                self.process_update(user_input_str)
            case "new":
                self.process_new(user_input_str)
            case "q":
                self.process_quit()   
            case "cyc":
                self.process_new_cycle()
            case "del":
                self.process_delete(user_input_str)
            case "help":
                self.show_user_actions()
            case _:
                print('\nNow sure I know that command...\n')
            
    def process_quit(self):
        print('\nGoodbye!')
        sys.exit(0)
    
    def process_delete(self, id_str):
        try:
            id = int(id_str.strip())
        except:
            print('invalid id')
            
        try:
            self.time_service.delete_time_entry(id)
        except NotFoundErr as nfe:
            print(f"\n{nfe}\n")
            
        
    def process_new_cycle(self):
        self.time_service.change_cycles()
        
    def process_new(self, user_input: list[str]):
        """Processes the 'new' command and the following flags."""
        flags_passed = self.input_service.parse(user_input)
        if (len(flags_passed) <= 0):
            self.time_service.new_blank_time_entry()
        else:
            new_entry = self.input_service.create_time_entry_from_inputs(id=0, cycle_id=0, action=NEW, inputs=flags_passed)
            self.time_service.new_time_entry(new_entry)
            
        
    def process_update(self, user_input_str: str):
        """Initial handling of the upd command by the user with all other user inputs provided."""
        id_to_upd, user_input_flags = self.input_service.separate_cmd_from_flags(user_input_str)
        id_to_upd = int(id_to_upd)
       
        input_dict = self.input_service.parse(user_input_flags)
        
        updated_entry = self.input_service.create_time_entry_from_inputs(id=id_to_upd, cycle_id=0, action=UPD, inputs=input_dict)
        self.time_service.update_time_entry(updated_entry)
        
    
