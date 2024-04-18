# %%
# Design and generate random minesweeper boards
import random
from typing import List

# Input:
# n,m rows and columns
# number of bombs


def generate_minesweeper_board(
    n: int,
    m: int,
    bombs: int,
    empty_symbol="E",
    bomb_symbol="B",
) -> List[List[str]]:
    # TODO: Validate inputs
    assert n > 0 and m > 0, ValueError(
        "Both board height (n) and board width (m) must be larger then zero"
    )
    assert bombs > -1, ValueError("Bombs must be a positive integer (including zero)")

    # Example can be m=n=8 and bombs = 4
    # Brute force solution would be to set the bombs iteratively,
    # while checking which positions already have a bomb.

    # Otherwise we need to select locations from a set of options.
    # In this case, our number of options would be out of a set of
    # n options.

    # We can select random n locations with choices.
    # e.g. select n choices out of a set. (random.sample)
    # random.sample()

    l = m * n
    if bombs >= l:
        # all are bombs
        return [[bomb_symbol] * m for _ in range(n)]

    # If we wanted to implement sample, its the idea of moving the selected sample to the end of the random
    # list.

    # Select the random range.
    # O(N)
    locs = list(range(l))
    board = [[empty_symbol] * m for _ in range(n)]

    # O(bombs)
    for _ in range(bombs):
        idx = locs[random.randint(0, l - 1)]
        i = locs[idx] // m
        j = locs[idx] % m
        board[i][j] = bomb_symbol

        # append the current location to the end
        if idx != l - 1:
            locs[idx], locs[l - 1] = locs[l - 1], locs[idx]

        # reduce l, to ignore the location selected.
        l -= 1

    return board


# %%
bombs = 5
n = 10
m = 10
board = generate_minesweeper_board(n, m, bombs, empty_symbol=0, bomb_symbol=1)
gen_bombs = sum(1 for r in board for v in r if v == 1)
print(bombs, gen_bombs, gen_bombs == bombs)

from matplotlib import pyplot as plt

plt.imshow(board)
a:str="Asds"
a.lower()