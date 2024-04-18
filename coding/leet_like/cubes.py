# %%
from functools import reduce


def can_stack_cubes(cubes: list, parent_cube: int = None) -> bool:
    # Need to determine which to start with, since
    # the either we would have left on right or reverse at
    # some point, take the larger

    parent_cube = cubes.pop(0 if cubes[0] > cubes[-1] else -1)

    for _ in range(len(cubes)):
        print(parent_cube, "|", cubes[0], cubes[-1])
        if cubes[0] > parent_cube and cubes[-1] > parent_cube:
            return False

        pop_idx = -1

        if cubes[0] <= parent_cube and cubes[0] > cubes[-1]:
            pop_idx = 0
        elif cubes[-1] > parent_cube:
            pop_idx = 0
        parent_cube = cubes.pop(pop_idx)

    return True


print(can_stack_cubes([4, 3, 2, 1, 3, 4]))
print(can_stack_cubes([1, 2, 3, 7, 8]))
print(can_stack_cubes([1, 2, 3, 8, 7]))
print(can_stack_cubes([1, 3, 2]))

# %%
arr = [1, 2, 3, 4]
print(reduce(lambda x, y: x + y, arr))


def show_item(x, y):
    print(x, y)
    return x + y


print(reduce(show_item, arr, -3))

# %%
from fractions import Fraction

a = Fraction(1, 3)
b = Fraction(1, 3)
c = Fraction(1, 3)
d = Fraction(3, 1)
print(reduce(lambda x, y: x * y, [a, b, c,d]))
