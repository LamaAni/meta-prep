from typing import List


class Solution:
    def binarySearch(self, nums, x, sidx=0, eidx=-1, l_nums: int = -1):
        if l_nums < 0:
            l_nums = len(nums)
        if eidx < 0:
            # the last index
            eidx = l_nums + eidx + 1

        # binary search
        end_at = eidx  # keep for later
        while sidx < eidx:
            mid = (sidx + eidx) // 2
            if nums[mid] < x:
                sidx = mid + 1
            else:
                eidx = mid

        if sidx >= end_at:
            return -1
        if nums[sidx] == x:
            return sidx
        return -1

    def search(self, nums: List[int], target: int) -> int:
        pass


arr = [1, 2, 5, 6, 7, 8, 12, 18, 22]
print(Solution().binarySearch(arr, 3))
