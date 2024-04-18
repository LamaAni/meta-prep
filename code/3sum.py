from typing import List


def threeSumBest(nums: List[int]) -> List[List[int]]:
    l_n = len(nums)
    if l_n < 3:
        # Or assert?
        return []

    # Can use set operations on a tuple
    # which is nice. No need for map.
    rslt = set()

    # If we sort this, we would know where to look for
    # depending on the values of the current indexis
    nums.sort()

    # Now that its sorted, we can set the three idxs
    i = 0

    # window search with 3 numbers.
    # on a sorted array. With the pinning number at i.
    # scan over all i's

    # this would go through all combinations
    # of unique ijk? No since we are increasing
    # or decreasing the window.

    # but permutations without repetitions are a
    # good solution. Since we can test it, and it would fit any number
    # of ijklm.. so 5 indexes would also work. Etc.

    actions = 0

    # I maps the main loop
    while i < l_n - 2:
        # we need to search for internal values by moving
        # j,k, we should expect j<k, so we have i<j<k?
        j = i + 1  # From this index on. Otherwise the prev number would have cought it.
        k = l_n - 1  # The last index
        while j < k:
            actions += 1

            nsum = nums[i] + nums[j] + nums[k]
            # if nsum == 0:
            #     rslt.add((nums[i], nums[j], nums[k]))

            # Moving to next
            if nsum <= 0:
                # If the sum is maller than zero. That means
                # the first number is too small. Need a bigger one.
                # If they match, then we need to just advance to the next one.
                j += 1
            else:
                # If the sum is larger than zero, then need num[k] to be smaller
                # to match num[j]+num[i].
                k -= 1
        i += 1

    return rslt, actions


nums = [i - 1500 for i in range(3000)]
print(threeSumBest(nums)[1])
