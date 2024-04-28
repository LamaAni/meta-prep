"""
Design an in-memory file system to simulate the following functions:

ls: 

Given a path in string format. 
If it is a file path, return a list that only contains this file's name. 
If it is a directory path, return the list of file and directory names in this directory. 
Your output (file and directory names together) should in lexicographic order.

mkdir: 
Given a directory path that does not exist, you should make a new directory according to the path.
If the middle directories in the path don't exist either, you should create them as well.
This function has void return type.

addContentToFile:
Given a file path and file content in string format. 
If the file doesn't exist, you need to create that file containing given content. 
If the file already exists, you need to append given content to original content. 
This function has void return type.

readContentFromFile: Given a file path, return its content in string format.
"""

from typing import Dict, List, Union


class MemoryINode:
    def __init__(
        self,
        path: tuple,
        content: str = None,
        is_dir: bool = False,
    ) -> None:
        assert content is None or isinstance(content, str), ValueError(
            "Invalid content input when appending to file"
        )
        self.path = path
        self.content = content
        self.is_dir = is_dir
        self.child_nodes: List["MemoryINode"] = []
        self.child_nodes_set = set()

    def add_child(self, child: "MemoryINode"):
        assert isinstance(child, MemoryINode), ValueError(
            "Child must be of type MemoryINode"
        )

        if child in self.child_nodes_set:
            return False

        # can be better
        # we can do an insert int the sorted position already.
        # using some binary search. So single value in list -> O(LogN)
        self.child_nodes.append(child)
        self.child_nodes_set.add(child)

        def get_key(n: MemoryINode):
            return "/".join(n.path).lower()

        self.child_nodes.sort(key=get_key)

        return True

    def __str__(self) -> str:
        return f"{'/'.join(self.path)}:{'dir' if self.is_dir else 'file'}"

    def __repr__(self) -> str:
        return str(self)


class MemoryFS:
    def __init__(self, sep: str = "/") -> None:
        self.sep: str = sep
        self.root = MemoryINode((), is_dir=True)
        self.inodes: Dict[tuple, MemoryINode] = {}
        self.inodes[self.root.path] = self.root

    def parse(self, path: Union[str, List[str]]) -> List[str]:
        if path is None:
            return tuple()
        if isinstance(path, tuple):
            return path
        if isinstance(path, str):
            path = path.strip()
            path = path.strip("/")

            if not path:
                return tuple()
            return tuple(path.split(self.sep))
        elif isinstance(path, list):
            path = tuple(path)
            return path
        else:
            raise ValueError("Path must either be a string or list of strings")

    def get_inode(
        self,
        path: Union[str, List[str]],
        create: bool = True,
        crete_as_dir: bool = False,
    ):
        path = self.parse(path)

        if path not in self.inodes:
            # need to check the path in the inodes
            # assert parents exists.
            if create:
                # looking for and creating parents.
                # We assume that its most likely that some first parent was created.
                # therefore add in reverse.
                cur_path = path[:-1]
                child = None
                while len(cur_path) > 0:
                    node = self.inodes.get(cur_path, None)
                    has_node = node is not None
                    if node is None:
                        node = MemoryINode(cur_path, is_dir=True)
                        self.inodes[cur_path] = node

                    if len(cur_path) == 1 and not has_node:
                        self.root.add_child(node)

                    if child:
                        node.add_child(child)

                    if has_node:
                        break

                    child = node
                    cur_path = cur_path[:-1]

                inode = MemoryINode(path, is_dir=crete_as_dir)
                self.inodes[path[:-1]].add_child(inode)

                # Add child to inode map.
                self.inodes[path] = inode

            else:
                return None

        return self.inodes[path]

    def mkdir(self, path: Union[str, List[str]]):
        # make dirs and sub directories
        node: MemoryINode = self.get_inode(path, create=True, crete_as_dir=True)

        if not node.is_dir:
            raise Exception("Invalid directory, file already exists")

    def ls(
        self,
        path: Union[str, List[str]] = None,
        recursive: bool = True,
    ) -> list[str]:
        node = self.get_inode(path, create=False)
        if node is None:
            return []

        lst = []
        if node.is_dir:
            # get the paths inside the directory
            if recursive:
                stack = [node]
                while stack:
                    cur = stack.pop()
                    lst.append(self.sep.join(cur.path))
                    for i in range(len(cur.child_nodes) - 1, -1, -1):
                        stack.append(cur.child_nodes[i])
            else:
                lst = [self.sep.join(c.path) for c in node.child_nodes]
        else:
            lst = [self.sep.join(node.path)]

        return lst

    def append(self, path: Union[str, List[str]], content: str):
        path = self.parse(path)
        node = self.get_inode(path, create=False)
        if node is None:
            # Check if there is a parent.
            parent = self.get_inode(path[:-1], create=False)
            if parent is None:
                raise Exception("Parent path dose not exist")
            if not parent.is_dir:
                raise Exception(
                    f"Invalid path, one of the directories in the path is actually a file: {parent.path}",
                )

            # we can just create the inode
            node = MemoryINode(path)
            self.inodes[path] = node
            parent.add_child(node)

        node.content = content if not node.content else node.content + content

    def read(self, path: Union[str, List[str]]):
        node = self.get_inode(path, create=False)
        return None if node is None else node.content


# The way to do this is to keep two a contents map
# and to handle all the data changes on add, mkdir.

if __name__ == "__main__":
    import os
    from utils.logs import REPO_PATH
    from datetime import datetime

    fs = MemoryFS()
    global tictoc_cur
    tictoc_cur = datetime.now()

    def tic():
        global tictoc_cur
        tictoc_cur = datetime.now()

    def toc():
        global tictoc_cur
        return datetime.now() - tictoc_cur

    print()
    print("Insert")
    tic()

    for root, dirs, files in os.walk(os.path.join(REPO_PATH, "internals")):
        fs.mkdir(root)
        for f in files:
            fpath = os.path.join(root, f)
            with open(fpath, "r") as raw:
                fs.append(fpath, raw.read())

    # auto build p
    # cur_path = ""

    # for i in range(5000):
    #     # cur_path_parts.append(str(i))
    #     cur_path = os.path.join(cur_path, str(i))

    #     fs.mkdir(cur_path)
    #     file_path = os.path.join(cur_path, "txt.txt")
    #     # str(i)
    #     fs.append(file_path, str(i))

    print("print")
    chars = 100
    print(
        "\n".join([("..." + v[-chars:]) if len(v) > chars else v for v in fs.ls("/")])
    )

    print("Insert time")
    print(toc().total_seconds())

    cur_path = ["0"] * 1000

    tic()
    for i in range(20000):
        fs.parse(cur_path)
    print("Prase time")
    print(toc().total_seconds())

    tic()
    for i in range(20000):
        fs.get_inode(cur_path)
    print("Get inode time")
    print(toc().total_seconds())
