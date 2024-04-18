n = 3


def advance(idxs, l):
    # advances the idxs internally to provide all posibilities
    # in an ordered list.
    for i in range(l - 1, -1, -1):
        max_i = n - l + i
        if idxs[i] < max_i:
            # can advance this index
            idxs[i] += 1
            # distance to end l-i
            # next new val idxs[i]+1
            if i < l - 1:
                # current value
                idxs[i + 1 :] = range(idxs[i] + 1, idxs[i] + l - i)
            return i
    return -1


nums = [1, 2, 3]

for l in range(n + 1):
    print(l)
    idxs = [i for i in range(l)]
    while True:
        print(idxs, [nums[i] for i in idxs])
        if advance(idxs, l) < 0:
            break
