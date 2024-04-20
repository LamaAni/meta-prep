# Topic

A design for a url shortener -> creates a short url from a given url and will from there forward any url requests to a full url system

The job of the URL shortener is,

1. Provide a short url for a long url
2. Allow users to type this url -> from a printout, goes through a human
3. Will redirect to the true url from the short url.
4. Allow use of arguments in the matching url to the short url.

## Questions about scope and requirements

1. Is this a shortener for multiple companies, or just for one company?
1. Can I expect to be able to add parameters to the forwarded url?
1. Is there any "bad validation I need to add"?
1. Are all redirects permanent?
1. What is the number of requests per second i expect? 100 million generated per day.
1. Can a short url be remapped (edited)? what is the total cache time for that url? (time until remapping)
1. What is the persistance expected from the system?
1. What is the url generation latency expected?
1. Dose the short url expire?

## Questions about the limitations

1. Do we have any hardware limitations
2. Do we have any code writing limitations
3. Can we use existing systems (say Redis)?
4. Are we forced to use any type of database?
5. Data structure - a-zA-Z0-9

## Work scenario

1. Given a long URL - a short url is provided.
1. Access a short URL -> redirect to long URL.
1. High availability and scalability.

## Estimations and discussion

1. 100E6/24/60/60 - ~1200 generation requests per second; therefore at peak expect 10000 writes per second.
1. If we assume reads at least 10 times, we would have peak at 100000 requests per second - can be done with local memory cache?
1. Data size? If the shortener is running for 10 years -> then we have 365*100,000,000*10 = 365B records -> What database can do this? Would I need to create the key value store? Redis can handle max 4B records? we would need to make sure the db can handle this. Can cassandra handle it? (Cache would make it faster). Cassandra vs redis? Also assume 1b per record, we would have 365TB data.

We should consider the database we are using, and what the database can handle, that said, the database can be slow since we do not expect

# First description

First lets discuss what the service is doing. On the client side,

1. Client provides url
1. Client gets back a short url.
1. Short url is stored for time X in the system (can be forever) with its mapped url.
1. Each short url is unique.

On the user side (or request side),

1. User makes an http/s request for the short url
1. User get redirect response (permanent, 301)
1. User can go to the actual url.

Note that the request response is a permanent redirect and therefore the user not send requests to the short service after being redirected.

As for the client side, we will design this as an API (REST) -> GET, for getting the short url for a long url. This is not the most efficient and we may want to create a user "account" in the future to manage, but will do for now.
Our rest API is then,

1. GET -> params {long url}

So our api endpoints (note the v1, since we may have other versions)

1. srt.com/v1/\_create - POST or GET -> params {url} -> returns short url in form of srt.com/v1/[short_hash]
1. srt.com/v1/[short_hash] -> redirects to original url.

**NOTE** in this case a user can create different short urls to the same website with a `?oid=1,2...`, this gathering info about the statistics.

## Consider the hashing method

We consider a hashing method for `hash(url)` of url len ~100 chars -> unique value for this string hash. Since we know that the number of options for a hash is, `(number of options)^len`, we need to make sure that the number of hash values we have is much larger than the number of records we expect, which is ~400B.

We know we have 27*2 large and small, and 10 numbers. So ~52+10 -> 62. So we need 62^len>400e9 ~ 1e12.
`len*log(62)=12\*log(10) -> len=12/log(62) = 12/1.7 = ~7`

So a 7 char value should generate enouph values. If we take 8, that would be more then possible.

Since we don't want to invent the wheel we should use a known has function, say md5. For which the length is already bigger the 7. In this case, we can use a hash method that already hash the ability to produce an arbitrary length hashes like shake. Using may result in a bit more cpu usage, but we don't really care about this since we have more time creating the url (latency can be bigger).

Finally, we would like our hash function to map to the same url at the same time - so if we ask twice we will get the same result.

### Collisions

We can add collision detection using a serial number (our hash function would start at 1), this would
increase the time it takes to create a short url, since it would require a call to the database. This of course is possible but may not be required since we took 8 digits and not 7. This would reduce the chance of collisions dramatically. To get this collision, we expect to need `2^(n/2)` generations to get a 50% collision chance. Therefore, since we have 7 symbols, and therefore 8\*8/2=64/2=32, 2^32 is in the billions. We can in general just add one more digit and avoid it altogether.

## Components

Writes:

1. Our api would produce the short hash internally, without consulting the database.
1. Once a new short hash is created it will be written to the database, api will return after write.

Redirects:

1. Api will get a request from the clients and redirect them.
1. Api will resolve the short url first from cache, and then from database.
1. Api servers do not need to reload the cache since the short url resolution is atomic.

# Design

1. Backend database will be cassandra (or redis). Since each node can hold approx, 4B records, we would need to increase the size of this database over the years. The advantage is that the database can be slow.
1. All API servers are independent, and would work against the database directly. In this we have write and http requests.
1. All API servers have an in memory cache with limited size, where the cache is cleared in interval after a key has expired. If a key is access it is prolonged. Otherwise cleared in intervals (say 1 hr).
1. We do not expect a lot of service calls - since we redirect the result if the url response.

API actions

- writes: we generate the short hash. Check if exists in the database, if not, add it. If it dose, and different from url sent to write throw an error.
- reads: Lookup in the local cache, if not load from database.

# Performance, scalability

We expect the shortener system to be fast redirect, but slower on write. We, in general, do not need the system to be ultra fast in the redirect since we expect this call to be once in a while.

In terms of availability, since we have the ability to horizontally scale the API's we can just add more servers if the load becomes high. We can definitely apply a dynamic horizontal scaler. For the database, as the years go by and the size of the database becomes larger, we can add more nodes to the database, and make sure that our database. 

We can in general use a load balancer request routing since each server is effectively stateless (except for cache), we added the local cache just to reduce the number of calls to the database in the case of repeating calls. If we use a sticky resolve for our service this would be even better for repeated requests for the same short url - but may cause hotspots.

This would also be highly available, we can create the nodes in different regions, and make sure the database is spanning regions. In our DHS we would require that at least one api node exists per region.

# Monitoring
We would like to monitor:
1. Collisions - once a collision is detected (see api) - we log it, and the urls involved. We may need to add more letters to the url to allow this to be resolved.
1. Servers are available - we are using a DHS
1. Server load - do we need more servers?
1. Server cache size - we may need to decrease the cache hold time.
1. Database load - we expect this to be small, if not we may want to change from round-robin strategy.
1. Database size - we may need to add more server to the database.

Use prometheus if no in org system -> since we can send metrics properly and easily monitor loads.

# Further improvements

1. We can consider the case where our users may want to delete -> or redirect an old url to a new location. This would mean that we should allow
    - user accounts
    - user delete a short url.
    - user redirect a url. (Which should not override the old url but a different field? or maybe an array of urls).
1. We may want to add a rate limiter - but in this case, we should add it as a middleware.
1. Gather statistics for the user account - will allow to know how effective the api is.




