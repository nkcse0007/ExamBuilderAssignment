import re


def isValidEmail(email):
    if re.match(
            "^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$",
            email) != None:
        if (len(email) > 5) and (len(email) < 40):
            return True
        else:
            return False
    else:
        return False


import phonenumbers


def isValidPhone(phone):
    try:
        z = phonenumbers.parse(phone, None)
    except:
        return {'message': 'country code is required'}, False
    if phonenumbers.is_valid_number(z):
        return {'message': ''}, True
    else:
        return {'message': ''}, False


def isFbValidPhone(phone):
    if 15 > len(phone) > 9:
        try:
            hello = int(phone)
            return True
        except:
            return False
    else:
        return False
