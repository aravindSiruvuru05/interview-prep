# Go Channels Explained — Buffered vs Unbuffered

A walkthrough using examples from this repo (`primenumbers.go`, `oddeven.go`, `worker_pool_semaphore.go`).

---

## The one-line difference

| | Syntax | What it means |
|---|--------|---------------|
| **Unbuffered** | `make(chan int)` | Send and receive must happen **at the same time** (handshake) |
| **Buffered** | `make(chan int, 10)` | Up to 10 values can sit in a queue **without** a receiver |

---

## Part 1 — Unbuffered channel (your `findPrimesUnbuffered`)

Your code uses:

```go
tasks := make(chan int)
```

This is an **unbuffered channel** (capacity = 0).

### What happens?

```go
go func() {
    for i := start; i < end; i++ {
        tasks <- i
    }
    close(tasks)
}()
```

Suppose there are 4 workers.

Initially:

```text
Producer

tasks <- 1

Workers
W1 waiting
W2 waiting
W3 waiting
W4 waiting
```

When the producer executes:

```go
tasks <- 1
```

it **blocks** until some worker receives it.

For example:

```go
Worker1:
t := <-tasks
```

Now:

```text
Producer sends 1
        │
        ▼
     Worker1 receives 1
```

Only after Worker1 receives `1` does the producer continue to:

```go
tasks <- 2
```

Again it blocks until another worker receives it.

So the producer **cannot race ahead** and push all 99 numbers instantly. It synchronizes on every send.

---

### Timeline

```text
Producer            Worker1

tasks <- 1   -----> receive 1
(tasks send completes)

tasks <- 2   -----> receive 2
(tasks send completes)

tasks <- 3   -----> receive 3
```

Each send waits for a receiver. This is a **synchronization point**.

---

### What if workers are busy?

Suppose all 4 workers are computing primes:

```text
Worker1 -> busy
Worker2 -> busy
Worker3 -> busy
Worker4 -> busy
```

Now the producer reaches:

```go
tasks <- 10
```

There is **no worker waiting** on receive.

So the producer stops here:

```text
Producer
tasks <- 10

BLOCKED
```

It waits until one worker finishes and executes:

```go
t := <-tasks
```

Then:

```text
Worker2 finished
takes 10
Producer continues to 11
```

This is called **backpressure** — the producer automatically slows down to match the consumers. A fast producer cannot overwhelm slow workers.

---

### The `result` channel is unbuffered too

```go
result := make(chan int)
```

When a worker finds a prime:

```go
result <- t
```

the worker **blocks** until main receives:

```go
for r := range result {
    primes = append(primes, r)
}
```

So you have backpressure on **both** sides:

```text
Producer  --tasks-->  Workers  --result-->  Main collector
(unbuffered)          (unbuffered)
```

---

## Part 2 — Buffered channel (your `findPrimesBuffered`)

Suppose instead:

```go
taskCount := end - start
tasks := make(chan int, taskCount)   // buffer holds all 99 tasks
result := make(chan int, taskCount)
```

### What changes for the producer?

The producer can put **all 99 numbers** into `tasks` without waiting for workers:

```go
for i := start; i < end; i++ {
    tasks <- i   // does NOT block until buffer is full
}
close(tasks)
```

```text
tasks buffer (capacity 99)

1, 2, 3, 4, 5, ... 99   ← all queued immediately
```

Workers pull from the buffer at their own pace:

```text
Producer -> [buffer: 1,2,3,...,99] -> Workers
           (fills instantly)         (pull when ready)
```

Only if the buffer were **full** would:

```go
tasks <- 100
```

block until a worker removes one.

---

### What changes for workers → main?

With buffered `result`:

```go
result := make(chan int, taskCount)
```

A worker can send a prime **without** main receiving immediately — up to `taskCount` primes can sit in the buffer.

This avoids a common deadlock: workers blocked on `result <-` while main is still starting up.

See `concurrency/channels_deadlocks.go` — it buffers both channels for exactly this reason.

---

## Side-by-side summary

### Unbuffered (`make(chan int)`)

```text
Producer ---- waits ----> Worker
```

- Every `tasks <- i` waits for a worker to receive it
- The producer cannot get ahead
- Natural **flow control** / backpressure

### Buffered (`make(chan int, 99)`)

```text
Producer -> Buffer -> Workers
```

- Producer can queue up to 99 tasks immediately
- Only blocks when buffer is full
- Decouples producer speed from consumer speed

---

## Part 3 — Real example: odd/even ping-pong (`oddeven.go`)

```go
oddChan := make(chan bool)   // unbuffered
evenChan := make(chan bool)  // unbuffered
```

Odd goroutine:

```go
<-oddChan          // wait for signal
fmt.Print(i, " ")
evenChan <- true   // wake even goroutine
```

Even goroutine:

