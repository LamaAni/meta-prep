# Question
After upgrading kernel the machine fails to boot, what will you do?

# Answer

## Triage

1. What is this machine? - a webserver, handing api requests
2. Is it critical? - nope, other machines exist
3. Is there another machine taking its place? - yeap, we already pre-configured another machine
4. What dose it serve? - api requests for the api server.

**This is not critical, handle the issue**

## Info gather 1

### Checks
1. do we have access to the machine, can I boot into the grub menu? - yes you can, via the VM GUI
2. Is there another kernal installed? no. Just one drive, one kernal.
3. Can I boot from a thumb drive? - no
4. Can I mount another drive via the VM and try and boot there? - yes

### Actions
1. I mount another drive, via the VM manager.
1. Iry and boot to that machine on the new disk (Best approach if its a fresh install of easy to use toolset - ubuntu? )
1. If the boot from another is not available, I can use the grub rescue option to find what is wrong with the boot sequence.

## Info gather 2

### Checks
1. Once booted on the other machine, I check for errors in the syslog, if bad sector run fsck, or check fstab
2. I mount the disk, and check the boot directory for obvious errors (empty, or missing kernal) - no errors, kernal looks ok. File is there.
3. I check the boot.log file, and see what errors I find. It is possible the grub was misconfigured -> need to make sure the error is not from hardware, but is rather curruption or something not installed properly, I can try and recover the grub if its the grub. Otherwise, if the error is not hardware, maybe it would be best that we reinstall the os. - Error is in the init sequence, one of the start services is errored.
4. I can chroot and then try to run that app from there - this is a unrelated service that failed, and it seems a long debug, I'd rather install a new fresh os -> unrelated to services.

### Conclusion
1. There is an error in the system in the init sequence the error is unrelated to the webserver.
2. We can debug the error using chmod, but that may be not the right approach since the webserver is alreayd down.
3. We should probably reinstall the server, after backing up the server data.

## Resolution
1. I back up the server, copy the data to my rescue disk. I also copy the webserver code and other non packaged dependencies. I make sure to separate these
2. I check what is the os that is needed to be installed, is there an image?
3. I create a new VM disk, with same size and configuration, and attach that disk to the server.
4. I install an os on that disk, depending on the webserver configuration.
5. After adding the grub entries, I reboot to the new fresh os. 
6. Install the webserver and copy the data. 
7. I test the webserver. If all is working, bring it up online.
8. I keep the rescue disk and the original disk, and add a ticket to remove them if everything is working within a week.
9. I notify the team this would take a bit while... 