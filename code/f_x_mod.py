# %%
# Enter your code here. Read input from STDIN. Print output to STDOUT
import string
import math

# F(x)=x^2, power(x,2)
# K=3
# S=(Sum(F(Xi)%M))


def is_digits(val):
    return [let in string.digits for let in val]


examples = []


def add_answer(inputs: str, rslt: int):
    examples.append((inputs.strip(), rslt))


add_answer(
    """
3 1000
2 5 4
3 7 8 9 
5 5 7 8 9 10 
""",
    206,
)
add_answer(
    """
3 10
2 1 10
3 1 5 10
5 1 5 10 20 30
""",
    7,
)
add_answer(
    """
3 10
2 1 10
3 10 5 1
5 1 7 10 20 30
""",
    9,
)
add_answer(
    """
1 384
5 899954391 390010037 470009874 789620942 589990574
""",
    324,
)
add_answer(
    """
7 952
6 386364143 56297585 479292050 782778989 177771725 945191156
7 458982242 957774948 25202756 357554307 248513713 506622954 769577156
3 109432676 494972174 914814315
1 49979276
2 491584479 103564062
1 25883738
1 460971693
""",
    943,
)
add_answer(
    """
3 10
5 1 7 10 20 30
3 10 5 1
2 1 10
""",
    9,
)
add_answer(
    """
7 867
7 6429964 4173738 9941618 2744666 5392018 5813128 9452095
7 6517823 4135421 6418713 9924958 9370532 7940650 2027017
7 1506500 3460933 1550284 3679489 4538773 5216621 5645660
7 7443563 5181142 8804416 8726696 5358847 7155276 4433125
7 2230555 3920370 7851992 1176871 610460 309961 3921536
7 8518829 8639441 3373630 5036651 5291213 2308694 7477960
7 7178097 249343 9504976 8684596 6226627 1055259 4880436
""",
    866,
)

# %%
example_idx = 3
args_input_lines = examples[example_idx][0].strip().split("\n")
expected_output = examples[example_idx][1]


def input():
    return args_input_lines.pop(0).strip()


args_input = input()

assert is_digits(args_input), ValueError(
    "The first line must be composed of digits only"
)
args_input = [v.strip() for v in args_input.split(" ")]
assert len(args_input) == 2, ValueError("The first row must be of the form 'K M'")

K = int(args_input[0])
M = int(args_input[1])

# reading lists
k_lists = [input() for _ in range(K)]
assert all(is_digits(ln) for ln in k_lists), ValueError(
    "Invalid input, all rows must be composed of a list of numbers, in the form Ni, X0, X1 .. X_Ni"
)
# Split to cells.
k_lists = [[int(v.strip()) for v in ln.split(" ")] for ln in k_lists]

for i in range(K):
    lst = k_lists[0]
    assert len(lst) - 1 == lst[0], ValueError(
        "Invalid input, for each list row, the first element should be the number of elements in the list"
    )


def f_x(val):
    return math.pow(val, 2)

import re



repeating_pattern=re.compile("|".join(["[{0}]{{3}}[{0}]+".format(i) for i in range(10)])fl)
                             
# First calculate the fx? Is it worth it?
# Since were dealing with modulo we first can reduce the functions by the modulo
# to find only numbers that contribute to the sum. since (1100 + 2600)%1000 = (1000+100+2000+600)%M = (100+600)%M

# (a + b) mod n = [(a mod n) + (b mod n)] mod n. This is correct!

# O(N)*O(K)*O(7)
k_list_vals = [[f_x(v) % M for v in arr[1:]] for arr in k_lists]
print(k_list_vals)

# We can now try to specify the load indexes, and add one to the index of the list,
# To get closest to M.
idxs = [0 for _ in range(K)]


def calc_sum():
    rslt = 0
    for i in range(K):
        rslt += k_list_vals[i][idxs[i]]
    return rslt % M


attempts = []


# Since its in 1, 7
def get_max_sum_in_list(k_i=0):
    lst = k_list_vals[k_i]
    max_sum = calc_sum()
    for i in range(len(lst)):
        idxs[k_i] = i
        if k_i < K - 1:
            cur_sum = get_max_sum_in_list(k_i + 1)
        else:
            cur_sum = calc_sum()
            attempts.append(f"{idxs}: {cur_sum}")

        if cur_sum > max_sum:
            max_sum = cur_sum
    return max_sum


try:
    max_sum = get_max_sum_in_list()
except Exception as ex:
    print(idxs)
    raise ex

max_sum = int(max_sum) % M
print()
# print(max_sum)
print(f"{max_sum} ?= {expected_output} ({max_sum==expected_output})")
