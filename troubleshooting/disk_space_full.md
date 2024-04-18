# Question
We get an error from an application Disk Full, on server myser.fb.com, check causes.

# Answer

## Triage

### Investigation 2
1. What is this server? What dose it serve? - file storage application
2. Is it critical, dose it run in prod? Is it a part of a server group? - prod. Upload file service for user forms. Single machine
3. What services are using this server? - webservers, mainly the tax forms.
4. Is that service critical? yes. But can accommodate some downtime.

### Investigation 1
1. Check server is responding; `nc ... 22` on the ftp service. Can I ping the server? - service active
2. Check errors coming from website services - is there any errors related to uploads? - a few, not a lot. (Maybe later)
3. Can I upload manually? If so - service is responding, but some space was full.

### Actions
1. Notify the stakeholders there may be an issue with this service, but we are seeing mixed results. Working on it.
2. Alert team but dont pull anyone in.

### Investigation 3.
1. Try and ssh into the machine - ok
2. Run `df` and `df -h` to see how many inodes are consumed on which drives -> I see 4 drives, with one drive 100% Inodes ext3. mounted @ /data/store2
3. Other drives are ok.

### Actions 
1. First releave the issue. Check which directory is the largest (number of files) check if there are subdirectories.
2. If there are, and they have not been modified lately (in last hour or two), its possible to copy them to another location if modified has not changed.
3. Then symlink and that should remove some inodes and allow the process to continue.