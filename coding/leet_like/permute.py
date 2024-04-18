# we can do all combinations
def next_lexical_perturb(nums) -> int:
    # steps:
    # 1. find largest where nums[k]<nums[k+1], or -1
    # 2. find largest where nums[k]<nums[m]
    # 3. swap nums[i] and nums[j]
    # 4. reverse nums[i+1:] - rest of it

    n = len(nums)
    if n < 2:
        return -1

    k = n - 2
    while k > -1:
        if nums[k] < nums[k + 1]:
            break
        k -= 1

    if k < 0:
        return k

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


arr = list(range(20))
arr.sort()
# perturbs = set()

while True:
    # if tuple(arr) in perturbs:
    #     raise Exception("Repetition")
    # last = tuple(arr)
    # perturbs.add(last)
    p_k = next_lexical_perturb(arr)
    # print(last, ",", p_k, "->", arr)
    if p_k < 0:
        break

print(len(perturbs))
