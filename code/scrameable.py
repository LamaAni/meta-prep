# %%
import math
from random import randint, random


class Solution:
    def isScramble(
        self,
        src: str,
        comp: str,
    ) -> bool:
        # depth = math.ceil(math.log(len(src), 2))

        def scramble_perm(src, min_idx: int, max_idx: int):
            if src == comp:
                return True

            if min_idx == max_idx:
                # reached end
                return False

            # Calculates the scramble permutations
            delta = (max_idx - min_idx) // 2
            x = src[min_idx : min_idx + delta]
            y = src[min_idx + delta : max_idx]

            switched = y + x
            # check the opposite
            if switched == comp:
                return True

            for s in [src, switched]:
                # apply on original and on the switched
                # options
                # n(min->delta), n2
                # n1, s2
                # s1, n2
                # s1, s2

                pass

        return scramble_perm(src, 0, len(src))

        pass


expected = True
rslt = Solution().isScramble("abc", "cba")
print()
print(rslt == expected)


# %%

n_nums = 4

# Now that its sorted, we can set the three idxs
i = 0
n_idxs = n_nums - 1
idxs = [-1 for _ in range(n_idxs)]  # The last 3, I will handle i externally


def next_idxs(last=False) -> bool:
    if last:
        # advancing the last index
        idxs[-1] -= 1
        if idxs[-2] + 1 == idxs[-1]:
            # Advance the next one below possible.
            return next_idxs()
        return True
    else:A
        # advances the index by the following rule
        for i in range(n_idxs - 1, -1, -1):  # reverse count
            cur_idx = idxs[i]
            next_idx = idxs[i + 1]
            # Compre i,i+1
            if cur_idx + 1 == next_idx:
                # next and cur are the same.
                if i == 0:
                    return False
                # advancing prev index
                idxs[i - 1] += 1
                idxs[i] = idxs[i - 1] + 2
            else:
                idxs[i] += 1
                return True

    # Cannot advance anymore
    return False


idxs = [0, 5, 6, 7]

for i in range(40):
    print(idxs)
    next_idxs()


# %%
