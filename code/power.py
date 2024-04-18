import math


def do_pow(x: float, n: int):
    if n == 0:
        return 1

    if n < 0:
        x = 1 / x

    n = abs(n)

    def pow(x, n):
        if n == 1:
            return x
        mul = 1
        if n % 2 != 0:
            mul = x
        pn = pow(x, n // 2)
        return pn * pn * mul

    return pow(x, n)


x = 2.0
for n in [6, 3, 5, 10]:
    print(do_pow(x, n), math.pow(x, n))
