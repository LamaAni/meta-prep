# Question
You are unable to do ssh to a node, what could be the problem?

# Answer

## Triage
Find out the urgency of the situation - e.g. 

**FIRST** check policy -> is ssh supposed to be open? If can't tell right now and got an error ticket assume yes, but dont open the port until get confirmation.

1. What dose this machine do? - its a database server
2. What port is the database and what type? single machine postgres server.
3. What dose this database serve? Message queue
4. Is this a prod server? Yes
5. Do I have metrics collection for this server? No
6. Do I have access via some other terminal (GUI, or the VM system)? No

### Rslt
* The database serves a critical message pipeline
* Its a single server database with a failover
* No other means of connection.

**Criticality** The server is a critical component since its a single machine database and
is required in a production environment.

### Actions
1. Check the database is responding to connections using nmap -> what are the open ports.
2. Is the database active? Can I log in (if I have creds)
3. Check for postgres healthcheck service, if exists. If not try and find out if health check is ok.
4. Check other services that use this database to check for alert or errors. `nmap` should give some info about that. 

### Rslt
* Server is responding, but is slow.
* The other services, using the database, are not showing errors.
* Good index query returns in good time.
* No backlog on messages queue -> seems the service is working.
 
### Conclusion

**No need to raise the alarm**, something is probably wrong with the ssh service, keep monitoring the message queue
and see if messages are building up.

## Identification

**We first need to access the server**

### Actions
1. Do a `traceroute -p 22` or `tcptraceroute -p 22`, am I stopped on the way to the server? (I know the db is working.. so), is the connection dropped (filtered)?
2. Is there another user I can use. Dose that user allow me to access the ssh. Try that user
3. Do I know another machine on that network? Can I connect from there?
4. Do I know another machine on a different network? Can I connect from there?

### Rslt
* `traceroute` ok -> we are reaching the machine. But connection on `netcat` is refused on port 22.
* No other user I know or can use.
* I cannot reach the other machine on the network -> port 22 is not open.
* I can reach the machine and login via a remote host on a different network (prod). 

### Conclusion
**Probably firewall settings have changed** the service is available, need to check changes with the team and track the firewall changes. 

## Identification 2

### Notes
We are accepting this ssh connection with this user. This means the service is running and permissions are ok. The machine needs to be checked in any case, to see that the connection drop is not accidental (unlikely). If it is another user, we need to check if our original user has a lock, or is not allowed ssh

### Steps

1. Check top -> is the computer overloaded? (Probably not, service is ok, if so -> open another ticket) (We check this since we are already here)
1. Check if the firewall is active, and look for drops on the iptable list.
1. Check the machine sshd service to see if its running -> are there any ssh connections open to the machine? What is the origin `netstat`
1. Check if we can detect the machine that is blocking the port. (traceroute, lcoal to remote)

### Rslt
* Machine is not overloaded. Service is ok, but is heavy.
* Machine is not blocking the connection, firewall ok.
* Traceroute shows that the connection is blocked along the way -> we are blocked by admin

### Conclusion
1. We are blocked by a recent change in the network
2. Machine is running well, and service is ok.
3. If the ssh needs to be open (without a gateway), open a ticket to the admin.
4. Notify that currently connection via ssh is disabled, but you can access via another machine in prod. Until fixed.


###