def get_bits(n):
    bits = []
    while n > 0:
        if n % 2 == 0:
            bits.insert(0, 0)
        else:
            bits.insert(0, 1)
        n = n // 2

    return bits


print(get_bits(8))