```go
<-evenChan         // wait for signal
fmt.Print(i, " ")
oddChan <- true    // wake odd goroutine
```

Why unbuffered? Because you **want** strict alternation — each print must wait for the other side. A buffered channel would let signals pile up and break the pattern.

```text
Odd:  wait ──receive── print 1 ──send──>
Even:       wait ──receive── print 2 ──send──>
Odd:              wait ──receive── print 3 ...
```

**No `close()` needed here** — see [Part 5](#part-5--close-range-and-when-you-must-close) for why.

---

## Part 4 — Buffered channel as semaphore (`worker_pool_semaphore.go`)

```go
sem := make(chan struct{}, 4)  // 4 empty slots
```

**Acquire** (take a slot):

```go
sem <- struct{}{}   // blocks when 4 goroutines already inside
```

**Release** (free a slot):

```go
<-sem
```

```text
Slot 1: [in use]
Slot 2: [in use]
Slot 3: [in use]
Slot 4: [in use]

Goroutine 5 tries sem <- struct{}{}
→ BLOCKED until someone does <-sem
```

The buffer **is** the counting semaphore. Capacity N = max N goroutines in the critical section.

---

## Part 5 — `close`, `range`, and when you MUST close

### The interview question

> **When do we close a channel?**

**Answer:** Close a channel when the receiver **doesn't know how many values to expect** — typically when using `for range ch`. If the receiver already knows exactly how many values it will receive (a counted `for` loop), **closing is optional and often unnecessary**.

---

### `range` vs explicit receive

#### Case 1 — `for range` → **must close**

If you do:

```go
for range oddChan {
    ...
}
```

or

```go
for v := range oddChan {
    ...
}
```

the loop continues **until the channel is closed** (and drained).

So in that case, you **must** call:

```go
close(oddChan)
```

Otherwise the goroutine waits forever.

Example from `primenumbers.go`:

```go
for r := range result {
    primes = append(primes, r)
}
```

Loop exits only when:
1. Channel is **closed**, AND
2. Buffer is **drained**

If you forget `close(result)` after workers finish → **deadlock** (main waits forever).

Correct pattern:

```go
go func() {
    wg.Wait()
    close(result)   // signal: no more primes
}()

for r := range result { ... }
```

---

#### Case 2 — counted loop → **no close needed**

But `oddeven.go` does this instead:

```go
for i := 1; i <= 9; i += 2 {
    <-oddChan
    fmt.Print(i, " ")
    evenChan <- true
}
```

Notice you're **not ranging over the channel**.

Instead, you're saying:

> "Receive exactly 5 times."

The loop itself controls when to stop.

---

### Let's count (`oddeven.go`)

**Odd goroutine:**

```go
for i := 1; i <= 9; i += 2
```

Runs for:

```text
1, 3, 5, 7, 9
```

Exactly **5 iterations** → exactly **5** `<-oddChan` receives.

**Even goroutine:**

```go
for i := 2; i <= 10; i += 2
```

Runs for:

```text
2, 4, 6, 8, 10
```

Exactly **5 iterations** → exactly **5** `<-evenChan` receives.

---

### Timeline

```text
Main
 |
oddChan <- true

Odd receives
prints 1
evenChan <- true

Even receives
prints 2
oddChan <- true

Odd receives
prints 3
evenChan <- true

...

Even receives
prints 10

break
return
```

Both goroutines naturally finish because their `for` loops end. No one is waiting for another message. Therefore **no channel needs to be closed**.

---

### Rule to remember

| Pattern | Close required? | Why |
|---------|-----------------|-----|
| `for v := range ch` | **Yes** | Loop waits for `close(ch)` to know it's done |
| `for i := 0; i < N; i++ { <-ch }` | **No** | Loop count tells receiver when to stop |
| Worker pool + `for range tasks` | **Yes** (on `tasks`) | Workers don't know how many jobs exist |
| Ping-pong / handshake (`oddeven.go`) | **No** | Fixed number of signals, bounded loops |

```go
// Case 1 — MUST close
for range ch { ... }
close(ch)

// Case 2 — no close needed
for i := 0; i < 5; i++ {
    <-ch
}
```

---

### What `close` actually does

```go
close(tasks)
```

- Tells receivers: no more values coming
- Workers exit: `for t := range tasks` stops after draining
- **Never** send on a closed channel → **panic**
- Receiving from closed + empty channel: zero value, `ok == false`

```go
v, ok := <-ch
// ok == false  →  channel closed and empty
```

---

### Side-by-side: `primenumbers.go` vs `oddeven.go`

| | `primenumbers.go` | `oddeven.go` |
|---|-------------------|--------------|
| Receive style | `for r := range result` | `for i := 1; i <= 9; i += 2 { <-oddChan }` |
| Knows count? | No — primes until channel ends | Yes — exactly 5 receives |
| Must `close`? | **Yes** | **No** |
| Who closes? | Goroutine after `wg.Wait()` | Nobody |

---

## Part 6 — `len(ch)` and `cap(ch)`

```go
ch := make(chan int, 10)

len(ch)  // values currently in buffer (e.g. 3)
cap(ch)  // buffer size (10)
```

```go
ch := make(chan int)  // unbuffered
len(ch)  // 0
cap(ch)  // 0
```

Useful for debugging: "is my producer filling the buffer?"

---

## Part 7 — Channel directions (send-only / receive-only)

In `primenumbers.go`:

```go
func worker(tasks <-chan int, result chan<- int, wg *sync.WaitGroup)
//            receive only      send only
```

| Type | Can send? | Can receive? |
|------|-----------|--------------|
| `chan int` | yes | yes |
| `chan<- int` | yes | no |
| `<-chan int` | no | yes |

Compile-time safety — worker cannot accidentally receive from `result` or send to `tasks`.

---

## Part 8 — `select` — multiplex channels

From `select.go`:

```go
select {
case msg := <-ch:
    fmt.Println("work done:", msg)
case <-ctx.Done():
    fmt.Println("timeout:", ctx.Err())
}
```

- Waits until **one** case is ready
- If multiple ready → picks one **at random**
- `default` → non-blocking (don't wait)

Common uses:
- Timeout / cancellation
- Read from multiple channels
- Non-blocking send/receive

---

## Part 9 — Nil channel (gotcha)

```go
var ch chan int   // nil
ch <- 1           // blocks forever
x := <-ch         // blocks forever
```

A nil channel blocks forever on send and receive. Sometimes used intentionally to disable a `select` case.

---

## Part 10 — Deadlock scenarios (interview favorites)

### 1. Forgot to close

```go
for r := range results { ... }  // hangs forever if results never closed
```

### 2. Unbuffered + no receiver

```go
ch := make(chan int)
ch <- 1   // main has no other goroutine receiving → deadlock
```

### 3. All goroutines blocked on channels

```text
G1 waiting on ch1
G2 waiting on ch2
G1 is the only one who can send to ch2
G2 is the only one who can send to ch1
→ circular wait → deadlock
```

### 4. Send on closed channel

```go
close(ch)
ch <- 1   // panic
```

---

## Part 11 — When to use which?

| Scenario | Channel type | Example in repo |
|----------|--------------|-----------------|
| Strict sync / handshake | Unbuffered | `oddeven.go` |
| Backpressure on producer | Unbuffered | `findPrimesUnbuffered` |
| Preload job queue | Buffered | `findPrimesBuffered` |
| Avoid worker→main deadlock | Buffered results | `channels_deadlocks.go` |
| Limit concurrent goroutines | Buffered `struct{}` | `worker_pool_semaphore.go` |
| "Ready" signal between goroutines | Unbuffered | `oddeven.go` |

---

## Part 12 — Interview quick answers

**Q: What is the difference between buffered and unbuffered?**
- Unbuffered: synchronous hand-off; both sides must meet
- Buffered: async queue up to N; send blocks only when full

**Q: Why use unbuffered if buffered seems faster?**
- Flow control, synchronization, backpressure — not always about speed

**Q: Can buffered channel improve throughput?**
- Yes, when producer and consumer run at different speeds and you want to decouple them — but unbounded buffering can hide overload (memory grows)

**Q: What happens if buffer is full and producer keeps sending?**
- Producer blocks (backpressure) until consumer receives

**Q: How do channels provide flow control?**
- Unbuffered: producer waits per item
- Buffered: producer waits when queue is full
- Either way, a slow consumer eventually slows the producer

**Q: When do we close a channel?**
- Close when receiver uses `for range ch` and doesn't know how many values to expect
- No close needed when receiver uses a counted loop (`for i := 0; i < N; i++ { <-ch }`) — see `oddeven.go` vs `primenumbers.go` in [Part 5](#part-5--close-range-and-when-you-must-close)

**Q: Why doesn't `oddeven.go` call `close()`?**
- Both goroutines use bounded `for` loops (5 receives each), not `for range`. Loops end naturally — no one waits for "no more data" signal.

## Runnable code

```bash
# primenumbers.go — both patterns side by side
# Rename maindd → main, then:
go run primenumbers.go
```

Files to read together:
- `primenumbers.go` — unbuffered vs buffered worker pool
- `oddeven.go` — unbuffered sync
- `concurrency/channels_deadlocks.go` — why buffer prevents deadlock
- `worker_pool_semaphore.go` — buffered channel as semaphore
- `select.go` — select + context timeout

---

## The big idea

Go channels are not just queues. They are **synchronization primitives**:

```text
Unbuffered  →  "I will wait for you"
Buffered    →  "I can queue up to N, then I wait for you"
```

That built-in flow control is why channels replace locks + condition variables for so many concurrency patterns in Go.
