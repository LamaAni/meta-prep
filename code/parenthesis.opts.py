from typing import List


def diffWaysToCompute(expression: str) -> List[int]:
    # recursive?
    # tokenize
    exp = []
    num = ""
    for c in expression:
        if c in ["+", "-", "*"]:
            if len(num) == 0:
                raise Exception("Bad expression")
            exp.append(tuple([int(num), c]))
            num = ""
        else:
            num += c

    if len(num) > 0:
        exp.append(tuple([int(num), None]))

    def opt_to_str(opt):
        if not isinstance(opt, list):
            return str(opt[0]), opt[1]
        o = None
        as_str = []
        for o in opt:
            o_str, operator = opt_to_str(o)
            as_str.append(o_str)
            as_str.append(operator)
        return "(" + " ".join(as_str[:-1]) + ")", as_str[-1]

    # just the number of the exp
    def get_opts(exp):
        if len(exp) == 1:
            return [[exp[0]]]
        if len(exp) == 2:
            return [[exp[0], exp[1]]]
        rslt = []
        # split for each element is possible
        for j in range(1, len(exp)):
            left = get_opts(exp[:j])
            right = get_opts(exp[j:])
            for opl in left:
                for opr in right:
                    rslt.append([opl, opr])

        return rslt

    def calc_opt(opt):
        if not isinstance(opt, list):
            return opt[0], opt[1]
        elif len(opt) == 1:
            return opt[0][0], opt[0][1]

        a, operator = calc_opt(opt[0])
        b, next_operator = calc_opt(opt[1])

        if operator == "-":
            return a - b, next_operator
        elif operator == "+":
            return a + b, next_operator
        elif operator == "*":
            return a * b, next_operator

    opts = get_opts(exp)
    return [calc_opt(opt)[0] for opt in opts]


print(diffWaysToCompute("2-1-1"))
print()
print(diffWaysToCompute("2*3-4*5"))
