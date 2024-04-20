# Topic

A web crawler is a software that ingests a url html, reads all of its internal url, and follows them to repeat the same action. It should not read urls repeatedly.

We should have,

1. Rules - what to follow
1. Info - what to collect.
1. Expiration - do I need to check this again, when? If nothing has changed, should I check it again?

## Questions for scope and requirements

1. What is the purpose of the crawler? Is it for general purpose?
1. What do we expect to crawl? What is the expectation of the craw size (single website, the whole web)?
1. What are we crawling (http)?
1. What is the expectation of called websites per day?
1. If a website has changed, what is the latency we expect for these changes?
1. Do we record redirect response or error responses?
1. Do we expect this to run all the time? Can we have downtime? What is the availability?
1. We expect to be solid against partitioning? yes
1. Can we have a centralized database for urls to be crawled? yes

## Questions for Limitations

1. Do we have any server limitations? Yes - max N servers.
1. Do we have any data size limitations? Yes - we are collecting the metrics, and should not collect history or clones.

## Simple design (Buy in)

We have a seed of websites to crawl, for each one:

1. We collect the data
   - if redirect, follow,
   - if html, create a hash of this html, and check if the hash has changed in the database, if it was not, ignore this url.
   - if html, collect all urls, check the rules, and add record for each url to crawl in the future.
   - for all urls collected, add them to be crawled in the future.
   - mark this url as crawled, the time it was last crawled, and its html hash if any.
   - Use the data (html, or other), and process the metrics needed or send to metrics server to process. Store them to the db.
1. Go to next url in list to be crawled.

This process will crawl all the websites that we need to.

## Issues with design

1. If we have multiple servers, server a can start crawling, and before it finishes, server b will start crawling
1. The metrics servers can easily lag behind the crawlers - we need to make sure the metrics servers are not lagging behind. This can be done by either collecting the metrics while crawling in the same process, or throttling the crawl according to the metric server load.
1. Throttling - is not taken into account.

We can solve the sync issue by adding a message queue, with ack.

1. Each url added will be added to the queue, with expiration date.
1. Each crawler will load the next website to be crawled from the queue, and will ack once done processing.
1. If no ack was ack in time, the message will returned to the beginning of the queue.

## Data size

In this case the final data size should be the metrics we store, plus the size of hash \* number of urls to be crawled. For the entire web this would be trillions of records. That said the crawler can be slower, since we care less about latency but rather care about the total number of urls crawled per hour or day.

If we plan to crawl 1B websites in a month -> 1e9/30/24/60/60 = ~300 per second. With peak (NYQUIST 600 per second).
Html data for page is on average 100kb per page -> 600MB per second. (definitely need more than one crawler :)

## Duplicate content

We should also consider the case where two links of the same website that lead to the same content. We should take this into account when checking the data.

## Seed urls

We would need a good seed to actually find all the locations to crawl. This would be taken as popular websites, blogs and q/a websites like redit from which we can reach the entire web. This would be a project by its own.

## Crawler work

Our crawler, may have lots of work. Since we don't know what crawler load would be. This would mean that we may want increase the number of crawlers according to the pending number of links to crawl.

The crawler should also take into account security, though not addressed here. For example malicious websites or viruses exc.

We should also discuss the crawl methodology, in general we can address the web as a graph, and so we dont wanna go deep first but want to go wide first (can be very deep), and therefore we should do all the children of a url before going to the children of children.

## Rules

Rules should allow us to define rules if we should crawl this link or not. This can even have checks for malicious websites or spider traps. Should have access to metrics and/or databases.

# Design

We separate our design to three components,

1. Crawl database (fast response, redis)
1. Data database (Slow response - relational? depends on what we want to do for metrics)
1. Crawlers
1. ReCrawl service (expired crawl service)

## Crawl algorithm (Crawler)

1. Get a crawl url from the queue.
1. Check the throttling for that url (redis token bucket), if we cannot crawl
   - add to Data database with expiration in now + dt (depending on the throttling), the recrawler will readd it to queue.
   - ack.
1. Check the rules for crawling, if not. ack. goto 1.
1. Get the data from the url. And handle errors, check security, viruses, etc. Render the data (whatever method)
1. Check the rules for crawling, if not. ack. goto 1.
1. Check for changes in the Data database, use the hash method, check if data has changed or seen. If not, ack, and goto 1.
1. If html, gather urls from data. For each url to be crawled gathered,
   1. Check if already in queue. Skip if it is.
   1. If not, add.
   1. Note that we are ignoring the database expires since if parent has changed, child may have changed and we need to look.
