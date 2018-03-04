import re


def check_email(email):
    """ Method to check if email entered is valid """
    blank_input = email != ''
    newmail = email.strip()
    inline_space = len(newmail) == len(email)
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"
    pattern = bool(re.search(regex, email))
    if blank_input == inline_space == pattern:
        return True
    return False


