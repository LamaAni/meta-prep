import os
import random
import string

from utils.logs import REPO_PATH

LOCAL = os.path.join(REPO_PATH, ".local", "file_reader")
os.makedirs(LOCAL, exist_ok=True)


def line_gen():
    while True:
        yield str(random.randint(0, 10000)) + " " + "".join(
            random.choices(string.ascii_letters + string.digits, k=20)
        )


file_names = [os.path.join(LOCAL, base + ".txt") for base in ["a", "b", "c", "d", "e"]]


gen = line_gen()
line_count = 10000
for fn in file_names:
    with open(fn, "w", encoding="utf-8") as raw:
        lines = [next(gen) for _ in range(line_count)]
        raw.write("\n".join(lines))
