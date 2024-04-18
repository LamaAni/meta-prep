import math
from typing import List


def maxProductNaive(nums: List[int]) -> int:
    n = len(nums)
    max_prod_set = [nums[0]]
    max_prod = nums[0]
    for i in range(n):
        for j in range(i, n):
            p = math.prod(nums[i : j + 1])
            if max_prod < p:
                max_prod = p
                max_prod_set = nums[i : j + 1]
    return max_prod, max_prod_set


def maxProductOther(nums: List[int]) -> int:
    curMax, curMin = 1, 1
    res = nums[0]

    for n in nums:
        vals = (n, n * curMax, n * curMin)
        curMax, curMin = max(vals), min(vals)

        res = max(res, curMax)

    return res


def maxProduct(nums: List[int]) -> int:
    # try again
    n = len(nums)

    # scan the positives/negatives in the next values
    # e.g.
    # 1,-1,1,1,1,-1 -> max 1
    # question is can you continue multiplying.
    # if sign is zero, then we zero out.

    # we are keeping track of min, and max,
    # since they can flip. When we hit zero
    # it dosen't matter since it zeros out.

    cmax = cmin = 1
    max_prod = nums[0]

    for n in nums:
        # see what happens
        compare_to = [n, cmax * n, cmin * n]

        # if negative cmax and cmin flip
        cmax = max(compare_to)
        cmin = min(compare_to)

        max_prod = max(cmax, max_prod)

    return max_prod


nums = [1, 2, -2, -5, -3, -2, -10]
print(maxProductNaive(nums))
print(maxProductOther(nums))
print(maxProduct(nums))
