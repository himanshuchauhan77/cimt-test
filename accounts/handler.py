import re

def check_email_is_valid(email):
    print(email.lower())
    return re.fullmatch(r"[a-z0-9.]+@[a-z0-9]+\.[a-z]+",email.lower())

