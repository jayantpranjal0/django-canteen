import random


def generate_otp(n):
    string="0123456789"
    otp=""
    for i in range(n):
        otp+=string[random.randint(0,9)]
    return otp
