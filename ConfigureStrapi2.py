import os
import random
import string

def generate_random_string(length=32):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

# Generate two keys for APP_KEYS
app_keys = f"{generate_random_string()},{generate_random_string()}"

print(f"APP_KEYS=\"{app_keys}\"")