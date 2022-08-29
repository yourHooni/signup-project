import re

validate_dict = {
    "email": r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
    "password": r'(?=.*\d)(?=.*[a-z]).{8,}'
}


def check_validate(pattern_name, value):
    """Value validation for pattern name"""
    pattern = re.compile(validate_dict[pattern_name])
    return bool(pattern.match(value))
