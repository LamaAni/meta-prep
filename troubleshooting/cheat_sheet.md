component |  type |  metric
--- | --- | --- 
CPU | utilization |  system-wide: vmstat 1, "us" + "sy" + "st"; sar -u, sum fields except "%idle" and "%iowait"; dstat -c, sum fields except "idl" and "wai"; per-cpu: mpstat -P ALL 1, sum fields except "%idle" and "%iowait"; sar -P ALL, same as mpstat; per-process: top, "%CPU"; htop, "CPU%"; ps -o pcpu; pidstat 1, "%CPU"; per-kernel-thread: top/htop ("K" to toggle), where VIRT == 0 (heuristic). [1]
CPU |  saturation |  system-wide: vmstat 1, "r" > CPU count [2]; sar -q, "runq-sz" > CPU count; dstat -p, "run" > CPU count; per-process: /proc/PID/schedstat 2nd field (sched_info.run_delay); perf sched latency (shows "Average" and "Maximum" delay per-schedule); dynamic tracing, eg, SystemTap schedtimes.stp "queued(us)" [3]
CPU |  errors |  perf (LPE) if processor specific error events (CPC) are available; eg, AMD64's "04Ah Single-bit ECC Errors Recorded by Scrubber" [4]
Memory capacity |  utilization |  system-wide: free -m, "Mem:" (main memory), "Swap:" (virtual memory); vmstat 1, "free" (main memory), "swap" (virtual memory); sar -r, "%memused"; dstat -m, "free"; slabtop -s c for kmem slab usage; per-process: top/htop, "RES" (resident main memory), "VIRT" (virtual memory), "Mem" for system-wide summary
Memory capacity |  saturation |  system-wide: vmstat 1, "si"/"so" (swapping); sar -B, "pgscank" + "pgscand" (scanning); sar -W; per-process: 10th field (min_flt) from /proc/PID/stat for minor-fault rate, or dynamic tracing [5]; OOM killer: dmesg | grep killed
Memory capacity |  errors |  dmesg for physical failures; dynamic tracing, eg, SystemTap uprobes for failed malloc()s
Network Interfaces |  utilization |  sar -n DEV 1, "rxKB/s"/max "txKB/s"/max; ip -s link, RX/TX tput / max bandwidth; /proc/net/dev, "bytes" RX/TX tput/max; nicstat "%Util" [6]
Network Interfaces |  saturation |  ifconfig, "overruns", "dropped"; netstat -s, "segments retransmited"; sar -n EDEV, *drop and *fifo metrics; /proc/net/dev, RX/TX "drop"; nicstat "Sat" [6]; dynamic tracing for other TCP/IP stack queueing [7]
Network Interfaces |  errors |  ifconfig, "errors", "dropped"; netstat -i, "RX-ERR"/"TX-ERR"; ip -s link, "errors"; sar -n EDEV, "rxerr/s" "txerr/s"; /proc/net/dev, "errs", "drop"; extra counters may be under /sys/class/net/...; dynamic tracing of driver function returns 76]
Storage device I/O |  utilization |  system-wide: iostat -xz 1, "%util"; sar -d, "%util"; per-process: iotop; pidstat -d; /proc/PID/sched "se.statistics.iowait_sum"
Storage device I/O |  saturation |  iostat -xnz 1, "avgqu-sz" > 1, or high "await"; sar -d same; LPE block probes for queue length/latency; dynamic/static tracing of I/O subsystem (incl. LPE block probes)
Storage device I/O |  errors |  /sys/devices/.../ioerr_cnt; smartctl; dynamic/static tracing of I/O subsystem response codes [8]
Storage capacity |  utilization |  swap: swapon -s; free; /proc/meminfo "SwapFree"/"SwapTotal"; file systems: "df -h"
Storage capacity |  saturation |  not sure this one makes sense - once it's full, ENOSPC
Storage capacity |  errors |  strace for ENOSPC; dynamic tracing for ENOSPC; /var/log/messages errs, depending on FS
Storage controller |  utilization |  iostat -xz 1, sum devices and compare to known IOPS/tput limits per-card
Storage controller |  saturation |  see storage device saturation, ...
Storage controller |  errors |  see storage device errors, ...
Network controller |  utilization |  infer from ip -s link (or /proc/net/dev) and known controller max tput for its interfaces
Network controller |  saturation |  see network interface saturation, ...
Network controller |  errors |  see network interface errors, ...
