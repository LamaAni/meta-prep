from typing import List


def split_equal_sums(nums: List[int]):
    right_sum = sum(nums)
    left_sum = 0
    split_at = -1
    for i in range(len(nums) - 1):
        right_sum -= nums[i]
        left_sum += nums[i]
        if right_sum == left_sum:
            split_at = i + 1
            break
    arrs = [nums[:split_at], nums[split_at:]]
    return arrs, ([sum(a) for a in arrs])


print(split_equal_sums([1, 2, 3, 4, 5, 5]))
