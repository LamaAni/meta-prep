# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def kthLargestLevelSum(self, root: Optional[TreeNode], k: int) -> int:
        sum_map = {}

        def traverse(tn, depth=1):
            if depth not in sum_map:
                sum_map[depth] = tn.val
            else:
                sum_map[depth] += tn.val

            if tn.left:
                traverse(tn.left, depth + 1)
            if tn.right:
                traverse(tn.right, depth + 1)

        traverse(root)

        sum_vals = list(sum_map.items())
        if len(sum_vals) < k:
            return -1

        sum_vals.sort(key=lambda i: i[1])
        return sum_vals[k]

a=[]
a.reverse()
