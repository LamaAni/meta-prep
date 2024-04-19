# Topic

To achieve saleability, we must distribute our load across multiple servers. To get this to work consistantly we would need a way to fast identify the server or server group to handle the request. We may also need to implement some kind of cache where we have multiple servers with a fast response. 

## Problem statement

You have a web-server, connected to a cache backend. The amount of requests for this servers is large, but most requests and resources are static. How do you implement the cash system?

## Requirements questions
1. What is the total amount of requests -> very large. Assume no single cache server can handle it.
1. What type of data is served from cache -> Text responses, from small to medium. 
1. Is the bandwidth of the system good enough to serve all requests from the cache service.
1. Data is pulled from backend storage? What is the latency? - backend storage is slow. Data is set by the application -> set cache value, with expiration time. 
1. Are keys evenly fetched? - no - potential for hostspots.

## Limitation questions
1. Do I have hardware limitations - e.g. I have only low grade computers. I have small network bandwidth .. etc.
1. Do I have coding limitations - e.g. is my team large enough to develop code? - yes
1. Can I use off the shelf systems - e.g. redis? - no

## Data questions
1. What size of data? - small to mid, max 1mb
1. What type of data? - text mostly. No video.

# Basic naive design

We can in general use a very basic hashing method where, if all cache server ip's are known to all other webservers, we put all known servers in a list and select the server vai a hash method, where:

`server_idx = hash(key) % len(servers)`

This would produce a consistent cache server ip, as long as we are not adding or removing servers from the list.

## Pros for this approach
1. Simple
1. Requires only a registry of servers, which can be achieved by another database
1. Keys are evenly distributed.

## Cons for this approach
1. Rehashing - will require the rehash of the data in the servers, if a server is added, fails, or removed. The rehashing will happen on all servers, since the hash is not consistent.
1. Has a lot of potential for hotspots - keys are evenly distributed but not all keys are accessed the same amount.

# The hash ring design

We can use a hash function, and this time instead of modulu assing each server a range within the hash function. That is, say out hash function produces a range of 1-100, and we have 3 servers,
server 1 -> 1-33
server 2 -> 34-67
server 3 -> 67-100

Now if we add a server,
server 1 -> 1-25
server 2 -> 26-50 ...

Note that the number of rehashes that are needed are less. server 1 has no rehashes to do, only server 2 dose.

## Pros for this approach
1. The hash is consistent, we are not rehashing a lot.
1. Adding and removing servers is easy. Failures are tolerated, but just going to the next server in line.

## Cons for this approach
1. Keys are not evenly distributed - potentital for hostspots
1. The hash range may not be evenly distributed.
1. Keys are not accessed evenly - potential for hostspots.

## Improvement
If we map the server more than once on the ring, we can in general distribute the keys better and reduce the hash range the occupy. This would mean that a hash server may have non overlapping hash ranges and that would also improve the key distribution.

Finally, we can move/remap/add extra nodes for servers which are idle in hotspot area allowing multiple hash nodes to serve the same area. For this though we must monitor the hash ring - which would mean metrics and a control plane.

## Solution summary
1. Use hash ring
1. Use multiple "virtual nodes" in the hash ring - to balance out the key distribution.
1. Monitor the hash rings keys called, and adjust the positions of the servers on the hash ring - may cause redistribution and cache miss, but would work better in the long run.
1. Add "helper" servers in an either configuration at the same location in the hash ring. This would distribute the calls randomly or round robin between them. This would mean two servers will be serving the hostspots.

## Performance and scalability
1. The hash ring solution would be performat, since they keys would be distributed across many servers.
1. It would be scalable, we can add or remove servers.
1. Would not need, in the basic solution, any monitoring service.
1. Monitoring (say with prometheus) would allow metrics and therefore allow the redistribution of virtual nodes, or adding "helper" servers.
1. Scale would be limited by the registry.

## Availability
We would also need to consider the network location (locality) of the requests. We may want to add "helpers" for each region, for each keyset, this way we could reduce the networking work needed when deploying the service. The locality of the servers would allow less network traffic which is a shared resource

We would not want our system to be overloaded at specific locations, or to wait a long time for traffic. We could in general, if we have a control plane,
1. Add "helper" servers in specific networks where these are needed.
1. Move servers, and server groups to match a smaller range of servers.

## Monitoring
By implementing a metric services, we want to make sure that no server is overloaded, and we are distributing the keys properly. We can check that by monitoring
1. Number of keys per server
1. Number of requests per server

Given that, if we have a control plane, we can adjust the number of "helper" servers and assign helpers for each of the monitoring service.

## Optimizations
1. We can consider the helper servers, or server hash range groups as a methodology that would allow us to optimize our services.
1. The control plane can be made inside the cache servers, notably, a server with less load dose some monitoring and reorders itself and its friends. 
1. The control plane can be persistent.
1. We can introduce a second layer of "hash" rings for regions. That is instead of looking at one hash ring we can look at two, one identifying the region and one ring per region, identifying the region. Since the next server rule will apply, this should behave across regions?

# Conclusion

We implemented a hash service which is implemented in a consistent hash ring. We improved on that by adding virtual nodes and server groups (instead of single server) - we could also use multiple rings.