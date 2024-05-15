import random


def get_code():
    gen_num = "".join(str(random.randrange(10)) for _ in range(6))
    return gen_num


def check_code(user):
    return ""
