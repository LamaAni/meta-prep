# What is swap

Swap memory is a way to extend the computers physical memory to disk (RAM->disk). When the application runs, the kernel needs to load the memory from disk to RAM in order to execute. The latter process is called paging.

page - a block to be loaded into/or downloaded from memory.

In linux (and other OS's) we use a virtual memory address, which then can be mapped to a location in the RAM, on disk (swap), or not at all.

When the kernel sees that memory is low will download in pages some of the memory to disk and store it in the swap (Selection algorithm called least recently used (LRU)). This will make this memory not available for the program when it tries to rum.

When a program who's memory was downloaded tries to execute, the MMU will throw a page fault - telling the kernel it needs this block of memory, in which case,

1. The memory is on disk - load the page from disk into memory and continue execution.
1. In case this memory range was not assign, assign it to RAM. (In the case where it was not downloaded - but never initialized)

In some cases, when we try to allocate more memory in the RAM, and were out, we will move memory, the least recently used, to disk. (This takes time). Once swapped. Memory can then be loaded back from disk.

## Advantages

1. Allows us to extend the memory and run more programs.
1. Allows programs, that are waiting to be off loaded - better multitasking.
1. Prevents run out of ram.

## Disadvantages

1. Slow - very. If a program writes a lot of swap it will slow the computer.
1. Takes disk IO - Which can result in locks or breaks or slowdown. Even in unrelated services.
1. Slows down execution since it stops (traps) the cpu while memory is loading for a page.
