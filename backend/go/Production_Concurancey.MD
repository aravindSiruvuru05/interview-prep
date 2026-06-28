This is an excellent question. In production, **you almost never let every component create unlimited workers**. Instead, companies use **bounded concurrency** and **resource management** at multiple levels.

Imagine a service that does:

* Web crawling
* Sending emails
* Image processing
* Database writes
* Calling other microservices

If each of these creates 100 workers independently:

```
Crawler      -> 100 workers
Email        -> 100 workers
Images       -> 100 workers
Payments     -> 100 workers
Search       -> 100 workers

Total = 500 workers
```

Now imagine there are 20 such components. You could easily end up with thousands of goroutines all competing for the same CPU, memory, database connections, and network sockets.

Production systems avoid this in several ways.

---

## 1. Fixed worker pools (most common)

Instead of every request spawning goroutines:

```
Incoming Requests
        |
        v
     Job Queue
        |
  ----------------
  Worker 1
  Worker 2
  Worker 3
  Worker 4
  ----------------
```

Only four workers execute at a time. The queue may contain millions of jobs.

---

## 2. Semaphore (limit concurrent work)

Sometimes you don't even create a worker pool. Instead you allow goroutines but limit how many can execute the expensive part.

```go
sem := make(chan struct{}, 50)

go func() {
    sem <- struct{}{}   // acquire

    callAPI()

    <-sem               // release
}()
```

If 10,000 goroutines arrive, only 50 will call the API simultaneously. The others block waiting for a slot.

This is extremely common in Go.

---

## 3. Connection pools

Suppose you have PostgreSQL.

The database may allow 500 connections.

Your service creates only:

```
DB Pool = 50 connections
```

Even if 100,000 requests come in,

```
100000 requests

      |

50 DB connections
```

The remaining requests wait until a connection becomes free.

Every major database driver does this.

---

## 4. HTTP client connection pools

The same happens with HTTP.

Instead of opening a new TCP connection every time,

```
Service A

Connection Pool

TCP 1
TCP 2
TCP 3
TCP 4
```

Thousands of requests reuse these persistent connections (HTTP Keep-Alive or HTTP/2 multiplexing).

---

## 5. Message queues

Instead of directly processing work:

```
API

↓

Kafka

↓

50 Consumers
```

or

```
RabbitMQ

↓

20 Workers
```

The queue stores millions of pending jobs, while consumers process them at a controlled rate.

---

## 6. Rate limiting

Suppose another service allows only 100 requests/sec.

Even if your application receives

```
1,000,000 requests
```

it intentionally sends only

```
100 requests/sec
```

to that dependency to avoid failures.

---

## 7. Horizontal scaling

Instead of one machine having 1,000 workers,

companies deploy many instances.

```
Load Balancer

      |

-------------------------
|     |      |      |
S1    S2     S3     S4
-------------------------
```

Each service instance might have:

* 20 workers
* 50 DB connections
* 100 HTTP connections

If traffic doubles, Kubernetes or another orchestrator starts more instances instead of increasing the number of workers on a single machine.

---

## Example from a large company

Suppose you're processing 10 million images.

You **would not** start 10 million goroutines.

Instead:

```
10 million images

↓

Kafka

↓

100 Pods

↓

Each Pod

20 Workers

↓

Image Processor
```

That gives:

* 100 Pods
* 20 workers each
* **2,000 images processed concurrently**

The remaining jobs stay safely in Kafka until workers are ready.

---

## How companies decide the worker count

The number isn't arbitrary. It's based on what the work is doing:

* **CPU-bound work** (compression, image resizing, encryption): usually around the number of CPU cores (or a small multiple). More workers than cores often just increase context switching.
* **I/O-bound work** (network calls, database queries, disk I/O): workers spend much of their time waiting, so you can often have many more workers than CPU cores. The optimal number depends on latency, throughput, memory, and limits of downstream systems.

Teams monitor CPU usage, memory, latency, queue length, and error rates, then tune these values over time.

---

### The key production principle

Every expensive resource has a limit:

* CPU → worker pools or goroutine limits
* Database → connection pool
* HTTP → connection pool
* External APIs → rate limiter or semaphore
* Background jobs → Kafka/RabbitMQ/SQS queues
* Entire service → horizontal scaling behind a load balancer

The overarching idea is simple: **never let concurrency grow without bounds**. Instead, queue work and process it at a rate your system and its dependencies can sustain.
