# CPU is under high I/O. How to find the issue?

1. What is this machine
1. What dose it do..
1. Details about it.

Since cpu is under high IO wait?

1. Is there anything that should be writing to disk on this machine? (iotop, or atop->f->d)
1. If don't know -> run either atop, or sar -d 2, to see if something is actually writing. If so run iotop to see what is writing.
1. Are there multiple processes that are writing to disk?
1. What is the memory like?
1. What is the cpu io_wait? (atop or mpstat -P all ) is it any cpu in particular?

# We have possible?

- Slow network
- Heavy workload (Heavy read write)
- Bad software (assume not)
- Storage bottleneck or write crash between two.
- Bad drive.
- Processes in Uninterruptable sleep state

# Check components

1. CPU
1. DISK
1. Network

Check network, (sar -n DEV,EDEV) looks ok. Low transport, and almost no errors.

- Saturation (no dropped) ~1 %
- Utilization ~1 %

Check DISK (sudo iotop ) - write is not high. Two programs writing.
Utilization looks ok 20% but wrqm is high. -- investigate further.

Check cpu (mpstat -P ALL 1) -- cpu is mostly idle.

# Investigate

1. Disk (what writing)

- Check the iotop and see which apps are writing. Two processes are writing to the same file.
- check load. And check if the apps are in uninterruptable sleep we have 10 of these.
- check open files -> are they writing to the same file? - yes they are.
- they are probably blocking each other.
- are they supposed to be writing to the same file?
