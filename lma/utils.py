import secrets
from string import digits, ascii_lowercase


def generate_random(length, only_numbers=True):
    if only_numbers:
        random_value = ''.join(secrets.choice(digits) for i in range(length))
    else:
        random_value = ''.join(secrets.choice(ascii_lowercase) for i in range(length))

    return random_value
