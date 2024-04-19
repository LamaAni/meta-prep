# Topic

Unique ID generators allow us to create consistant id's in a distributed system. This therefore allows either synchronization of ids for storage or ticketing or tokens. May also allow us to identify events. 

The requirements for such a system would be,
1. Fast,
1. Non repeating
1. ID type,
    * Random
    * Sequential

## Questions about requirements and scope
1. Dose all ides have to be sequential ? No
1. Dose it have to be unique? yes (hence the name)
1. That data type?
    * Just numbers
    * 64 bit int
    * Sortable
1. How dose it increment? Increments by time, relation to time - but not necessarily sequential.
1. How many id's would we require, would a database unique key handle this? A lot, and No (10000/s)
1. Whats the latency? As fast as possible.

## Limitations and system requirements
1. Do I have good network? yes
1. Multi zone? Yes
1. Do I have any storage limitations? No

# Design options

## Multi master (Simplest approach)

### With counter id
Create a multiple nodes, each node has
1. Cur id = Node Id
1. Node id = 1..N

Where N is number of nodes. Every time we increase the counter, we do it by N. This way if we have,
nodes: 1,2,3 N=3,
Node 1: 1, 4, 7, ...
Node 2: 2, 5, 8, ...
Node 3: 3, 6, 9, ...

Which keeps the counter persistent. We can serve as many ids as we like.

**Cons**
1. Very hard to scale, when we add nodes or ordering is off
1. Dose not follow go up with time since we can have id 4 then 3s

### UUID

The chance if generating multiple UUIDs of the same would require us to generate 1B ids/s for 100 years. Yeap. Were good.

Just multiple masters generating UUIDs (or the application just generates one)

## Issues with multi master

Not the best since it may scale to medium sizes and may not provide us with a good approach for generating the id. In the case of UUID, this problem my be solved but would not follow that all ids can be sorted in time.

## Multi master, with zoning and server id

Consider having the following server properties,
1. A local clock
1. A server location id, e.g. "{zone}/{datacenter}/{rack}" -> 3/5/1
1. A server id (uuid)
1. A server counter (increment 1)

We can now compose an id that would be always unique, and would produce a time series assuming the data clocks are roughly synchronized.
```
[ts][locaiton id][uuid][#]
```
And for the server we would increment the counter every time. Now we can
1. Add as many servers as we like
1. Will get a time series.
1. Will have absolute order at least within one server.

# Performance, availability and scalability
We can see since we have multiple masters, we can easily generate ids, and if one server fails, gets removed or added the id generation is still valid. We can also create servers in multiple zones and centers and we would still have good ids as long as we can sync the times.

# Monitoring
In general we want to monitor
1. Server load - add more servers if too many requests
1. Time keeper server, and make sure these are synchronized. 
1. The servers are time synchronized.

# Further optimizations
1. Sync the servers time to a single instance time keeper with failover to allow the clocks to be synchronized. Even if this server fails, the clocks will be still roughly synchronized for enough time that the clock service can be recovered. 