1. Process metrics
1. Write hash, crawled metrics and last crawled to the Data database.
1. Send ack - url was crawled, and delete the crawl from the queue.

**NOTE** we can check the last-modified header also, this would allow us to use the websites own definition of modifications instead of the hash, and avoid downloading all the url data.

## Crawl Database

1. Holds crawl queue and crawl set (what are we crawling right now)
1. Holds the crawl url lock.
1. Holds the throttling token buckets.
1. If a crawl was ack, then we delete it.

We need the crawl database to be relatively fast, so it will not hold back the crawls. Also it must implement a persistent queue for the active crawls that would not be destroyed if the database node has failed. In this case we can use something like Redis, which is a distributed ring hash table. This should allow us some safety that the crawl process will not stop. Redis should also have a pattern for lock with ack.

## Data database

1. Holds metrics about urls
1. Holds any other data crawled.
1. Holds the expiration time for the crawl.
1. Holds the hashes of the data, and therefore the content seen.

Our database is deployed across multiple zones and would require us to save lots of data. Since we are storing all the metrics and data. For the whole web this would be Petabytes of data for a key value store. Something like Cassandra would work well and be fault tolerant.

## ReCrawl service

1. Running in background
1. Periodically checks,
   - If we reached max size of number of simultaneous crawls, ignore this step.
   - For N crawled urls that have expired,
     - if in crawl queue skip
     - check the crawl throttle bucket - can we crawl.
     - add to crawl queue.
   - Mark these N pending re-crawl (add a time delta to the expiry from now)

This is a background service, that would run on multiple servers. They do not need to synchronize since even if we cannot add a new crawl to the queue if its already there.

## Seeding

It would be best to seed this system by writing the crawl to the Data database, so its persistent, with the timeout expired. This would mean the we will first add the seed urls to the main database and the crawles would be added to the queue by the recrawl service.

## Issues with this design

1. The recrawl service may access the same urls more than once
1. The database is slow, so crawlers may spend a lot of time on a crawl.
1. Since we dont know the metrics, its hard to estimate the database size. But since its separated from the crawl service even if its down the data is preserved.

## Performance, Scalability and availability

We in general do not need this system to be scalable or available. We can stop the crawler and continue it.

Note that each service is separated and the crawlers have no state (they are all the same), the state is maintained by the main queue for the crawl, and a crawler can consume crawls the urls at its leisure.

We note the check of the data hash, in this case, we may want to make sure the hash values

That means that,

1. We can do a DHS on the crawlers, depending on how much power we want to give it.
1. The database for the crawl queue would can be smaller, since we should have number of queued crawls that is relative to the number of crawlers (say 100 links per url -> 100\*crawlers), and therefore we should not have much data there.
1. The database for data can be slow, its accessed on the end of the crawl for metrics, and is not used for sync and queue. We use an eventual concurrency model for the database.

## Fault tolerance

We require fault tolerance only on the Data database, even if the other systems fail, the re-crawl service would restart the crawling from where we stopped off.

## Monitoring

We want to monitor,

1. Queue size vs number of crawlers, and increase or decrease the size of the crawler set if this is unbalanced.
1. Database size, we may need to increase the size of the database if we reached the data.
1. The recrawl service, and the number of expired crawls.
1. The longest expired crawl to match our latency, if we see that this is still not being crawled then we would need to add more crawlers -> so we are processing expirations faster.

# Further improvements

1. We can in general keep the crawler status in a hash set in the crawlers, using a ring. Not sure if this is an improvement
1. We can assign specific crawlers to specific url sets for different data, thus allowing faster ingestion of specific websites or types of data.
1. Throttler - a crawler should not make to many requests for a website within a specific set of time. Otherwise it may be blocked.
1. Content storage different then meta storage - we may want to hash the content as not to has duplicates of the same data in the database. For html for example we can do this for the head/body sections separately.
1. We can add prioritization to the crawl, that is which pages are more or less important. In this case, the crawl queue may change.
1. We can also use the website update frequency (after multiple crawls?), with a default value to avoid checking websites that have not been changed in a while.
1. Should take into account Robots.txt
1. Use a job executor (say using kubernetes) to auto scale.
1. Add method to avoid spider traps (security) (say inner link with change parameters or change end url with increasing number).. etc.
1. Dynamic rendering (js. etc.)