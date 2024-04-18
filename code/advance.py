from itertools import combinations

n = 8


# Should give all permutations of the index.
def advance(idxs) -> int:
    # returns the index of the change
    # advance the sidx to the next possible value
    # 0256789 -> 0345678
    li = len(idxs)

    # from end
    for i in range(li - 1, -1, -1):
        if i == li - 1:
            if idxs[i] < n - 1:
                idxs[i] += 1
                return i
            continue

        if idxs[i] + 1 < idxs[i + 1]:
            idxs[i] += 1
            idxs[i + 1 :] = range(idxs[i] + 1, idxs[i] + li - i)
            return i
    return -1


l = n // 2
possible = set()
idxs = list(range(l))
while True:
    possible.add(tuple(idxs))
    print(idxs)
    if advance(idxs) < 0:
        break

print("--")

for comb in combinations(range(n), l):
    if comb not in possible:
        print(f"missing {comb}")
