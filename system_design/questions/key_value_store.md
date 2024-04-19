# Topic

In this topic we are discussing the implementation of a key and value store - which is persistant and scalable. We would need to take into account CAP theorem,

1. Consistency - all reads receive most recent data
1. Availability - every request is responded - even when some nodes are down
1. Partitioning - The system is fault tolerant against nodes down, or loss of messages between nodes.

In real world application partitioning would happen (unless we are using a single node) - we therefore are left with CP or AP, depending on system requirements.

We should also consider how the data if stored (if stored). This is similar to a Redis Cluster.

The storage will store, for each key, a value, e,g,

```javascript
{
    "A": "some value of any type"
}
```

When called, with the key `A` will return value `some value of any type`

# Problem

Design a key value store, with the following operations,

- `put(key, value)`
- `get(key)->value`

## Questions for requirements and design scope

1. Is it persistent? Yep. Must be persistent against recovery
1. What is the number of requests? A lot
1. The is the expected latency? - a few miliseconds
1. Is this high availability? - yes
1. What is the size of the data? - large, but increasing with time - eventually will not fit in a single server.

Limitations:

1. Do we have any? Not on resources
1. Number of servers - will scale with load? Yes
1. Network - Good network throughput but would be best to separated to zones. -
1. Can we write code?
1. Can we use an existing system (redis?)

# Basic design

We can start with a single server in memory, that stores the keys and values to the database. In this case, the database will allow the key/value to be loaded from disk (say as files) and to have a cache in memory to allow fast response. Cache is periodically written to disk.

We can use a failover method to be available, that is, we have another server that follows the master server, and requests are sent to that server in the case where the main server is destroyed.

we,

1. Keep everything in a hash table
1. Save periodically to disk.
1. Load data from that disk.
1. Lock multiple serving threads against a specific key.

## Consider two cases here

1. Eventual update - We do not need to wait until the everything is written to disk and return
1. Strict or Sequential - We wait before ack that the key has been updated. If reading is done, we can just return.

## Pros for this approach

1. Simple, and consistant. As long as we dont have too many requests.

## Cons for this approach

1. Scales veritically - not good.
1. Data will eventually not fit the server.
1. Large load -> large disk load.
1. If master crashes we may lose data - if follower did not catch up.
1. Cannot handle too many requests.
1. Requests from multiple zones would have to transverse network.

# Hash ring approach

For the hash range of method `hash` we will give each server a range... see more in consistent_hashing.md.

Using the hash ring method (without helpers), we can,

1. Map the key to a specific server.
1. Reduce the server load.
1. Evenly distribute the keys (would require virtual nodes)

To achieve **availability**, we can go to the next N servers (2?) on the ring, and store the key there
as well. This would mean that that server would also have this data, and therefore when the ring fails we would be able to resolve that key to within that ring.

Note that virtual nodes may be a problem here - we want distinct nodes and not to repeat them.
We may also need to take into account the network location - since similar nodes may be mapped to adjacent regions. In this case we would prefer nodes that map to the same hash region to be in different data centers.

For **consistency** we would need to implement some kinda consensus mechanism (raft, paxos, leader + raft, etc). We can define 3 numbers:
`N` number of servers
`W` the number of servers that need to ack, for writing.
`R` the number of servers that need to ack, for reading.

We then know, that if `W+R>N` then we have a fully consistent system, since there must be at least overlapping node for reads and writes that has to agree with the read value. Otherwise this system is not consistent.

We can also note that,

1. `R=1, W=N` -> fast read.
2. `R=N, W=1` -> fast write.

We should consider node failures. Consider that even if a node fails, the requirements for W, R, would ensure consistency.

## Eventual consistency

Note that even for R=1 W=1, and N>2 we should have eventual consistency. This is since the replica service will be defined as the next node in the ring. When a server drops, the next server will be, after a specific time period, the one to replicate to.

That said, two contradicting values may enter the system at the same time, since both server A and B may write at the same time. In this case we would need to resolve which value is best.

That can be done with a LogicalClock or a Vector Clock. We can pick a vector clock, to determine which key,value pair is most recent. Vector clock in general require us to know all the servers in the interaction, which not the best against adding and removing servers. But in this case, since we should know the active servers for a key (from the hash ring), that should be ok. Note that vector clock is not efficient since it needs to keep a record of the clock per key. But in this case, we can in general detect collisions even if we delete the older vector lock entries (as in dymanodb).

## Detecting nodes

