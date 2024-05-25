import os
import random
import string

def generate_random_string(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

keys = [
    "APP_KEYS",
    "API_TOKEN_SALT",
    "ADMIN_JWT_SECRET",
    "JWT_SECRET",
    "TRANSFER_TOKEN_SALT"
]

for key in keys:
    print(f"{key}={generate_random_string()}")