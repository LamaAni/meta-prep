# Linux booting process

In general the steps are,

1. Computer loads
1. Bios checks
1. Bios look in boot record -> loads grup
1. grub -> looks in its records -> loads /boot directory and kernel.
1. once kernel running -> starts the boot sequence in as defined in /etc
1. System configurations (devices - fstab, other configs)
1. Loads services (systemd and/or init.sh)
1. Scripts
1. Then either
   - terminal
   - UI load
