def mySqrt(x: int) -> int:
    if x == 0:
        return 0

    if x == 1:
        return 1

    # sqrt x lies between 1 and x
    # approach
    # 1. define r_mid=(rmax-rmin)/2+rmin -> give a number
    # 2. if r_mid*r_mid<x then this is smaller than sroot(x)
    # 3. if r_mid*r_mid>x then this number is larger than sroot(x)
    # 4. change r_min and r_max appropriately.
    # 5. loop back. Stop when r_min == r_max or r_min-r_max<1?

    r_min = 1  # result min number
    r_max = x  # result max number
    while r_max - r_min > 1:
        mid = r_min + (r_max - r_min) // 2
        smid = mid * mid
        if smid == x:
            # the number
            return int(mid)
        elif smid > x:
            r_max = mid
        else:
            r_min = mid

    return int(r_min)


print(mySqrt(9))
