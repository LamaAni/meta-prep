# Sort a large file by splitting into separate files?
import random
from typing import List, Tuple


def find_smallest(pairs: List[Tuple[int, int]]):
    # finds the first smallest
    min_pair = None
    for pair in pairs:
        if min_pair is None or min_pair[1] > pair[1]:
            min_pair = pair
    return min_pair


# Do this until we have no changes.
def sort_chunks(lst: List[int], k: int = 100):
    chunks: List[List[int]] = []

    def append_chunk(chunk):
        chunk.sort()
        # This will be save to disk.
        chunks.append(chunk)

    chunk: List[int] = []
    for v in lst:
        chunk.append(v)
        if len(chunk) == k:
            append_chunk(chunk)
            chunk = []

    if chunk:
        append_chunk(chunk)

    if len(chunks) == 1:
        return chunks[0]

    # Now we keep a vector index for each of the chunks
    # e.g. one value in memory
    cidx = [0] * len(chunks)

    # Need to find smallest values and get back its index.
    sorted_values = []
    while True:
        pairs = [
            (i, chunks[i][cidx[i]])
            for i in range(len(chunks))
            if cidx[i] < len(chunks[i])
        ]

        if len(pairs) == 0:
            break

        i, val = find_smallest(pairs)
        cidx[i] += 1
        sorted_values.append(val)

    return sorted_values


if __name__ == "__main__":
    lst = list(range(1000))
    random.shuffle(lst)
    print(sort_chunks(lst))
