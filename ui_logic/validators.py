from enums.day_type import DayTypeEnum


def validate_day_type(day_type_str):
    valid_day_type = False
    for dt in DayTypeEnum:
        if dt.value == day_type_str.strip().lower():
            valid_day_type = True
            
    return valid_day_type

