import dis
from constants.consts import NUM_DAYS_IN_CYCLE, NUM_HOURS_IN_CYCLE
from constants.ui_consts import RELIEVED_EMOJI, ROCKET_EMOJI, SQUIGGLE_EMOJI
from models.bank import Bank
from models.time_entry import TimeEntry
from utils.time_calculator import calculate_hours_worked


class TimeSummaryView():
    def __init__(self, bank_list : list[Bank], current_cycle_entries: list[TimeEntry]):
        self.banks = bank_list
        self.entries = current_cycle_entries
        self.banked_min = self.get_total_min(self.banks, self.entries)
        
    def get_total_min(self, banks: list[Bank], entries: list[TimeEntry]):
        total_banked = 0
        total_worked_this_cycle = 0
        
        for bank in banks:
            total_banked += float(bank.banked_time)
        
        expected_min_per_day = (NUM_HOURS_IN_CYCLE * 60) / NUM_DAYS_IN_CYCLE
        for entry in entries:
            worked_min = round(calculate_hours_worked(entry.start_time, entry.end_time, entry.unpaid_break_min) * 60)
            total_worked_this_cycle += worked_min - expected_min_per_day
           
        total_worked_this_cycle = round(total_worked_this_cycle) 
        return total_banked + total_worked_this_cycle
    
    def display_banked(self, banked_time):
        time_owed_str = f"TIME OWED {SQUIGGLE_EMOJI}"
        even_time_str = f'All hours worked {RELIEVED_EMOJI}'
        extra_time_str = f'Worked extra {ROCKET_EMOJI}'
        # time calcs
        abs_min = abs(banked_time)
        hours = abs_min // 60
        minutes = abs_min % 60
        
        display_str = f'\n{time_owed_str if banked_time < 0 else even_time_str if banked_time == 0 else extra_time_str}\n'
        # all hours worked implies 0 hours and minutes to work.
        if hours == 0 and minutes == 0:
            return display_str
        return f'{display_str}{hours} hours and {minutes} min'
            
        
    def __str__(self):
        return self.display_banked(self.banked_min)