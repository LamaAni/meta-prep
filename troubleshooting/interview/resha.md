# CPU is under high I/O. How to find the issue?

# What can go wrong in the filesystem?

- Currupt files, Bad sectors (fsck)
- Heavy workloads
- Software locks
- Storage layer bottlenecks (large queue, large latency)
- Devices just too slow for writes.
- uninterruptible sleep state (check)
- Degraded or failing drive (check dmesg)

# What if the system has no more inodes available?

(df -i) - check the inodes. Check dmesg

Indicators:

- Data loss
- Applications crashing
- OS restarting
- Processes don't restart
- Periodic tasks not firing
- New files won't show up on the compute

Actions:

- check disk space.
- check inodes count
- a response to write commands?

# How to increase your I/O?

- reduce the number of opertions and write larger blocks.
- Use raid (software Raid)
- increase the in memory IO cache size.
- Separate the main IO offenders into different disks.
- Separate sequential apps and random apps (database) to different disks.

# How to tune I/O?

- change the scheduler (/sys/block/DEV[sdc?sda?]/scheduler ) (cfq, noop, deadline - kernel schedulers)

  - noop - FIFO
  - deadline - gurentee a start time (Best for reads) (Change in case of heavy reads.)
  - cfq - tries to maintain the access fairness.

# You can’t see your mounted filesystem. What can be the issue? etc.

- Access
- Is the mount available (findmnt)
- Is the device available (df)

# Someone started forkbomb on your system how would you stop it? Google

- find the root
  'ps -ao cmd | grep -Eo "^[^ ]+" | sort | uniq -c'
- kill it.

# How would you troubleshoot network communication between two servers?

Issues can be:

1. Server can access.
1. Cannot reach each other.
1. CAnnot resolve DNS.
1. Has communication issues.
1. Firewall issues. iptables, and nmap
1. Port is closed.

- dnslookup
- tracerout
- ping
- nmap
- (internet connection)
- check services are active.
- check on both servers.
- check external access.

# Question: You are trying to run the command but it says no more PIDs available. What can be the reason? How will you solve the issue?

- Check /proc/sys/kernel/pid_max
- Check `sudo ps -axo pid | sort | uniq`
- Am I running in a cgroup.
- ulimit?

- ulimit (check `ulimit -a`) for your user/group is set to very low. You can't create processes more than ulimit range.
- Someone started fork bomb. There are no PIDs available actually.
- All PIDs have specific fd in the file system. You are running out of inodes. No more inodes. (df)
