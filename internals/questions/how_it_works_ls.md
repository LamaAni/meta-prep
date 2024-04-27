# What happens when you type ls -l

I'll describe the process going from

1. The hardware
1. The kernel (input)
1. The shell + parsing
1. The application ls

## Hardware

The user press the key, which generates a signal in the motherboard input. This is mapped to the device input, which is mapped to the memory (Memory mapping vs bus). A hardware interrupt is then called and this signal is transferred to the kernel.

## Kernel

The kernel receives the signal and triggers the right function that handles the event and data. This adds the keystroke to a buffer. We write 'ls -l'. Then press enter.

## The shell

Note that the shell program started before we started typing.
