class TreeNode:
    def __init__(self, val=None):
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

    def insert(self, val):
        if self.val >= val:
            if self.left:
                self.left.insert(val)
            else:
                self.left = TreeNode(val)
        else:
            if self.right:
                self.right.insert(val)
            else:
                self.right = TreeNode(val)

    @classmethod
    def from_vals(cls, vals: list):
        if vals is None:
            return None

        root = None
        for val in vals:
            if root is None:
                root = TreeNode(val)
            else:
                root.insert(val)

        return root

    def __repr__(self) -> str:
        return str(self.values())


class ListNode:
    def __init__(self, val=None) -> None:
        self.val = val
        self.next: ListNode = None
        self.prev: ListNode = None

    def values(self, visited: set = None):
        visited = visited or set()
        if self in visited:
            return []
        visited.add(self)
        if self.next is None:
            return [self.val]
        return [self.val] + [*self.next.values(visited)]

    def __repr__(self) -> str:
        return str(self.values())


def bst_to_dll(root: TreeNode):
    # scan the tree and add to the root value
    # do it with linear tree scan.
    head: ListNode = None
    tail: ListNode = None

    def insert_to_list(node: TreeNode):
        nonlocal head
        nonlocal tail

        ln = ListNode(node.val)

        if head is None:
            head = ln
            tail = ln
        else:
            tail.next = ln
            ln.prev = tail
            tail = ln

    # scanning in order. so we should not be afraid of duplicates.
    stack = []
    cur: TreeNode = root
    while True:
        if cur:
            stack.append(cur)
            cur = cur.left
        elif len(stack) > 0:
            cur = stack.pop()
            insert_to_list(cur)
            cur = cur.right
        else:
            break

    # circular list
    tail.next = head
    head.prev = tail
    return head


# creating samples
Object = lambda **kwargs: type("Object", (), kwargs)
samples = [
    Object(
        tree=TreeNode.from_vals([4, 2, 5]),
        expected=[2, 4, 5],
    ),
    Object(
        tree=TreeNode.from_vals([4, 2, 5, 3, 1]),
        expected=[1, 2, 3, 4, 5],
    ),
]


for sample in samples:
    print("---")
    print(sample.tree)
    rslt: ListNode = bst_to_dll(sample.tree)
    is_ok = rslt.values() == sample.expected
    print(is_ok, ",", sample.expected, "==", rslt.values())