Since its very important to detect which nodes are down, and we are dependent on `R` and `W` for our consistency model, we must implement a more robust model for identifying a server is down. For this we can use the gossip model.

1. Each server keeps a list of active servers with last seen
1. Periodically, each server picks `M`, where `M<N`, server to ping the heartbeat.
1. If the heartbeat succeeds and the server gets the active list of heartbeats from the new server, and updates the last seen to the latest.
   - optional - each server that receives a heartbeat pings another set of servers, and passes forward the update list. And updates the last pinged.
1. If the a server is not seen for a predefined period it is considered to be down.

## Handling node failures

If a server is down, and `R+W>N` then the system may be blocked for writing. In this case we need to handle the server down.

In this case we can use the first available `R` and `W` servers, which are not down, to get our quorum. "Sloppy quorum".

That said, we have danger in the case of strict writes.

1. More then half the servers are down - we cannot be sure if the current disconnect is just due to a network issue in our data center (split brain). We therefore cannot assume that our read of the network is correct, and that the other set is down. Writing is stopped.
1. Less then half - We can be assured that we are the dominant part of the cluster, if the other part sees us down, it would not be able to write since it should see more than half the servers down.

-> Goes to requirement, we need the server number to be non equal between data centers, so one data center can take priority. Better to have 3 zone for very high availability.

If enough time has passed we also need to offload the workload of the down server onto another, and in this case the ring can be adjusted, and data be rebalanced. If the down server(s) come back online we would need to rejoin them. This would cause a lot of data migration in the case where half-1 servers are down, but will persist the system against long term outages.

Synchronizing a server back uses Markel trees, or the log. Better to replay the log - its usually easier.

## High level design again

Client -> get,put -> (ring node) ---> quorum nodes.

1. We use a hash ring to determine where the key is stored.
1. Nodes are distributed, and redistributed through the ring as they join. (Self distribution is possible yet not efficient) -> we can do self distribution if we come up with a lock mechanism.
1. We define the `R,W` of the system to have `CP` if needed and determine the consistency level (Strict - `CP`).
1. Consistency is maintained by the vector clock (though inefficient). Resolves conflicts.
1. We handle node downs by gossip protocol, and re-balance of the ring.

## Pros of the hash

1. Can grown horizontally
1. Each server would map to a key.
1. No single point of failure.

## Cons of this method

1. When a server goes down - we would go to another server, but the key is not there..
   ..

# Discussion

## Availability and Consistency

We see that the service is available, and would be highly available if deployed across three zones, since each of the nodes perform the same task. If we choose the CP route `R+W>N` we can still have very high availability if at least more than half the nodes in the system can talk to each other.

For consistency, this depends on the system required. I can be from stick to eventual, but it would depend on the requirements.

## Performance and scale

Since we have multiple nodes we would be able to scale up to a massive amount of requests, as long as we dont have hotspots. We may need to introduce a load balancer - some control plane - that would reposition the nodes and add virtual nodes across the ring to allow us to redistribute the keys. For hotspots, we can increase the number of replications, but note that this cannot be done with just a key (not in this design). The replication must increase across the application.

Another issue may be that when multiple servers are down, large amounts of data may have to be moved across the system to facilitate recovery and redistribution of the nodes in the system. In some cases, it would be better to use a surrogate for the down node, without actually transferring responsibility -> this adds risk though, If there is only one "real" node that is left, and we lose that one as well, data may become unavailable.

## Monitoring

In the case of a key value store, we need to monitor similar things as the hash ring,
1. No hotspots -> many requests to the same machine
1. Mahcine load -> machine is working hard.
1. Machine metrics and machine down.
1. Key distribution.
1. Number of requests.

Using the above we can balance the system via by moving the location of the servers or adding virtual nodes in different locations around the ring, and then having the system re-stabilize, thus allowing further flexibility. If we have a control node then we can further optimize the system.

## Further optimization

1. We can consider that the ring we used here is not split into zones. We can consider that.
1. We can also consider a control plane that would redistribute the nodes and keys and add "helper" nodes to handle large traffic sets -> that is the helper node will be a temporary surrogate for the actual node, and allow writing to it. It will nevertheless not participate as a "real" node. This may be a way to handle hotspots.
1. When sharing the heartbeat between servers we can also send the status of the server load. So we have an updated list of all the node "states". In this case, we nodes see that one node has heavy load, they can assign themselves as surrogates and the hotspot can be handled.

