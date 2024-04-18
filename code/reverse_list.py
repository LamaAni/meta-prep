from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next: ListNode = next

    def to_list(self, lst: list = None, visited: set = None) -> list:
        lst = lst or []
        visited = visited or set()
        if self in visited:
            return lst
        visited.add(self)

        lst.append(self.val)
        if self.next:
            self.next.to_list(lst, visited)
        return lst

    def walk(self, count: int):
        if count <= 0:
            return self
        if self.next:
            return self.next.walk(count - 1)
        return None

    def __repr__(self) -> str:
        return f"{self.val}"


def build_linked_list(vals: list) -> ListNode:
    head = None
    cur = head
    for v in vals:
        if cur:
            cur.next = ListNode(v)
            cur = cur.next
        else:
            cur = ListNode(v)
            head = cur

    return head


def reverse_list(head: ListNode, stop_at: ListNode = None):
    if head is None:
        return head
    cur = head.next
    prev = head
    while cur is not None and prev != stop_at:
        # a -> b -> c
        # a <- b -> c
        next_i = cur.next
        cur.next = prev
        prev = cur
        cur = next_i

    if stop_at is not None:
        head.next = cur

    return prev


def reverseBetween(
    head: Optional[ListNode],
    left: int,
    right: int,
) -> Optional[ListNode]:
    # try do in 2 parts. Get to the point and then start the reverse.
    cur = head

    left_anchor = None
    left_node = None
    right_node = None

    # load params
    i = 0
    while cur:
        if left == i + 1:
            left_node = cur
        if left_node is None:
            left_anchor = cur
        if right == i + 1:
            right_node = cur
            break
        cur = cur.next
        i += 1

    if left_node is None:
        return head

    # found the left anchor and left node.
    # reverse until reached right
    prev = left_node
    cur = left_node.next
    while cur is not None and prev != right_node:
        next_node = cur.next
        cur.next = prev
        prev = cur
        cur = next_node

    # attach back if any cur = 5 , prev == 4, left_anchor = 1, left_node=2
    # 1 -> 2 <- 3 <- 4 -> (5)
    # 1 -> 4 -> 3 -> 2 -> 5
    # reattach the end
    left_node.next = cur

    # reattach the start.
    if left_anchor:
        left_anchor.next = right_node
    else:
        head = right_node

    return head


head = build_linked_list([1, 2, 3, 4, 5])
print(head.to_list())
print(reverseBetween(head, 2, 4).to_list())
# print(reverse_list(head, head.walk(3)).to_list())
