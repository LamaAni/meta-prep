# %%
def bins(v, pad_zeros=4):
    s = 2
    if v < 0:
        s = 3
    return (bin(v)[s:]).rjust(pad_zeros, " ")


# ^ xor


def add_with_bits(a, b):
    a = int(a)
    b = int(b)

    # max int value is 32 bit, or 8 bytes
    # the max limits the negative bits.
    # if we overflow
    mask = 0xFFFFFFFF
    while b & mask != 0:
        print("**")
        # if (a & b) << 1 != (a & b):
        #     print("diff", (a & b) << 1, (a & b))
        print(
            "\n".join(
                [
                    f"          a = {bins(a)}",
                    f"          b = {bins(b)}",
                    "--",
                    f"      a ^ b = {bins(a ^ b)}",
                    f"      a & b = {bins(a & b)}",
                    "--",
                    f" (a & b)<<1 = {bins((a & b)<<1)}",
                ]
            )
        )
        a, b = a ^ b, (a & b) << 1

    print("**")
    # the case we a stooped by the mask, we limit it 
    # to return just the mask
    return a if b == 0 else a & mask


print(add_with_bits(5, -2))
