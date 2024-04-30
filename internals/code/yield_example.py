import random
import string


def line_gen():
    while True:
        yield "".join(random.choices(string.ascii_letters + string.digits, k=20))


gen = line_gen()
idx = 0
for row in line_gen():
    print(row)
    idx += 1
    if idx == 100:
        break
