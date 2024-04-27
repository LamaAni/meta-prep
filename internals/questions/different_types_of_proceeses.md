# What are the different types of processes in linux?

Go over,

1. kernel space
1. user space

Process types

1. Kernel process
1. User process (interactive)
1. Background processes (Daemons, backup scripts)
1. zombie processes
1. Orphan process

## Kernel space

A memory address list and permission set where the kernel runs. The kernel is allowed to execute CPU instructions that the child cannot. (ring0 - kernel mode, ring1 - device driver ...)

Applications that fail in the kernel space may affect the whole system.

## User space

Where the applications outside the kernel run. There may be many applications here. CPU instructions are limited to non privileged instructions (ring3- user mode)

Applications that fail in the user space will not affect the whole system

## Kernel processes

Examples

1. Memory management
1. Device drivers
1. Networking
1. Task Scheduling
   ...

These processes run in the kernel space (kernel memory address list), and are part of the kernel execution. They handle low-level system operations like memory allocation and network binding. (lsmod).

## USer processes

Interactive processes that have started from the command line (or GUI). These processes belong to the user.

## Background processes

In systemd, the background processes are mainly daemons, which have ben started by systemctl. These services run in the background and provide functionality like cron, web service, sshd, etc.

## Zombie processes

A process that has stopped, but has not been removed from the process tree. It dose not hold any memory, but may keep buffers open which consume memory.

## Orphan process

A child process who's parent have died. This process may never exit and will consume memory, though its functionality is questionable. This may happen if the process captures the SIGPIPE. If the parent has died though, the process will be re-parented to the init process. In general in linux, an exiting parent dose not send a signal to child??
