# User function Template for python3


class Solution:
    def subArraySum(self, arr, n, s):
        if s == 0:
            # just find the first zero if any
            try:
                idx = arr.index(0)
            except Exception:
                idx = -1

            if idx < 0:
                return [-1]
            return [idx, idx]
        # Sliding window solution
        i = 0
        j = 0
        sub_sum = 0
        while i < n:
            if sub_sum == s:
                return [i + 1, j]

            # advance the minimum
            if sub_sum > s:
                sub_sum -= arr[i]
                i += 1

            # advance the maximum
            if sub_sum < s:
                if j >= n:
                    break

                sub_sum += arr[j]
                j += 1

        return [-1]


arr = [0]
# print(arr)
print(Solution().subArraySum(arr, len(arr), 0))
