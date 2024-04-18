from typing import List


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left: TreeNode = None
        self.right: TreeNode = None

    def values(self):
        # map to values
        arr = [self.val]
        if self.left:
            arr = self.left.values() + arr
        if self.right:
            arr = arr + self.right.values()
        return arr


class ListNode:
    def __init__(
        self,
        val=None,
        next: "ListNode" = None,
        prev: "ListNode" = None,
    ) -> None:
        self.val = val
        self.next: ListNode = next
        self.prev: ListNode = prev

    def values(self):
        cur = self
        arr = []
        while cur is not None:
            arr.append(cur.val)
            cur = cur.next
            # circular
            if cur == self:
                break
        return arr


class Solution:
    """
    @param root: root of a tree
    @return: head node of a doubly linked list
    """

    def treeValues(self, tn: TreeNode):
        arr = [tn.val]
        if tn.left:
            arr = self.treeValues(tn.left) + arr
        if tn.right:
            arr = arr + self.treeValues(tn.right)
        return arr

    def treeToDoublyListWithArray(self, root: TreeNode):
        # Write your code here.
        values = self.treeValues(root)
        # convert to list
        head: ListNode = None
        cur: ListNode = None
        for v in values:
            if cur is None:
                cur = head = ListNode(v)
            else:
                cur.next = ListNode(v)
                cur = cur.next

        return head

    def treeToDoublyList(self, root: TreeNode):
        if root is None:
            return None

        # convert to list
        head: ListNode = ListNode(root.val)

        def traverse(tn: TreeNode, ln: ListNode):
            nonlocal head
            if ln.val < head.val:
                head = ln

            if tn.left:
                left = ListNode(tn.left.val)
                if ln.prev:
                    ln.prev.next = left
                    left.prev = ln.prev
                ln.prev = left
                left.next = ln

                traverse(tn.left, ln.prev)

            if tn.right:
                right = ListNode(tn.right.val)
                if ln.next:
                    ln.next.prev = right
                    right.next = ln.next
                ln.next = right
                right.prev = ln

                traverse(tn.right, ln.next)

        traverse(root, head)

        # make it circular
        # left.prev = right

        return head


def compose_binary_tree(nums: List[int]):
    root: TreeNode = TreeNode(nums[0])

    def insert_into_tree(val, tn: TreeNode = root):
        if tn.val <= val:
            if not tn.right:
                tn.right = TreeNode(val)
            else:
                insert_into_tree(val, tn.right)
        else:
            if not tn.left:
                tn.left = TreeNode(val)
            else:
                insert_into_tree(val, tn.left)

    for val in nums[1:]:
        insert_into_tree(val)
    return root


tree_root = compose_binary_tree([4, 2, 5, 1, 3])
print(tree_root.values())
print(Solution().treeToDoublyList(compose_binary_tree([4, 2, 5, 1, 3])).values())
