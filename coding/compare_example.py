from functools import cmp_to_key


def comp_func(a, b):
    if a[0]>b[0]:
        return 1
    if a[0]<b[0]:
        return -1
    if a[1] > b[1]:
        return 1
    if a[1] < b[1]:
        return -1
    return 0


a = [(0, "a"), (3,"a"), (2, "a"), (1, "a"), (0, "b")]
a.sort(key=cmp_to_key(comp_func))
print(a)
