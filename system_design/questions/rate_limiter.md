# Question
From `System design interview - insiders guide`

In a network system, a rate limiter is used to control the rate of traffic sent by a client or a
service. In the HTTP world, a rate limiter limits the number of client requests allowed to be
sent over a specified period. If the API request count exceeds the threshold defined by the
rate limiter, all the excess calls are blocked. Here are a few examples:

1. A user can write no more than 2 posts per second.
1. You can create a maximum of 10 accounts per day from the same IP address.
1. You can claim rewards no more than 5 times per week from the same device.

# Questions on scope

1. Client side or server side (was not defined in the question)? - We are creating a server side rate limiter.
1. Based on IP, UserID .. etc? - Should allow for multiple types of rules (like nginx)
1. Scale ? Startup or mid or large? - Large number of requests. And should scale horizontally.
1. Is it in application code? Or a separate system? - Up to me.
1. Do users get informed that they are throttled? - yes.
1. Can requests be lost - yes. We may respond with error to some requests.
1. Is this a soft or hard rate limit - can we deviate? What are the limits.

# Requirements

- Accurately limit excessive requests.
- Low latency. The rate limiter should not slow down HTTP response time.
- Use as little memory as possible.
- Distributed rate limiting. The rate limiter can be shared across multiple servers or processes.
- Exception handling. Show clear exceptions to users when their requests are throttled.
- High fault tolerance. If there are any problems with the rate limiter (for example, a cache server goes offline), it does not affect the entire system.

# First high level design, Simple in application approach

**NOTE:** Can just show the design and not explain how it works. And just move on to a better high level design.

## Design

1. Inside the application. Checks request by rules.
1. if too many requests are generated block - return 429 on http requests
1. We record the "request status" in a persistent database (Say cassandra, or much better redis cluster - better redis) and load the state from there.
    * We can use a single redis instance if the number of requests is low enough with a failover. This would give a faster response time, but not sure how it would handle scale.
    * We can also try and implement a token bucket in the redis server, 
1. Cache cannot be used.

## Disadvantages

1. Overhead request for every request (we are synchronized by redis backend - avg. latency is 12ms, or redis with 1-2 ms). For redis some faults may occur and larger latency if we are using the persistance (store to disk option), though in this case it wont be needed since if the whole cluster is reset - we may lose some performance for short while. Not sure if this can be overcome since we need to synchronize.
1. Scales with the api layer, but we may want to scale differently.
## Conclusion

We match some requirements but would slow the application if the rate limit check is slow. It would
be better to use some kinda cache but we cannot do that since we are synchronizing the application with the user.
In general, and depending on the number of requests per user, one may think we can assign a user to a specific API entrypoint.

Another issue with the design that it is not separated from the application and is dependent upon it. It cannot be generalized as a deployment on its own and therefore cannot be tested on its own. This may fit a company with less resources, but may need to be generalized for the case of a larger company that would have multiple apis that use the same rate limiter. In this case, it would be better to have an APIGateway that implements the rate limits.

**Note** that this methodology would also reduce the load on the internal network since it would note the client to redirect the call to a specific api server. This would mean that the calls would go directly to that api server and not require in-network communication.

**Note** that using a cache server here (DHT, or any other) may not be the best approach. The cache server would be invalidate every time we update the key, and therefore at each call.

# Second approach, rate limiter as middleware (API Gateway)

In general, there are api gateways out there (Kong - Nginx based, supports IP and username - but we can add a plugin - in lua, or use the webhooks) which will be distributed and fault tolerant. Since we are designing this middleware I would assume we need to write code for it.

## Design

1. The API gateway's requirements are
   - Pass requests to the requested apis.
   - Rate limit
   - Return requests to the client.
   - Allow that service to synchronize to fast response database (say redis)
1. Cache the response to the rules for each request parameters. E.g. we should not process the request parameters to get the limiter rules each time.
1. The api should be written in a fast enough language that dose not require a lot of memory. This is since we should not have a large load on this service.
1. Even if we use the token bucket to get requests we are still required to take a token from the bucket and update the bucket for every request -> this would increase latency. Fastest latency is in memory.
1. In this case, and since we are using the middleware as an application gateway, we should also allow
   - Webhooks with cash - to interpret parameters
   - Custom Roles.
   - Auth and barer tokens.

## Notes
1. We can use lua script to do the Token bucket implementation, using the lua code to return the current token bucket count. We can also check the timestamp in that lua script, thus allowing very fast response from the script. We should consider locking.

# Performance and Scalability
1. Its best to use multiple zones.
1. It would be best to use the external database cluster, with implementations in multiple zones.
1. Use dns and not ips - more reliable.
1. Use failovers (if using single nodes for anything)

# Monitoring
1. State of the service
1. Is the algorithm working
1. Is the algorithm following rules.

The question of how to monitor will check need to check the number of requests per second in a different manner than the database, we are actually checking the total requests. This can be done by implementing a request recoding schema, with pass/fail (either in redis, kafka or another database, so the data can be processed later and checked). We can also record these metrics in some database where a hash of the parameters of the pass fail can be loaded. We should not record all requests - that would be a lot, but rather limit it to some request token hash ranges where this is recorded.

Since we are recoding metrics, and these metrics can be done in the API Gateway off time - that is when its not bz. We can suffer some data loss here but not a lot.

For the services, a monitoring service (either internal to the org, or we use something like prometheus), where we can monitor the service online. Note that prometheus is not a direct push but has a gateway - but this would work for our example.