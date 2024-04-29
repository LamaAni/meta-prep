# CPU is under high I/O. How to find the issue?

USE method resources like,

1. CPUs: sockets, cores, hardware threads (virtual CPUs)
1. Memory: capacity
1. Network interfaces
1. Storage devices: I/O, capacity
1. Controllers: storage, network cards
1. Interconnects: CPUs, memory, I/O

for each resource, 3 metric types,

1. Utilization - Avg. time resource is bz. Can be identified in % of timespan. (100% no more work). Represented as %/time (100% in the last minute)
1. Saturation - How much of the resource is bz. (Can be more than 100%, i.e. buffered work) Queue length (cpu - vmstat 1 'r' column, or iostat -xnz 1, "avgqu-sz" > 1)
1. Errors - Errors, found in logs. (dmesg)

Note that , low utilization dose not mean no saturation -> e.g bursts of work.

