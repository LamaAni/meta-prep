from typing import List
from datetime import datetime


class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        valid = set()
        l_can = len(candidates)
        candidates.sort()

        # tree search is too slow
        # recursive, no self.

        def tsearch(idx, cur_set: List[int], cur_sum=0):
            if cur_sum > target:
                # Over.
                return

            if cur_sum == target:
                valid.add(tuple(cur_set))
                return

            if idx >= l_can:
                # end
                return

            def ts_next(i):
                val = candidates[i]
                cur_set.append(val)
                tsearch(i + 1, cur_set, cur_sum + val)
                cur_set.pop(-1)

            for i in range(idx, l_can):
                # If its not the base index (0)
                # and its the same candidate, this was already handled in the previous call to ts_next.
                if i > idx and candidates[i] == candidates[i - 1]:
                    continue
                ts_next(i)

        tsearch(0, [])
        return valid


pre = datetime.now()
print(
    Solution().combinationSum2(
        # [2, 3, 5],
        # 5,
        # [10, 1, 2, 7, 6, 1, 5],
        # 8,
        [1] * 25,
        25,
    )
)
print(datetime.now() - pre)
