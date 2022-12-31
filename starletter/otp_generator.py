import random
def generate_otp():
    otp = random.randint(1000, 9999)
    print(otp, 'from generator')
    return otp
    