# %%
import math


def calc_theta(a, b):
    sine_t = math.sqrt(1 + math.pow(a / b, 2)) / 2
    return math.asin(sine_t)


print(calc_theta(10, 10))
