# Go Interview Prep — Quick Refresher

Your personal Go sandbox from ~1 year ago. Root-level files are **standalone snippets** (each has its own `main*` function so they don't clash). Subfolders are **small runnable modules** with their own `go.mod`.

### Learning path (read in this order)

| Step | Section | What you learn |
|------|---------|----------------|
| 1 | [Part 1 §1–4](#1-variables--types) | Variables, functions, structs, **pointers** |
| 2 | [Part 1 §5–7](#5-methods--receivers) | Methods, interfaces, slices, maps |
| 3 | [Part 1 §8–12](#8-control-flow) | Control flow, errors, packages, JSON, generics |
| 4 | [Part 1 §13](#13-concurrency-primitives-bridge-to-part-2) | Goroutine/channel preview (then Part 2) |
| 5 | [Part 2](#part-2--your-repo-deep-dives-advanced) | Worker pools, HTTP, reflection — your actual code |
| 6 | [Top 28 Q&A](#top-28-interview-questions-with-short-answers) | Rapid-fire interview answers |

---

## Folder Map

```
backend/go/
├── README.md                    ← you are here
│
│  ── Concurrency & Channels ──
├── workers.go                   Worker pool (interface{} + channels)
├── generic_worker.go            Same pool with Go generics [T, R]
├── worker_pool_semaphore.go     Worker pool + semaphore (3 patterns, generics)
├── primenumbers.go              Fan-out workers finding primes (unbuffered + buffered)
├── channels_explained.md        Buffered vs unbuffered walkthrough (read with primenumbers.go)
├── oddeven.go                   Two goroutines alternating via channels
├── select.go                    select + context.WithTimeout
├── optimistic_locaking.go       Optimistic locking with version field
│
│  ── HTTP & Middleware ──
├── muxservehttp.go              http.ServeMux routing
├── mux_middleware_ratelimiter.go  Sliding-window rate limiter middleware
├── panic.go                     panic/recover middleware
│
│  ── Reflection & Serialization ──
├── reflect.go                   Struct validation + custom marshal/unmarshal
├── reflect_typeassertion.go     Type switch on interface{} channel
├── marshallunmarshall.go        encoding/json tags
│
│  ── Misc ──
├── test.go                      Rate limiter + concurrent goroutines
│
│  ── Submodules (each has go.mod) ──
├── concurrency/                 Channel deadlock demo + comments
├── design_pattrens/             Decorator pattern (coffee toppings)
├── rate_limitter/               Sliding-window limiter + unit tests
├── go_hexagonal/                Hexagonal architecture (ports & adapters)
└── go_todo_app/                 Stub for a maintainable todo API
```

### How to run

```bash
# Root snippets — rename the main you want to `main`, or run a subfolder:
cd backend/go/go_hexagonal && go run .
cd backend/go/rate_limitter && go test -v
cd backend/go/concurrency && go run .
```

> **Note:** Root files share `package main`. Only one `func main()` can exist per directory. Each file uses a renamed entry point (`main12`, `main234`, `maisn`, etc.) — rename the one you want before `go run`.

---

## Go Cheat Sheet (30-Second Recall)

| Concept | Syntax / Rule |
|---------|---------------|
| Variable | `x := 10` (short declare) or `var x int = 10` |
| Pointer | `p := &x` · dereference `*p` |
| Struct | `type User struct { Name string }` |
| Method | `func (u *User) Greet() string` — pointer receiver mutates |
| Interface | `type Reader interface { Read([]byte) (int, error) }` — **implicit** satisfaction |
| Error | `return nil, fmt.Errorf("not found: %d", id)` — errors are values, not exceptions |
| Goroutine | `go doWork()` — lightweight thread, scheduled by Go runtime |
| Channel | `ch := make(chan int)` unbuffered · `make(chan int, 10)` buffered |
| Send/recv | `ch <- v` · `v := <-ch` · `close(ch)` |
| Select | `select { case v := <-ch: ... case <-ctx.Done(): ... }` |
| Defer | `defer f()` runs when function returns (LIFO stack) |
| Range on channel | `for v := range ch` exits when channel is **closed** |
| Zero value | `0`, `""`, `nil`, `false` for unset fields |
| JSON | struct tags: `` `json:"name"` `` · unmarshal needs **pointer** `&user` |
| Mutex | `mu.Lock(); defer mu.Unlock()` |
| WaitGroup | `wg.Add(1)` before goroutine · `defer wg.Done()` inside · `wg.Wait()` after |
| Semaphore | `sem := make(chan struct{}, N)` · acquire `sem<-struct{}{}` · release `<-sem` |
| Context | `ctx, cancel := context.WithTimeout(parent, 5*time.Second); defer cancel()` |
| Generics (1.18+) | `func Map[T, R any](...) R` · `WorkerPoolG[T, R]` in your code |

---

## Part 1 — Go Language Fundamentals (Basic → Advanced)

Read this top-to-bottom before concurrency. Every advanced topic in your repo builds on these.

---

### 1. Variables & Types

**Definition:** A variable stores a value of a specific type. Go is **statically typed** — the compiler knows the type at compile time.

```go
// Long declaration
var name string = "Alice"
var age int

// Short declaration (only inside functions)
city := "NYC"          // type inferred as string
count := 42            // int

// Multiple
var x, y int = 1, 2
a, b := 1, "hello"

// Zero values (default when not set)
var i int       // 0
var s string     // ""
var ok bool      // false
var p *int       // nil
```

**Basic types:**

| Category | Types | Zero value |
|----------|-------|------------|
| Integer | `int`, `int8`, `int16`, `int32`, `int64`, `uint`, `byte` (=uint8), `rune` (=int32) | `0` |
| Float | `float32`, `float64` | `0.0` |
| Bool | `bool` | `false` |
| String | `string` (immutable UTF-8 bytes) | `""` |
| Complex | `complex64`, `complex128` | — |

**Constants:**
```go
const Pi = 3.14
const (
    StatusOK = 200
    StatusNotFound = 404
)
const MaxUsers = 100  // untyped — usable with int, float64, etc.
```

**Type conversion (no implicit casting):**
```go
var x int = 10
var y float64 = float64(x)   // must be explicit
// var z float64 = x          // COMPILE ERROR
```

**Interview Q: `:=` vs `var`?**
- `:=` declares + assigns, only inside functions, type inferred
- `var` works at package level; can declare without assignment (`var x int`)

**Interview Q: What is a zero value?**
- Default value every type gets when declared without initialization. `nil` for pointers, slices, maps, channels, interfaces, functions.

---

### 2. Functions

**Definition:** A named block of code. Functions are first-class values (can be passed around).

```go
// Basic
func add(a int, b int) int {
    return a + b
}

// Shorthand same types
func add(a, b int) int { return a + b }

// Multiple return values (idiomatic for errors)
func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, fmt.Errorf("division by zero")
    }
    return a / b, nil
}

// Named return values
func split(sum int) (x, y int) {
    x = sum * 4 / 9
    y = sum - x
    return   // naked return — returns x, y
}
```

**Functions as values (used everywhere in your worker pools):**
```go
workerFunc := func(task int) int {
    return task * task
}
pool.Start(workerFunc)
```

**Variadic:**
```go
func sum(nums ...int) int {
    total := 0
    for _, n := range nums {
        total += n
    }
    return total
}
sum(1, 2, 3)
```

**defer — runs when function exits (LIFO stack):**

`defer` schedules a function call to run **when the surrounding function exits** — not immediately.

```go
func readFile() {
    f, _ := os.Open("file.txt")
    defer f.Close()   // registered now, runs on the way out

    // ... use f ...
}   // ← f.Close() runs HERE
```

Used in your code: `defer wg.Done()`, `defer mu.Unlock()`, `defer cancel()`.

**Multiple defers run in reverse order (LIFO):**
```go
defer fmt.Println("1")
defer fmt.Println("2")
// prints: 2, then 1
```

**Interview Q: When does `defer` run?**

When the surrounding function is **leaving** — on any exit path:

1. Return value is computed
2. **All `defer`s run** (last registered → first)
3. Function returns to caller

```go
func example() (n int) {
    defer fmt.Println("deferred")
    return 42   // defer still runs before caller gets 42
}
```

**Interview Q: What is a defer cost?**

Each `defer` has a small runtime cost:

- **Memory** — deferred calls are stored on an internal stack until the function returns
- **CPU** — on exit, Go walks that stack and runs each deferred call

A few `defer`s per function is negligible. Don't avoid `defer` for micro-optimization — it prevents bugs (forgetting `Unlock`/`Close` on one code path). Calling cleanup manually before every `return` is slightly faster but error-prone.

**Interview Q: Does defer run on panic?**

**Yes.** If the function panics, defers still run while the stack unwinds:

```go
func risky() {
    defer fmt.Println("cleanup runs")
    panic("oops")
}
// Output: "cleanup runs", then panic propagates upward
```

**"Even with panic if recover'd"** means: if an **outer** function catches the panic via `recover()` inside a `defer`, inner defers already ran during the unwind:

```go
func outer() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("caught:", r)
        }
    }()
    inner()
}

func inner() {
    defer fmt.Println("inner cleanup")  // runs BEFORE recover catches panic
    panic("boom")
}
// Output:
// inner cleanup
// caught: boom
```

This is exactly the pattern in `panic.go` — `defer` + `recover()` so one handler panic doesn't kill the whole server.

**One-liner:** `defer` = "run this when I leave this function" — small cost, big safety; runs on normal return **and** during panic unwind.

---

### 3. Structs

**Definition:** A struct groups related fields into one type. Go has **no classes** — structs + methods replace OOP.

```go
type User struct {
    ID   int
    Name string
    Age  int
}

// Literal
u := User{ID: 1, Name: "Alice", Age: 30}
u2 := User{1, "Bob", 25}   // positional — fragile, avoid in prod

// Access
fmt.Println(u.Name)
u.Age = 31
```

**Struct tags** (metadata for JSON, validation — see `reflect.go`, `go_hexagonal/user_port.go`):
```go
type User struct {
    ID   int    `json:"id"`
    Name string `json:"name" validate:"required"`
}
```

**Anonymous / embedded structs:**
```go
type Person struct {
    Name string
}
type Employee struct {
    Person          // embedded — promotes Person fields
    EmployeeID int
}
e := Employee{Person: Person{Name: "Alice"}, EmployeeID: 1}
fmt.Println(e.Name)  // promoted field
```

**Your repo examples:**
- `User` in `go_hexagonal/user_port.go`
- `Worker`, `WorkerPoolG` in `workers.go`, `generic_worker.go`
- `Record` with `Version` in `optimistic_locaking.go`

**Interview Q: Struct vs map for data?**
- Struct: fixed fields, compile-time safety, better performance
- Map: dynamic keys, flexible schema, no field names at compile time

---

### 4. Pointers

**Definition:** A pointer holds the **memory address** of a value. Go has pointers but **no pointer arithmetic** (unlike C).

```go
x := 10
p := &x      // p is *int — address of x
fmt.Println(*p)  // 10 — dereference

*p = 20
fmt.Println(x)   // 20 — x changed through pointer
```

**Why pointers matter:**
1. **Mutate** a value inside a function (pass by reference semantics)
2. **Avoid copying** large structs
3. **Share** state (DB, cache, mutex) across functions
4. **Nil checks** for optional/missing data

```go
func reset(u User) {
    u.Name = ""   // copies struct — original unchanged
}

func resetPtr(u *User) {
    u.Name = ""   // mutates original
}

user := User{Name: "Alice"}
reset(user)        // user.Name still "Alice"
resetPtr(&user)    // user.Name now ""
```

**`new` vs `&`:**
```go
p1 := new(int)     // *int, zero value 0
*p1 = 42

x := 0
p2 := &x           // preferred — more readable
```

**Nil pointer:**
```go
var p *User = nil
// p.Name  → PANIC: nil pointer dereference
if p != nil {
    fmt.Println(p.Name)
}
```

**Interview Q: Does Go have references like C++?**
- **No.** Only pointers. When you pass a slice, map, or channel, you pass a **header** (descriptor) that points to underlying data — it looks like reference behavior but it's not C++ references.

**Interview Q: When to use pointer vs value?**
| Use pointer `*T` | Use value `T` |
|------------------|---------------|
| Need to mutate | Small, immutable data |
| Large struct (avoid copy) | Simple value types (`int`, `bool`) |
| Method mutates receiver | Receiver is tiny struct |
| `nil` means "absent" | — |

---

### 5. Methods & Receivers

**Definition:** A method is a function with a **receiver** — binds a function to a type.

```go
type Rectangle struct {
    Width, Height float64
}

// Value receiver — gets a COPY
func (r Rectangle) Area() float64 {
    return r.Width * r.Height
}

// Pointer receiver — can MUTATE original
func (r *Rectangle) Scale(factor float64) {
    r.Width *= factor
    r.Height *= factor
}
```

```go
rect := Rectangle{10, 5}
rect.Scale(2)    // Go auto-converts: (&rect).Scale(2)
```

**Rule of thumb:** If any method on a type uses pointer receiver, **use pointer receiver for all methods** on that type (consistency).

**Your repo examples:**
```go
func (w *Worker) Start(do func(task interface{}) interface{}) { ... }
func (r *RateLimiter) Allow() bool { ... }
func (p *Person) changeName() { p.name = "asdf" }  // go_todo_app/main.go
func (m *Mocha) getPrice() int { return m.price + m.b.getPrice() }
```

**Interview Q: Value vs pointer receiver?**
- **Value:** read-only, small types, no mutation needed
- **Pointer:** mutates state, large struct, or struct contains `sync.Mutex` (mutex must not be copied — always `*T` receiver)

---

### 6. Interfaces

**Definition:** An interface is a **set of method signatures**. A type satisfies an interface **implicitly** — no `implements` keyword.

```go
type Beverage interface {
    getPrice() int
}

type Coffee struct { price int }
func (c *Coffee) getPrice() int { return c.price }

// Coffee satisfies Beverage automatically
var b Beverage = NewCoffee()
```

**Empty interface — holds anything:**
```go
var x interface{} = 42
var y any = "hello"   // `any` is alias for interface{} (Go 1.18+)
```
Used in `workers.go` for generic task queue before you wrote `generic_worker.go`.

**Type assertion — extract concrete type:**
```go
var i interface{} = 42
v, ok := i.(int)   // v=42, ok=true
if ok {
    fmt.Println(v)
}

// Type switch (reflect_typeassertion.go)
switch v := msg.(type) {
case User:
    fmt.Println(v.Name)
case Product:
    fmt.Println(v.ID)
default:
    fmt.Println("unknown")
}
```

**Nil interface trap (common interview question):**
```go
var p *User = nil
var i interface{} = p
fmt.Println(i == nil)  // false!
// interface holds (type=*User, value=nil) — not "empty"
```

**Your repo:**
- `Beverage` interface → `design_pattrens/decorator.go`
- `IUserRepository` port → `go_hexagonal/user_port.go`
- `http.Handler` interface → middleware wraps `ServeHTTP`

**Interview Q: What is interface{} used for?**
- Generic containers before Go 1.18 generics, JSON decoding to `map[string]interface{}`, reflection. Prefer concrete types or generics when possible.

---

### 7. Arrays, Slices & Maps

#### Arrays (fixed size — rarely used directly)
```go
var a [3]int = [3]int{1, 2, 3}
a[0] = 10
// len(a) is always 3
```

#### Slices (dynamic view — used everywhere)
**Definition:** A slice is a **descriptor** (pointer + len + cap) over an underlying array.

```go
s := []int{1, 2, 3}           // literal
s = make([]int, 5)              // len=5, cap=5, all zeros
s = make([]int, 0, 10)          // len=0, cap=10 (pre-allocate)

s = append(s, 4)                // may reallocate underlying array
s = append(s, 5, 6, 7)

sub := s[1:4]   // [2,3,4] — shares underlying array with s
```

**Slice gotchas:**
```go
a := []int{1, 2, 3}
b := a          // b shares same backing array as a
b[0] = 99       // a[0] is also 99

// Copy to detach
c := make([]int, len(a))
copy(c, a)
```

**Range:**
```go
for i, v := range slice {
    fmt.Println(i, v)
}
for i := range slice { }       // index only
for _, v := range slice { }    // value only

// Go 1.22+: loop variable per iteration (safe for goroutines)
for i := range 10 {
    go func() { fmt.Println(i) }()
}
```

#### Maps (hash table)
```go
m := make(map[string]int)
m["alice"] = 30
m["bob"] = 25

age, ok := m["alice"]   // ok=true if key exists
delete(m, "bob")

// iterate — order is RANDOMIZED
for k, v := range m {
    fmt.Println(k, v)
}
```

**Your repo:** `db map[int]*Record` in `optimistic_locaking.go`, `CacheLayer.Users map[int]*User`, `limiters map[string]*MRateLimiter`.

**Interview Q: Is map safe for concurrent use?**
- **No.** Concurrent read + write panics. Use `sync.Mutex` or `sync.Map`.

**Interview Q: Slice vs array?**
- Array: `[N]T`, fixed size, passed by value (copied)
- Slice: `[]T`, dynamic, passed by header (shared backing array)

---

### 8. Control Flow

```go
// if — can include short statement
if err := doSomething(); err != nil {
    return err
}

// switch
switch day {
case "Mon", "Tue":
    fmt.Println("weekday")
case "Sat", "Sun":
    fmt.Println("weekend")
default:
    fmt.Println("other")
}

// switch without condition (like if-else chain)
switch {
case x < 0:
    fmt.Println("negative")
case x == 0:
    fmt.Println("zero")
default:
    fmt.Println("positive")
}

// for — Go's only loop
for i := 0; i < 10; i++ { }
for condition { }          // while-style
for { }                     // infinite
for i, v := range items { }
```

---

### 9. Error Handling

**Definition:** Errors are **values**, not exceptions. Functions return `error` as last return value.

```go
user, err := repo.GetByID(1)
if err != nil {
    return nil, fmt.Errorf("get user: %w", err)  // wrap with %w
}

// Create errors
errors.New("not found")
fmt.Errorf("user %d not found", id)
```

**Check wrapped errors (Go 1.13+):**
```go
if errors.Is(err, sql.ErrNoRows) { ... }
var pathErr *os.PathError
if errors.As(err, &pathErr) { ... }
```

**panic / recover** (not for normal flow — see `panic.go`):
```go
panic("something broke")   // unwinds stack, crashes unless recovered

defer func() {
    if r := recover(); r != nil {
        log.Printf("recovered: %v", r)
    }
}()
```

**Interview Q: errors vs panic?**
- **error:** expected failures (not found, invalid input, network timeout)
- **panic:** programmer bugs, unrecoverable state; recover only at boundaries (HTTP middleware)

---

### 10. Packages & Modules

```go
package main   // executable — must have func main()
package users  // library — imported by others
```

```go
import (
    "fmt"
    "net/http"

    "github.com/you/project/internal/users"  // your module path
)
```

**Exported vs unexported:**
- **Capitalized** = exported (public): `User`, `NewWorker`
- **lowercase** = unexported (package-private): `accumulateResults`

**go.mod:**
```go
module github.com/you/interview-prep/go_hexagonal
go 1.22
```

```bash
go mod init example.com/myapp
go mod tidy      # add missing, remove unused deps
go get pkg@version
```

---

### 11. JSON & Struct Tags

```go
type User struct {
    Name  string `json:"name"`
    Email string `json:"email,omitempty"`  // omit if empty
    age   int    `json:"age"`              // lowercase = NOT exported, ignored by json
}

data, err := json.Marshal(user)
err = json.Unmarshal(data, &user)   // MUST pass pointer
```

See `marshallunmarshall.go`, `go_hexagonal/user_handler.go`.

---

### 12. Generics (Go 1.18+)

```go
type WorkerPoolG[T any, R any] struct {
    Tasks chan T
    Results []R
}

func NewWorkerPool[T any, R any](n int) *WorkerPoolG[T, R] { ... }

pool := NewWorkerPool[int, int](5)
```

**Constraints:**
```go
func Min[T constraints.Ordered](a, b T) T {
    if a < b { return a }
    return b
}
```

See `generic_worker.go`.

---

### 13. Concurrency Primitives (bridge to Part 2)

Only after you understand structs, pointers, methods, and interfaces:

| Concept | One-liner |
|---------|-----------|
| **Goroutine** | `go f()` — concurrent function, scheduled by runtime |
| **Channel** | `make(chan T)` unbuffered (sync hand-off) · `make(chan T, N)` buffered (queue/semaphore) |
| **select** | Wait on multiple channel operations |
| **sync.Mutex** | Lock shared data (`mu.Lock(); defer mu.Unlock()`) |
| **sync.WaitGroup** | `Add(1)` → `go func(){ defer Done(); ... }()` → `Wait()` |
| **Semaphore** | Limit how many goroutines run at once (buffered channel or `x/sync/semaphore`) |
| **context** | Cancellation + deadlines across goroutines |

→ Full patterns with your code in **Part 2** below.

---

## Part 2 — Your Repo Deep Dives (Advanced)

### 1. Goroutines & Worker Pools

**What:** Run many tasks concurrently with a fixed number of workers.

**Your code:** `workers.go`, `generic_worker.go`, `primenumbers.go`

```
Producer → tasks chan → [Worker 1..N] → result chan → collector
```

Key patterns:
- `sync.WaitGroup` — wait for N goroutines to finish
- Separate `TaskWg` — wait until all submitted tasks are processed
- **Close order matters:** wait for tasks → close `tasks` → workers exit → close `results`

**Generic version** (`generic_worker.go`):
```go
type WorkerPoolG[T any, R any] struct { ... }
pool := NewWorkerPool[int, int](5)
```
No more `task.(int)` type assertions — compile-time safety.

**Interview Q: Goroutine vs OS thread?**
- Goroutines are multiplexed onto fewer OS threads (M:N scheduling)
- Start cost ~2 KB stack (grows dynamically) vs MB for threads
- Communicate via channels, not shared memory (Go proverb: *"Don't communicate by sharing memory; share memory by communicating"*)

**Interview Q: What happens if you send on a closed channel?**
- **Panic.** Receiving from closed channel returns zero value + `ok == false`.

**Interview Q: Buffered vs unbuffered channel?**
- Unbuffered: send blocks until recv (synchronization point)
- Buffered: send blocks only when buffer is full
- Buffered channel with capacity N is also used as a **semaphore** — see [§4 Semaphores](#4-semaphores)
- Full explanation with repo examples → [channels_explained.md](channels_explained.md) · [§2 Buffered vs unbuffered](#buffered-vs-unbuffered-channels)

---

### 2. Channels, Deadlocks & `select`

**Your code:** `concurrency/channels_deadlocks.go`, `oddeven.go`, `select.go`, `primenumbers.go`, `worker_pool_semaphore.go`

#### Buffered vs unbuffered channels

**Definition:** A channel moves values between goroutines. The second argument to `make` sets the **buffer size**.

```go
ch := make(chan int)      // unbuffered — capacity 0
ch := make(chan int, 10)  // buffered  — holds up to 10 values without a receiver
```

| | Unbuffered (`make(chan T)`) | Buffered (`make(chan T, N)`) |
|---|---------------------------|------------------------------|
| **Capacity** | 0 | N slots |
| **Send blocks until…** | Another goroutine receives | Buffer is full (N values waiting) |
| **Receive blocks until…** | Another goroutine sends | Buffer is empty |
| **Sync behavior** | Hand-off — sender and receiver meet at the same time | Sender can fire-and-forget up to N times |
| **Use when** | You need strict synchronization ("ready" signal) | Decouple producer/consumer speed, or implement semaphore |

**Unbuffered = synchronization point (handshake):**

```
Goroutine A:  ch <- 42  ──────blocks──────►  until B receives
Goroutine B:  x := <-ch  ◄────meets here────  value delivered, both continue
```

`oddeven.go` uses unbuffered `chan bool` — odd goroutine **waits** until even goroutine receives before printing the next number. That's intentional ping-pong sync.

**Buffered = queue with N slots:**

```
Producer:  ch <- 1   ch <- 2   ch <- 3   (no receiver yet — sits in buffer)
                              buffer [1,2,3]
Consumer:  x := <-ch  (takes 1, buffer now [2,3])
```

`concurrency/channels_deadlocks.go` uses buffered channels on purpose:

```go
tasks := make(chan int, len(arr))    // preload all tasks, then close
results := make(chan int, len(arr))  // workers can send without blocking main
```

Without buffering, workers could block sending to `results` while main is still setting up — classic deadlock risk.

**Your repo at a glance:**

| File | Channel | Why |
|------|---------|-----|
| `oddeven.go` | `make(chan bool)` unbuffered | Force alternation — must sync each step |
| `primenumbers.go` | `make(chan int)` unbuffered | Tasks/results sync worker ↔ main |
| `channels_deadlocks.go` | `make(chan int, len(arr))` buffered | Preload tasks; workers won't block on full results |
| `worker_pool_semaphore.go` | `make(chan struct{}, N)` buffered | Semaphore — N acquires without blocking |
| `workers.go` | `make(chan interface{})` unbuffered | Back-pressure: producer waits if workers are slow |

**Interview Q: Buffered vs unbuffered?**
- **Unbuffered:** synchronous hand-off; send and receive must happen together
- **Buffered:** asynchronous up to N; send only blocks when buffer is full

**Interview Q: `len(ch)` vs `cap(ch)`?**
- `len(ch)` — values currently sitting in the buffer
- `cap(ch)` — total buffer size (0 for unbuffered)

**Interview Q: Can you close a buffered channel with values still in it?**
- **Yes.** Receivers drain remaining values; then `ok == false` on further receives.

**Interview Q: Which should I use?**
- Need **coordination** (signals, handshakes, "job done") → unbuffered
- Need **throughput** or **decoupling** (job queue, semaphore) → buffered

**Deadlock rule from your comments:**
```go
go func() {
    wg.Wait()
    close(results)  // MUST close or `for r := range results` hangs forever
}()
for r := range results { ... }
```

**Odd/even alternation** (`oddeven.go`): Two goroutines ping-pong on `oddChan` / `evenChan` — classic concurrency coordination interview question.

**Select + Context** (`select.go`):
```go
ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
defer cancel()

select {
case msg := <-ch:
    // work finished in time
case <-ctx.Done():
    // timeout or cancellation — ctx.Err() is context.DeadlineExceeded
}
```

**Interview Q: When do deadlocks happen in Go?**
1. All goroutines blocked on channel ops with no sender/receiver
2. Forgot to `close` channel used in `range`
3. Circular wait on unbuffered channels
4. Mutex held forever (no unlock)

**Interview Q: What is `select`?**
- Like `switch` but for channel operations
- If multiple cases ready, one is chosen **at random**
- `default` makes it non-blocking

---

### 3. sync Package

| Type | Use |
|------|-----|
| `sync.Mutex` | Exclusive lock — `rate_limitter/`, `mux_middleware_ratelimiter.go` |
| `sync.RWMutex` | Many readers OR one writer (not in repo, but common interview topic) |
| `sync.WaitGroup` | Wait for goroutine batch to complete |
| `sync.Once` | Run init exactly once (not in repo) |
| `sync.Map` | Concurrent map (not in repo; prefer regular map + mutex for most cases) |

**Interview Q: Is `map` safe for concurrent access?**
- **No.** Concurrent read + write on a plain `map` causes a runtime panic. Use `sync.Mutex` or `sync.Map`.

---

### 4. Semaphores

**Definition:** A semaphore limits how many goroutines can access a resource **at the same time**. Think of it as "only N slots available."

| Type | Meaning |
|------|---------|
| **Counting semaphore** | N slots — e.g. max 4 concurrent HTTP fetches |
| **Binary semaphore** | 1 slot — same idea as a mutex (one at a time) |

Go has **no built-in `Semaphore` type** in the standard library. Two idiomatic approaches:

#### A. Buffered channel as semaphore (most common in interviews)

```go
// Semaphore with capacity 4 — at most 4 goroutines inside the critical section
sem := make(chan struct{}, 4)

for _, url := range urls {
    sem <- struct{}{}        // acquire (blocks if 4 already running)
    go func(u string) {
        defer func() { <-sem }()  // release slot when done
        fetch(u)
    }(url)
}
```

- **Acquire:** send on channel (`sem <- struct{}{}`)
- **Release:** receive from channel (`<-sem`)
- Empty `struct{}` uses zero bytes — it's just a signal token

**Your worker pool is a related pattern** (`primenumbers.go`, `workers.go`):
- You spawn exactly **4 worker goroutines** that pull from `tasks` — fixed concurrency
- A semaphore pattern spawns **one goroutine per task** but only **N run at once**

```
Worker pool:     [W1][W2][W3][W4] ← fixed workers pull from tasks chan
Semaphore:       go per task, but sem chan blocks extras until a slot frees
```

Both solve: *"don't spawn unlimited goroutines"* (your `Untitled` crawler notes mention capping at 4 threads).

**Runnable example:** `worker_pool_semaphore.go` — all three patterns side by side.

#### B. `golang.org/x/sync/semaphore` (weighted semaphore)

```go
import "golang.org/x/sync/semaphore"

sem := semaphore.NewWeighted(4)

ctx := context.Background()
if err := sem.Acquire(ctx, 1); err != nil { return }
defer sem.Release(1)

// do work — supports context cancellation while waiting for a slot
```

Use when you need **context-aware acquire** or **weighted** slots (one job costs 2 slots).

#### Semaphore vs Mutex vs Worker Pool

| Tool | Limits | Best for |
|------|--------|----------|
| **Mutex** | 1 goroutine at a time | Protecting shared data (counter, map) |
| **Semaphore** | N goroutines at a time | Limit concurrent I/O (API calls, DB queries, crawls) |
| **Worker pool** | N fixed workers processing a queue | Steady stream of homogeneous tasks |

**Interview Q: How do you limit concurrency to 4 in Go?**
1. Buffered channel semaphore (`make(chan struct{}, 4)`)
2. Worker pool with 4 workers (`primenumbers.go` pattern)
3. `semaphore.NewWeighted(4)` from `x/sync/semaphore`

**Interview Q: Semaphore vs worker pool?**
- **Semaphore:** flexible — one goroutine per task, gate with N slots; good when task count is huge and sporadic
- **Worker pool:** fixed workers reuse goroutines; good for steady job queues and simpler lifecycle

**Interview Q: What happens if you forget to release a semaphore?**
- Slot is leaked — eventually all goroutines block on acquire (deadlock). Always `defer` release, like mutex unlock.

---

### 5. Context Package

**Used in:** `select.go`

| Constructor | Purpose |
|-------------|---------|
| `context.Background()` | Root context (never cancelled) |
| `context.WithCancel(parent)` | Manual cancel via `cancel()` |
| `context.WithTimeout(parent, d)` | Auto-cancel after duration |
| `context.WithDeadline(parent, t)` | Auto-cancel at time |
| `context.WithValue(parent, key, val)` | Request-scoped data (use sparingly) |

**Rules:**
- Always call `defer cancel()` to release resources
- Pass `ctx` as **first parameter** in functions
- Check `ctx.Done()` in long loops and blocking ops

**Interview Q: Why context?**
- Propagate cancellation, deadlines, and request-scoped values across API boundaries and goroutines

---

### 6. HTTP Server & Middleware

**Your code:** `muxservehttp.go`, `panic.go`, `mux_middleware_ratelimiter.go`

**Handler signature:**
```go
func handler(w http.ResponseWriter, r *http.Request) { ... }
```

**Middleware pattern** (wraps `http.Handler`):
```go
func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // before
        next.ServeHTTP(w, r)
        // after
    })
}
```

**Panic recovery** (`panic.go`):
```go
defer func() {
    if err := recover(); err != nil {
        log.Printf("Recovered: %v", err)
        http.Error(w, "Internal Server Error", 500)
    }
}()
```
- `recover()` only works inside `defer`
- **Don't** use panic for normal control flow — use `error` returns

**Rate limiter** — sliding window (`rate_limitter/`, `mux_middleware_ratelimiter.go`):
- Track timestamps of recent requests
- Drop timestamps outside the window
- Allow if count < limit
- Per-IP via `net.SplitHostPort(r.RemoteAddr)`

**Interview Q: `http.DefaultServeMux` vs custom `ServeMux`?**
- Default is a global singleton — fine for demos, bad for libraries/tests
- Custom mux gives isolated routing and is easier to test with `httptest`

**Interview Q: How to test HTTP handlers?**
```go
ts := httptest.NewServer(handler)
defer ts.Close()
resp, _ := http.Get(ts.URL + "/users/1")
```
See `go_hexagonal/server_test.go`.

---

### 7. Interfaces & Design Patterns

**Implicit interfaces** — no `implements` keyword:
```go
type IUserRepository interface {
    GetByID(id int) (*User, error)
}
// UserRepository satisfies this automatically if it has GetByID
```

**Decorator pattern** (`design_pattrens/decorator.go`):
```go
type Beverage interface { getPrice() int }

type Mocha struct {
    b     Beverage  // wraps inner beverage
    price int
}
func (m *Mocha) getPrice() int { return m.price + m.b.getPrice() }
```
Stack decorators: `Cardamom{ Mocha{ Coffee } }` → prices add up.

**Hexagonal architecture** (`go_hexagonal/`):
```
HTTP Handler (adapter) → UserService (domain) → IUserRepository (port) → UserRepository (adapter) → DB
                              ↓
                          CacheLayer
```
- **Ports** = interfaces the domain defines (`IUserRepository`)
- **Adapters** = concrete implementations (HTTP handler, DB repo)
- Domain doesn't import HTTP or DB details — testable, swappable

**Interview Q: Composition vs inheritance?**
- Go has **no inheritance**. Use struct embedding and interfaces for composition.

**Interview Q: Empty interface `interface{}` / `any`?**
- Holds any type. Use type assertion `v.(T)` or type switch. Prefer generics or concrete types when possible.

---

### 8. Reflection

**Your code:** `reflect.go`, `reflect_typeassertion.go`

```go
v := reflect.ValueOf(s)
t := reflect.TypeOf(s)
field.Tag.Get("validate")   // read struct tags
v.Field(i).IsZero()         // check zero value
```

**Type assertion vs type switch:**
```go
switch v := msg.(type) {
case User:   fmt.Println(v.Name)
case Product: fmt.Println(v.ID)
default:     fmt.Println("unknown")
}
```

**Interview Q: When to use reflection?**
- Serialization (JSON), ORM, validation frameworks, generic utilities
- **Avoid** in hot paths — slower, no compile-time checks

**Interview Q: `reflect.ValueOf(x)` — pointer or value?**
- Pass pointer if you need to **set** fields: `reflect.ValueOf(&target).Elem()`

---

### 9. JSON Marshal / Unmarshal

**Your code:** `marshallunmarshall.go`, `reflect.go`

```go
type User struct {
    Name string `json:"name"`
    Age  int    `json:"age,omitempty"`  // omit if zero
}
data, _ := json.Marshal(user)
json.Unmarshal(data, &user)  // MUST pass pointer
```

**Gotcha:** JSON numbers unmarshal as `float64` in `map[string]interface{}` — your `reflect.go` handles `float64 → int` conversion.

**Interview Q: Exported vs unexported fields?**
- Only **exported** (capitalized) fields are encoded/decoded by `encoding/json`

---

### 10. Optimistic Locking

**Your code:** `optimistic_locaking.go`

```
Read record + version → modify locally → UPDATE WHERE version = X
If version changed → conflict → retry or fail
```

- No DB row lock during read
- Good for low-contention updates
- Pair with `Version int` column; increment on every write

**Interview Q: Optimistic vs pessimistic locking?**
| | Optimistic | Pessimistic |
|---|-----------|-------------|
| Lock on read | No | Yes (`SELECT FOR UPDATE`) |
| Conflict handling | Retry / fail at write | Blocked until lock released |
| Best for | Low contention | High contention |

---

### 11. Error Handling

```go
if err != nil {
    return nil, fmt.Errorf("get user %d: %w", id, err)  // wrap with %w
}
```

- No try/catch — explicit `error` return
- `errors.Is(err, target)` / `errors.As(err, &target)` for wrapped errors (Go 1.13+)
- Panic only for truly unrecoverable programmer bugs

**Interview Q: nil interface vs nil pointer in interface?**
```go
var p *User = nil
var i interface{} = p
fmt.Println(i == nil)  // false! interface holds (type=*User, value=nil)
```

---

### 12. Testing

**Your code:** `rate_limitter/main_test.go`, `go_hexagonal/server_test.go`

```go
func TestSomething(t *testing.T) {
    if got != want {
        t.Errorf("got %d, want %d", got, want)
    }
}
```

```bash
go test ./...          # all packages
go test -v -run TestRatelimiter
go test -race ./...    # race detector — ALWAYS use for concurrency tests
```

**Table-driven tests** (idiomatic Go, not in repo but expected in interviews):
```go
tests := []struct{ input, want int }{{1, 2}, {2, 4}}
for _, tt := range tests {
    t.Run(fmt.Sprint(tt.input), func(t *testing.T) {
        if got := double(tt.input); got != tt.want { t.Errorf(...) }
    })
}
```

---

### 13. Generics (Go 1.18+)

**Your code:** `generic_worker.go`

```go
type WorkerPoolG[T any, R any] struct { ... }

func NewWorkerPool[T any, R any](n int) *WorkerPoolG[T, R] { ... }
```

**Constraints:**
```go
func Sum[T ~int | ~float64](nums []T) T { ... }
```

**Interview Q: When generics vs interfaces?**
- Generics: type-safe containers, algorithms on comparable types
- Interfaces: behavior polymorphism (methods)

---

## Top 28 Interview Questions (with short answers)

### Language Basics
1. **What is a goroutine?** Lightweight concurrent function; `go f()`.
2. **Value vs pointer receiver?** Pointer mutates original, avoids copy for large structs, required for `sync.Mutex` methods.
3. **What is a slice?** View over array: `ptr, len, cap`. `append` may reallocate.
4. **Map iteration order?** Randomized (intentionally, since Go 1).
5. **What is `init()`?** Runs before `main`, per file, in dependency order. Don't abuse it.

### Concurrency
6. **How to avoid data races?** Mutex, channels, or confine data to one goroutine.
7. **What does `-race` do?** Instruments code to detect concurrent unsynchronized access.
8. **Can you read from a nil channel?** Blocks forever.
9. **What happens on send to nil channel?** Blocks forever.
10. **Explain happens-before in Go.** Channel send happens-before receive; `wg.Done()` happens-before `wg.Wait()` returns.
11. **What is a semaphore in Go?** No stdlib type — use buffered `chan struct{}` (capacity N) or `golang.org/x/sync/semaphore`. Limits concurrent goroutines to N. See [§4 Semaphores](#4-semaphores).
12. **Semaphore vs worker pool?** Semaphore gates one-goroutine-per-task; worker pool uses N fixed workers on a shared task queue. Both cap concurrency.
13. **Buffered vs unbuffered channel?** Unbuffered = sync hand-off (send blocks until recv). Buffered = queue of N (send blocks only when full). See [§2 Buffered vs unbuffered](#buffered-vs-unbuffered-channels).

### Memory & Performance
14. **Stack vs heap?** Escape analysis decides; don't optimize prematurely.
15. **What is a defer cost?** Small memory + CPU overhead per deferred call (stack walk on exit). Negligible for a few defers; prefer clarity over micro-optimization. Runs on normal return **and** during panic unwind (before `recover` catches it). See [§2 defer](#2-functions) for full explanation.
16. **String immutability?** Strings are read-only byte slices; converting to `[]byte` copies.

### Interfaces & Types
17. **Duck typing?** If it has the methods, it satisfies the interface.
18. **Type assertion `v, ok := x.(T)`?** Safe cast; `ok` false if wrong type.
19. **`any` vs `interface{}`?** Same thing; `any` is alias (Go 1.18).

### HTTP & Production
20. **Graceful shutdown?** `srv.Shutdown(ctx)` stops accepting, drains connections.
21. **How to pass request ID?** `context.WithValue` or middleware setting header.
22. **Rate limiting algorithms?** Token bucket, leaky bucket, sliding window (your code), fixed window.

### Patterns
23. **Dependency injection in Go?** Pass interfaces via constructors: `NewUserService(repo IUserRepository)`.
24. **Functional options pattern?** `func WithTimeout(d time.Duration) Option` — common in libraries.
25. **Worker pool sizing?** CPU-bound → `GOMAXPROCS`; I/O-bound → higher count.

### Error & Panic
26. **When to panic?** Almost never in libraries; OK in `main` for fatal startup errors.
27. **`defer` + `recover` pattern?** Only in HTTP middleware or top-level goroutine wrappers.

### Modules
28. **What does `go.mod` do?** Module path, Go version, dependency versions. `go mod tidy` cleans deps.

---

## Common Coding Interview Tasks (Go-flavored)

| Task | Pattern in this repo |
|------|---------------------|
| Implement worker pool | `workers.go`, `generic_worker.go` |
| Limit concurrency to N | `worker_pool_semaphore.go`, buffered channel `make(chan struct{}, N)` |
| Print odd/even alternately | `oddeven.go` |
| Rate limiter | `rate_limitter/`, `mux_middleware_ratelimiter.go` |
| HTTP middleware chain | `panic.go`, rate limiter middleware |
| Fan-out / fan-in | `primenumbers.go` |
| Graceful timeout | `select.go` |
| LRU / cache layer | `go_hexagonal/cache.go` |
| REST handler + JSON | `go_hexagonal/user_handler.go` |
| Concurrent-safe counter | `test.go` (mutex around shared state) |
| Decorator / wrapper | `design_pattrens/decorator.go` |

---

## Quick Commands Before the Interview

```bash
go version
go run main.go
go build -o app .
go test ./...
go test -race ./...
go mod init example.com/myapp
go mod tidy
go vet ./...
gofmt -w .          # format (always run before submitting code)
```

---

## 5-Minute Pre-Interview Drill

**Basics (do first):**
1. Write: `var`, `:=`, pointer `&x` / `*p`, struct literal, value vs pointer receiver
2. Say: "Go has no classes, no inheritance, no references — only pointers"
3. Explain: slice is `(ptr, len, cap)`; map is not concurrent-safe

**Concurrency (if asked):**
4. Draw worker pool: tasks chan → workers → results chan → close order
5. Explain why `close(results)` is needed before `for range results`
6. Write HTTP middleware: `func(next http.Handler) http.Handler`

**Sanity check:** `cd rate_limitter && go test -v`

---

## Known Quirks in This Repo

- Root `package main` files can't all run together — rename one `main*` to `main`
- `marshallunmarshall.go` unmarshals into `User` but defines `MyUser` — typo from learning
- `go_todo_app/` is a stub (requirements only in its README)
- `concurrency/main.go` is empty — logic is in `channels_deadlocks.go`

Good luck in your interview.
