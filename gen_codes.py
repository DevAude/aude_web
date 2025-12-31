# gen_codes.py
import random
import string

def generate_code() -> str:
    letters = random.choices(string.ascii_lowercase, k=4)
    digits = random.choices(string.digits, k=3)
    code_chars = letters + digits
    random.shuffle(code_chars)
    return "".join(code_chars)

def generate_many(n: int):
    return [generate_code() for _ in range(n)]

if __name__ == "__main__":
    for c in generate_many(20):
        print(c)
