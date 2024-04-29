# Question
Server is not reachable or cannot connect

# Answer

## Triage

**Should the server be accessible from that network** 

### Questions
1. Is this a critical server? Is this prod? What is being served there? - its a queue service, in prod - kafka, or rabbitmq or redis
2. What are the processes using this message queue, are they working fine? - yeap. Looks like it
3. Is there metrics for this server. Can I see the metrics without logging in.

### Questions - next
* Should be reachable
* Its a critical service, so we have to check if messages are being dropped. Need to check the other DB end? Is there
any record of how many messages have been processed and how many are coming in? If so compare -  messages are being processed, but there is a backlock of messages growing.

### Conclusion
1. Alert the team of a `sev` since this is prod and we may be losing data on channel, but proceed withput pulling people in. The service looks as if its running. Check further.
2. Probably a network issue for the connection or a load issue. 
3. Looks like there is a load issue since the messages are not transferring.

## Investigation 1
***Focus on load first*** - since this is the critical 

1. Check `ping` `tcproute` and `nmap` to this machine. - got port 9090 open, TCP. Service is working
2. Can I ssh inside the machine? - yes. Ssh works, but fails sometimes.

## Investigation 3
1. ssh into the machine, check the top and see the load -> memory ok. swap ok.
2. do `sar -d 2` -> see lots of writes to disk, utilization is ~95%. Check `iotop` to see the disk usage by pid
3. ? Message queue is not the culprit -> but rather a defrag is running. Stop the diffrag. 
3. ? Message queue is the culprit -> too many messsges.
4. Is the disk slow? What kind of disk? can we create a new disk and upgrade the current disk? If so, can we hotswap the disk location?
5. Can we shut down the service for a few seconds without losing messages, if so, proper shutdown and disk swap. 

### Actions
1. Notify the team that we are losing/have backlock of messages due to overload. The machine cannot handle the number of messages.
2. If the capcity of the queue service can be increased (e.g. elastic, kafka) then try and increase the size of the message queue service (hoping there is a gateway, roundrobin)
3. Check and monitor the result. MAke sure the backlock is decreased. 

**If the capacity cannot be increased**
1. We need to create a new service to store the messages, with more resources and do a hotswap. In general, if there is a gateway we can do the hotswap through the gateway.
2. We need to make sure the configuration of the new service is the same as the old.
3. Test the new server against a set of command tests, make sure to follow CICD if possible.
3. Copy data before (rsync?) shutting down the old server.
4. Old server shutdown, rsync, hot swap on gateway and start new server. 

### Post actions
1. Add ticket to look into distributed and load calculations.
2. Add PostMortem
3. Check what other solutions had gone bad and why we have not recived error messages from the message service telling us there is a backlog.
