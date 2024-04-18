def numDecodings(s: str) -> int:
    # if not s or s[0] == "0":
    #     return 0

    n = len(s)
    prev = 0
    score = 1

    for i in range(1, n):
        one_digit = int(s[i])
        two_digits = int(s[i - 1 : i + 1])

        if one_digit == 0 and two_digits < 10:
            return 0
        elif 10 <= two_digits <= 26 and one_digit != 0:  # otherwise its just one
            score, prev = score + prev, score
        else:
            # advance
            score, prev = score, score

    return score


for case in [
    "2101",
    "10",
    "123123",
    "06",
    "666666",
]:
    print(numDecodings(case))
