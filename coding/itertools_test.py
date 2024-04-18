import string
from itertools import groupby

to_compress = "ccccsadsadqweasdf fggggg dsdf dsa eee     "
print(
    "".join(
        [
            f"({len(list(grp))}, {letter})"
            for letter, grp in groupby(to_compress, lambda l: l)
        ]
    )
)
