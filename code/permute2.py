# no repetitions
#
def next_permutation(nums):
    # based on binary search.
    # assuming reverse order is the last value, we can see what permutations
    # of arrangement we have on the way there.
    # e.g.
    # [1,2,3,4,5] -> [1,2,4,3,5] ... -> [1,2,5,4,3]  ... -> [5,4,3,2,1]
    # to get all permutations while we sort the array by shifting the smallest value
    # at the end of the largest ascending sequence to the end of the descending sequence.
    # since we are sorting in a "binary" fashion, we should not repeat

    # steps: [1,2,5,4,3]
    # 1. find the largest location of binary split, e.g. last permute: k where n[k]<n[k+1] -> k=2, k==-1 no more permutations.
    # 2. find the location where the upwards series last end (even if it has dips in it): m where n[k]<n[m] -> m=4
    # 3. swap k,m
    # 4. reverse n[k+1:] (we are not at end, and if we have ordered everything, we will not find or find a duplicate, so we reverse to make sure we have such an element)
    n = len(nums)

    if n < 2:
        # no sort. Single or no items
        return -1

    k = n - 2
    # look until we can find, if we cant its sorted.
    while k > -1:
        # find the last increasing sequence item.
        if nums[k] < nums[k + 1]:
            break
        k -= 1

    # if we havent found, nothing to sort.
    if k < 0:
        return k

    # find the upwards
    m = n - 1
    while m > -1:
        if nums[k] < nums[m]:
            break
        m -= 1

    # swap
    nums[k], nums[m] = nums[m], nums[k]
    # reverse
    nums[k + 1 :] = nums[n - 1 : k : -1]

    return k


arr = [1, 2, 3, 4]
arr.sort()
perturbs = set()

while True:
    if tuple(arr) in perturbs:
        raise Exception("Repetition")
    last = tuple(arr)
    perturbs.add(last)
    p_k = next_permutation(arr)
    print(last, ",", p_k, "->", arr)
    if p_k < 0:
        break

print(len(perturbs))
