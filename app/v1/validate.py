import re


def check_email(email):
    """ Method to check if email entered is valid """
    blank_input = email != ''
    stripmail = email.strip()
    newmail = re.sub(r'\s+', '', stripmail)
    inline_space = len(newmail) == len(email)
    regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9]+\.[a-zA-Z0-9-.]+$)"
    pattern = bool(re.search(regex, email))
    if blank_input == inline_space == pattern:
        return True
    return False


def check_name(name):
    """ Method to check if username entered is valid """
    blank_input = name != ''
    stripname = name.strip()
    newname = re.sub(r'\s+', '', stripname)
    namelength = len(newname)
    if blank_input and namelength > 0:
        return True
    return False
