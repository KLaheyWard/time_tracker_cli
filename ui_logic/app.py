import sys
from xml.dom import NotFoundErr
from constants.ui_consts import NEW, UPD
from services.time_service import TimeService
from ui.current_cycle_time_entries import CurrentCycleTimeEntries
from ui.time_summary_view import TimeSummaryView
from ui_logic.input_service import InputService
from utils.colour_logger import COLOURS, RESET, log

class App():
    def __init__(self, app_root):
        self.app_root = app_root
        # time service
        self.time_service = TimeService(app_root)
        self.input_service = InputService(app_root)

    def start(self):
        log(('\nFor all commands, enter: ',), ('help', 'cyan'))
        while True:
            self.show_entries()
            self.get_user_action()

    def show_entries(self):
        curr_entries = self.time_service.get_current_time_entries()
        banked = self.time_service.get_banks()
        print(CurrentCycleTimeEntries(curr_entries))
        print(TimeSummaryView(bank_list=banked, current_cycle_entries=curr_entries))

    def show_user_actions(self):
        print('-------------------------------------------------------')
        log(("\nActions","green", "underline", "bold"))
        log(
            ("\nAdd new time entry with all default values:",),
            ("\nnew", "cyan")
        )
        log(
            ("\nAdd new with custom values:",),
            ("\nnew -", "cyan"),
            ("<flag> <value>", "magenta")
        )
        log(
            ("\nUpdate a time entry:",),
            ("\nupd ", "cyan"),
            ("<entry ID> ", "magenta"),
            ("-", "cyan"),
            ("<flag> <value>", "magenta")
        )
        log(
            ("\nDelete a time entry:",),               # no color, style, bg
            ("\ndel ", "cyan"),               # text="del", color=cyan, style=bold
            ("<ID>", "magenta", "bold")                        # text="<ID>", color=cyan
        )
        
        log(("\nFlags","green", "underline", "bold"))
        log(('-start ', "cyan"), ('the start time in the format ',), ('HH', 'magenta'), (':', 'cyan'), ('MM', "magenta"))
        log(('-end ', 'cyan'), ('the end time in the format ',), ('HH', 'magenta'), (':', 'cyan'), ('MM', "magenta"))
        log(('-date ', 'cyan'), ('in the format ',), ('YYYY', "magenta"),('-','cyan'),('MM', 'magenta'), ("-", 'cyan'), ('DD', 'magenta'))
        log(('-break ', 'cyan'), ('the number of unpaid break minutes like ',), ('MM', 'magenta'))
        log(('-note ', 'cyan'), ('text to add to the notes for a time entry in the format ',), ('"', 'cyan'), ('<content for message>', 'magenta'), ('"', 'cyan'))
        log(('-type ', 'cyan'), ('options are ',) ,('regular', 'cyan'), (' or ',), ('holiday', 'cyan'))
        
        log(("\nExample command with flags","green", "underline", "bold"))
        log(('\nupd 5 -date 2025-12-25 -type holiday -note "Christmas day"', 'yellow'))
        print('\nThis updates time entry with ID of 5 to have a date of 2025-12-25 specifies it\'s a holiday, and adds a note "Christmas day" to the entry.\n')
        print('-------------------------------------------------------\n')

    def get_user_action(self):
        user_input = input(f"{COLOURS['green']}\nAction>{RESET}")
        self.process_input(user_input)
    
    def process_input(self, input_str : str):
        action,user_input_str = self.input_service.separate_cmd_from_flags(input_str)
        action = action.lower()
        
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
            print('\ninvalid id\n')
            return
            
        try:
            self.time_service.delete_time_entry(id)
        except NotFoundErr as nfe:
            print(f"\n{nfe}\n")
            
        
    def process_new_cycle(self):
        self.time_service.change_cycles()
        
    def process_new(self, user_input: list[str]):
        """Processes the 'new' command and the following flags."""
        try:
            flags_passed = self.input_service.parse(user_input)
        except ValueError as e:
            log(('\nInvalid entry', 'red'))
            log((f'{e}\n', 'red'))
            return
            
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
        if updated_entry is None:
            print(f'\nCould not find entry with id {id_to_upd}')
            return
        self.time_service.update_time_entry(updated_entry)
        
    
