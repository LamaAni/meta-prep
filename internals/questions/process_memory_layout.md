# What is the linux process memory layout

Top (max memory address)

```
Stack
---
expand memory
---
static libs
---
expand memory
---
Heap
---
Uninitialized static variables
---
Initialized static variables
---
read only code
```

bottom (min memory address)

## Stack

1. The stack memory has less space.
1. The stack memory is LIFO (Last in first out), and therefore, better for,
   - function args
   - local vars
   - function pointers
   - anything where we go "in" and "out" of scope.
   - usually faster
1. The stack is used to "run the program"

## Heap

1. The heap is slower then the stack, in most cases.
1. The heap is used for large memory items, that will be used across methods (pointers)
1. Use the heap if the size of the variable is very large.
