def merge_sort(nums: list):

    # doing half sort
    def merge_iter(low, high):

        if low == high:
            return

        # left
        mid = (low + high) // 2
        if mid - low > 1:
            merge_iter(low, mid)
        if high - mid > 1:
            merge_iter(mid, high)

        if nums[mid] < nums[mid + 1]:
            # reverse section order
            is_even = (high - low) % 2 == 0

            if is_even:
                # Swap
                nums[low : mid + 1], nums[mid + 1 : high] = (
                    nums[mid + 1 : high],
                    nums[low : mid + 1],
                )

    merge_iter(len(nums))


# sorting with class
