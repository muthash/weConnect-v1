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


def check_name(username):
    """ Method to check if username entered is valid """
    blank_input = username != ''
    stripname = username.strip()
    newname = re.sub(r'\s+', '', stripname)
    inline_space = len(newname) == len(username)
    namelength = len(username)
    length = namelength >= 6 and namelength <= 25
    if blank_input == inline_space == length:
        return True
    return False
