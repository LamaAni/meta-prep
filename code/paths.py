from typing import List


def uniquePaths(m: int, n: int) -> int:
    # naive solution will be recursion.
    # igore.
    #

    # I can take steps forward and then reverse it?
    # like a fro and back.
    # but then I'd have to travel all these paths.
    # use a stack?
    class Step:
        def __init__(
            self,
            x,
            y,
            went_right=False,
            went_down=False,
        ) -> None:
            self.x = x
            self.y = y
            self.went_down = went_down
            self.went_right = went_right

        @property
        def can_go_right(self) -> bool:
            return self.x + 1 < n

        @property
        def can_go_down(self) -> bool:
            return self.y + 1 < m

        def __repr__(self) -> str:
            return f"({self.x},{self.y}) ({self.went_right},{self.went_down})"

    stack: List[Step] = [Step(0, 0)]  # n, m, went right?, went down?
    paths = 0
    first = False

    while True:
        # until reached target
        step = stack[-1]

        # end condition
        if (
            not first
            and step.x == 0
            and step.y == 0
            and step.went_down
            and step.went_right
        ):
            break

        first = False

        if not step.can_go_right and not step.can_go_down:
            # reached target.
            # which means I can pop the stack once.
            stack.pop(-1)
            paths += 1
        else:
            # determine where to go
            if not step.went_right and step.can_go_right:
                step.went_right = True
                stack.append(Step(step.x + 1, step.y))
            elif not step.went_down and step.can_go_down:
                step.went_down = True
                stack.append(Step(step.x, step.y + 1))
            else:
                # cant go anywhere.
                # prev
                stack.pop(-1)

    return paths


print(uniquePaths(100, 7))
