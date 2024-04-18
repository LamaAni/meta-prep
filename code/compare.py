# %% 
from functools import cmp_to_key

a = ["1", "23", "84", "9"]


def comp(x, y):
    if x + y == y + x:
        return 0
    if x + y > y + x:
        return -1
    return y


a.sort(key=cmp_to_key(comp))
print(a)

# %%
