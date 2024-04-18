from typing import List


class Solution:
    def jump(self, nums: List[int]) -> int:
        # i=0
        # Length of nums is large.
        # So cant do recursive
        n = len(nums)

        # The second I'm over the end, it is the end.
        # question is is there any locations along the way that have a larger number.
        # so my best jump is to the position which is farthest?

        # best to find the farthest jump
        def find_best_jump(idx):
            max_idx = nums[idx]
            # where j is the jump
            max_j = 0
            max_jump = 0
            # the jump that will be the farthest is best, and wil give max options
            for j in range(max_idx, 0, -1):
                if idx + j >= n - 1:  # reached last item
                    return j
                jump = nums[idx + j] + j
                if jump > max_jump:
                    max_jump = jump
                    max_j = j
            return max_j

        idx = 0
        jumps = 0
        while idx < n - 1:
            jump = find_best_jump(idx)
            idx += jump
            jumps += 1

        return jumps


samples = [
    [2, 3, 1],
    [2, 3, 0, 1, 4],
    [4, 5, 1, 1, 4, 1, 6, 1, 1, 1],
    [1] * 1000,
]
for s in samples:
    print(Solution().jump(s))
