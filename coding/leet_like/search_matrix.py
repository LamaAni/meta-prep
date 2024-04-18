from typing import List


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    # binary 2d search.

    def find_closest_index(nums: List[int], target: int):
        # O(NlogN)
        # assume nums is sorted.

        left = 0
        right = len(nums) - 1
        # print(nums,"?", target)

        # When they are equal, either
        # this index or the next...
        while left <= right:
            # 1 10 10 30, t=11
            # (0,3) -> m = 1 -> 10<11
            # (2,3) -> m = 2 -> 10<11
            # (3,3)
            mid = (right + left) // 2

            if nums[mid] == target:
                # in case equal.
                return mid

            # check others
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        # since right is either left, or one less.
        return right

    # find row index
    ridx = find_closest_index([r[0] for r in matrix], target)
    print(ridx)
    row = matrix[ridx]
    row.sort()
    cidx = find_closest_index(row, target)
    print(cidx)

    return row[cidx] == target


print(searchMatrix([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 50]], 11))
