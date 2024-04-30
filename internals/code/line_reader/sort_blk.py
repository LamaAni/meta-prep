import os
from functools import cmp_to_key

from utils.logs import REPO_PATH

LOCAL = os.path.join(REPO_PATH, ".local", "file_reader")
file_names = [os.path.join(LOCAL, base + ".txt") for base in ["a", "b", "c", "d", "e"]]

sorted_file_name = os.path.join(LOCAL, "sorted.txt")


def file_line_gen(fn: str):
    with open(fn, "r", encoding="utf-8") as raw:
        for ln in raw:
            yield ln


def sort_file(fn: str):
    with open(fn, "r", encoding="utf-8") as raw:
        lines = [ln.strip() for ln in raw.read().split("\n") if ln.strip()]

    lines.sort(key=cmp_to_key(compare_lines))

    with open(fn, "w", encoding="utf-8") as raw:
        raw.write("\n".join(lines))


def compare_lines(a: str, b: str):
    return int(a.split(" ")[0]) - int(b.split(" ")[0])


def blk_merge_sorts():
    active_files = set(file_names)
    gen_by_name = {fn: file_line_gen(fn) for fn in active_files}
    batch = {}

    for fn in active_files:
        sort_file(fn)

    def fill_batch(fn=None):
        to_fill = None
        if fn is not None:
            to_fill = [fn]
        else:
            to_fill = [fn for fn in active_files if fn not in batch]
        for fn in to_fill:
            while True:
                val = next(gen_by_name[fn], None)
                if val is None:
                    # batch ended.
                    active_files.remove(fn)
                    batch.pop(fn)
                    break
                if val:
                    batch[fn] = val
                    break

    def batch_next():
        min_ln = None
        min_fn = None
        for fn, ln in batch.items():
            if min_fn is None or compare_lines(ln, min_ln) < 0:
                min_fn = fn
                min_ln = ln

        fill_batch(min_fn)

        return min_fn, min_ln

    fill_batch()

    with open(sorted_file_name, "w") as sorted:
        while active_files:
            _, ln = batch_next()
            sorted.write(ln)


blk_merge_sorts()
