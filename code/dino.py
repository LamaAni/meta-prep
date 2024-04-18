# reading the files
from functools import cmp_to_key
from typing import Dict
import json

dino_map: Dict[str, Dict] = {}


# O(fields * rows) per file
def read_file(fn):
    with open(fn, "r", encoding="utf-8") as raw:
        first = True
        cols = []
        # O(rows), should read line by line without loading all to memory. Check read line by line.
        # mmap would also work here to be faster. But thats overkill.
        for ln in raw:
            # not sure needed
            # TODO: Verify needed
            if ln is None:
                break
            # first row is cols
            if first:
                first = False
                # O(fields)
                cols = [c.strip() for c in ln.split(",")]
                continue

            dino_info = {}
            cells = ln.split(",")

            # O (fields)
            for i in range(len(cells)):
                dino_info[cols[i]] = cells[i]

            # Merge by name.
            name = dino_info.get("NAME")

            if name in dino_map:
                # O(Fields)
                dino_map[name].update(dino_info)
            else:
                dino_map[name] = dino_info


read_file("dino1.csv")
read_file("dino2.csv")

# print result
print(json.dumps(dino_map, indent=2))


# # ((STRIDE_LENGTH / LEG_LENGTH) - 1) * SQRT(LEG_LENGTH * g)
# for name in dino_map.keys():
#     if dino_map[name]["STANCE"] == "bipedal":
#         # dino_map[name]["SPEED"] =
