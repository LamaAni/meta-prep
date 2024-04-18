def advance_index(idxs, l, n):
    # advance the index l, up to n
    # e.g. n=6
    # 0123
    # 0124
    # 0125
    # 0134
    # ...

    for i in range(l - 1, -1, -1):
        if i < l - 1 and idxs[i] + 1 >= idxs[i + 1]:
            # already ascending
            continue
        elif idxs[i] >= n - 1:
            # we are at the max value, cannot advance more.
            continue

        # advance the index
        idxs[i] += 1
        # reset the following indexs to an ascending series.
        if i < l - 1:
            idxs[i + 1 :] = range(idxs[i] + 1, idxs[i] + l - i)
        return i
    return -1


count = 1
idxs = [0, 1, 2]
n = 3000
while advance_index(idxs, len(idxs), n):
    count += 1
print(count)

# nums = [1, 2, 2, 3]
# n = len(nums)
# possible = set()
# for l in [2]:  # range(n + 1):
#     idxs = list(range(l))
#     while True:
#         possible.add(tuple(idxs))
#         print(idxs)
#         if advance_index(idxs, l, n) < 0:
#             break
