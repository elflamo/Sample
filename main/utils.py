import random, string

def generate_unique_key(length):
    return ''.join(random.choice(string.digits) for _ in range(length))