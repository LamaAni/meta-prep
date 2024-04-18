from typing import List
from check_idxs_samples import samples

class Solution:
    def next_idxs(
        self,
        max_idx,
        idxs: List[int],
        start_at: int = 1,
        l_idxs=-1,
    ):
        if l_idxs < 0:
            l_idxs = len(idxs)

        adv_from = -1
        for i in range(l_idxs - 1, start_at - 1, -1):
            cur_idx = idxs[i]
            next_idx = idxs[i + 1] if i < l_idxs - 1 else max_idx + 1
            if cur_idx + 1 < next_idx:
                adv_from = i
                break
            i -= 1

        # cannot advance
        if adv_from < 0:
            return False

        idxs[adv_from] += 1

        for i in range(adv_from + 1, l_idxs):
            # all but last
            idxs[i] = idxs[adv_from] + i - adv_from

        # Cannot advance anymore
        return True

    def fourSum(self, nums: List[int], target: int, n_sum: int = 4) -> List[List[int]]:
        l_n = len(nums)
        if l_n < n_sum:
            # To sum at least n items you need a list of that size.
            return []

        # We first sort. On a sorted list we can scan left
        # to right and know that our sum can determine the motion.
        rslt = set()
        nums.sort()

        print(nums, "sums of", n_sum, "==", target, "\n----")

        # Now that its sorted, we can set the three idxs
        idxs = [-1 for _ in range(n_sum)]  # The last 3, I will handle i externally

        def next_idxs(start_at: int = 1) -> bool:
            return self.next_idxs(l_n - 1, idxs, start_at=start_at, l_idxs=n_sum)

        # I maps the main loop
        idxs[0] = 0
        while idxs[0] < l_n - n_sum + 1:
            # we need to search for internal values by moving
            # j,k, we should expect j<k, so we have i<j<k?

            # reset our position
            for j in range(1, n_sum):
                # For i=2 => idxs = [2,3,4,5,6...n_sum-1,l_n-1]
                idxs[j] = idxs[0] + j

            while True:
                sel_nums = [nums[j] for j in idxs]
                diff = sum(sel_nums) - target
                print(idxs, sel_nums, diff)
                if diff == 0:
                    # found a match
                    rslt.add(tuple(sel_nums))

                # Moving to next
                if not next_idxs():
                    # nothing to advance to.
                    break
            idxs[0] += 1

        return rslt




def run_problem(idx=0):
    y_pred: set = Solution().fourSum(samples[idx][0], samples[idx][1], samples[idx][2])
    y_true = set(tuple(v) for v in samples[idx][3])
    y_missing = y_true.difference(y_pred)
    y_extra = y_pred.difference(y_true)

    print("----")
    print("pred:", y_pred)
    print("true", y_true)
    print("----")
    print("missing:", y_true.difference(y_pred))
    print("extra:", y_pred.difference(y_true))
    print("----")
    print("Failed" if len(y_missing) + len(y_extra) > 0 else "Success")


def run_idxs():
    idxs = [0, 1, 2, 3]
    max_idx = 7
    for i in range(40):
        print(idxs)
        if not Solution().next_idxs(max_idx, idxs):
            break


run_problem(2)
