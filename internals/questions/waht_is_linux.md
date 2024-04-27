# What is linux?

Linux is an open source operating system (writtent by Linus), based on the then popular unix. The linux system has,

1. Kernel
   1. The kernel application is separated in memory from user applications.
   1. Manages CPU (What program is running on which cpu now, context switch)
   1. Manages Memory (MMU, Virtual Memory)
   1. Manages IO devices (hardware, Disks/Sockets/Inputs/Network)
   1. Manages resources (hardware -> processes)
   1. Runs software, and manages applications
   1. Supports application via system calls,
      - process control (exec, fork, exit, wait, getpid, ..)
      - file (open, read, write, close)
      - network (socket, bind, listen, accept, connect, send, recv)
      - device (ioctl, mmap)
      - device drivers (In kernal space, via modules, Block (video) or Char (keyboard))
1. User space, runs applications
   - application run in some restrict mode
   - they interact with other parts of the computer via the kernel.
   - many of them can run.
1. The user space and kernel space run on different memory address spaces - so one cannot touch the other.
   - Virtual memory is divided into kernel and user.
   - The kernel space is on top (last addresses)
