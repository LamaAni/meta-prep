# For and execute?

Both the fork and execute methods are used to create a new process in linux. When a new process is created it is assigned memory and a pid. One pid can be the child of another.

The main difference between fork and execute is that fork creates a process that has read access to its parent process memory. Though once changed (becomes dirty - copy-on-write) a copy of the parents memory is made for both fork and original process.

Its important to note that the fork and the parent run in different memory spaces, which means the child addresses are "mapped" to the parent ones.

## Execute

Create a new process and replaces the current. This process will not have any access to the memory of its parent process. This would mean that this process is "brand new" and would be allocated memory for all its parameters.

In general the "exec" should replace the current process. But there are ways to call exec without that. e.g. fork -> exec.

## Fork

The fork creates a copy of the running application (without actually copying the memory). i.e. creates a clone of the current running application with a new id.

Note that the code pages (the ones with instructions) are read-only and therefore will be shared across forks.
