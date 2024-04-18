def minDistance(word1: str, word2: str) -> int:
    # try recursive first
    # naive solution?
    def calc_ops(word1, word2):
        # partial words 1,2.
        if len(word1) == 0:
            return len(word2)
        elif len(word2) == 0:
            return len(word1)

        if word1[0] == word2[0]:
            return calc_ops(word1[1:], word2[1:])

        # each op is itself plus internal
        add = 1 + calc_ops(word2[0] + word1, word2)
        replace = 1 + calc_ops(word2[0] + word1[1:], word2)
        delete = 1 + calc_ops(word1[1:], word2)

        return min(add, replace, delete)

    return calc_ops(word1, word2)


print(minDistance("horse", "ros"))
