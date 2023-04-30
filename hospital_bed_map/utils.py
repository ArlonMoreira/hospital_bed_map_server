import string, random, hashlib

def generate_hash_key():
    chars = string.ascii_lowercase+ string.digits
    chars_random = ''.join(random.choice(chars) for x in range(20))
    return str(hashlib.sha224(chars_random.encode('utf-8')).hexdigest())