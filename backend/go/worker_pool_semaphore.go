package main

import (
	"fmt"
	"sync"
	"time"
)

// =============================================================================
// Pattern 1: Fixed worker pool
// N goroutines pull tasks from a shared channel — see primenumbers.go, workers.go
// =============================================================================

type WorkerPool[T any, R any] struct {
	workers int
	tasks   chan T
	results chan R
	wg      sync.WaitGroup
}

func NewWorkerPool[T any, R any](workers int) *WorkerPool[T, R] {
	return &WorkerPool[T, R]{
		workers: workers,
		tasks:   make(chan T),
		results: make(chan R),
	}
}

func (p *WorkerPool[T, R]) Start(process func(T) R) {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go func(workerID int) {
			defer p.wg.Done()
			for task := range p.tasks {
				p.results <- process(task)
			}
		}(i)
	}
}

func (p *WorkerPool[T, R]) Submit(task T) {
	p.tasks <- task
}

func (p *WorkerPool[T, R]) CloseAndCollect() []R {
	close(p.tasks)
	go func() {
		p.wg.Wait()
		close(p.results)
	}()

	out := make([]R, 0)
	for r := range p.results {
		out = append(out, r)
	}
	return out
}

// =============================================================================
// Pattern 2: Semaphore
// One goroutine per task, but at most N run at once — good for crawlers / HTTP
// =============================================================================

type Semaphore struct {
	slots chan struct{}
}

func NewSemaphore(maxConcurrent int) *Semaphore {
	return &Semaphore{slots: make(chan struct{}, maxConcurrent)}
}

func (s *Semaphore) Acquire() {
	s.slots <- struct{}{} // blocks when N slots are taken
}

func (s *Semaphore) Release() {
	<-s.slots
}

func RunWithSemaphore[T any, R any](tasks []T, maxConcurrent int, process func(T) R) []R {
	sem := NewSemaphore(maxConcurrent)
	results := make([]R, len(tasks))
	var wg sync.WaitGroup

	for i, task := range tasks {
		wg.Add(1)
		go func(idx int, t T) {
			defer wg.Done()
			sem.Acquire()
			defer sem.Release()
			results[idx] = process(t)
		}(i, task)
	}

	wg.Wait()
	return results
}

// =============================================================================
// Pattern 3: Worker pool + semaphore (combined)
// Workers pull from a job queue; semaphore caps in-flight I/O per job.
// Solves: "crawler discovers URLs fast but only 4 HTTP fetches at a time"
// =============================================================================

type BoundedWorkerPool[T any, R any] struct {
	workers int
	jobs    chan T
	results chan R
	sem     *Semaphore
	wg      sync.WaitGroup
}

func NewBoundedWorkerPool[T any, R any](workers int, maxInFlight int) *BoundedWorkerPool[T, R] {
	return &BoundedWorkerPool[T, R]{
		workers: workers,
		jobs:    make(chan T),
		results: make(chan R),
		sem:     NewSemaphore(maxInFlight),
	}
}

func (p *BoundedWorkerPool[T, R]) Start(process func(T) R) {
	for i := 0; i < p.workers; i++ {
		p.wg.Add(1)
		go func() {
			defer p.wg.Done()
			for job := range p.jobs {
				p.sem.Acquire()
				result := process(job)
				p.sem.Release()
				p.results <- result
			}
		}()
	}
}

func (p *BoundedWorkerPool[T, R]) Submit(job T) {
	p.jobs <- job
}

func (p *BoundedWorkerPool[T, R]) CloseAndCollect() []R {
	close(p.jobs)
	go func() {
		p.wg.Wait()
		close(p.results)
	}()

	out := make([]R, 0)
	for r := range p.results {
		out = append(out, r)
	}
	return out
}

func simulateWork(id int) int {
	time.Sleep(20 * time.Millisecond)
	return id * id
}

// Rename to main() to run: go run worker_pool_semaphore.go
func mainWorkerPoolSemaphore() {
	const maxConcurrent = 4
	const taskCount = 20

	inputs := make([]int, taskCount)
	for i := range inputs {
		inputs[i] = i + 1
	}

	fmt.Println("=== Pattern 1: Fixed worker pool ===")
	pool := NewWorkerPool[int, int](maxConcurrent)
	pool.Start(simulateWork)
	for _, n := range inputs {
		pool.Submit(n)
	}
	r1 := pool.CloseAndCollect()
	fmt.Printf("%d tasks, %d workers, first results: %v\n", len(r1), maxConcurrent, r1[:4])

	fmt.Println("\n=== Pattern 2: Semaphore (goroutine per task, max 4 in flight) ===")
	r2 := RunWithSemaphore(inputs, maxConcurrent, simulateWork)
	fmt.Printf("%d tasks, max %d concurrent, first results: %v\n", len(r2), maxConcurrent, r2[:4])

	fmt.Println("\n=== Pattern 3: Worker pool + semaphore ===")
	bounded := NewBoundedWorkerPool[int, int](maxConcurrent, maxConcurrent)
	bounded.Start(simulateWork)
	for _, n := range inputs {
		bounded.Submit(n)
	}
	r3 := bounded.CloseAndCollect()
	fmt.Printf("%d tasks, first results: %v\n", len(r3), r3[:4])

	fmt.Println("\nPick the right tool:")
	fmt.Println("  Worker pool      → steady job queue, reuse N goroutines")
	fmt.Println("  Semaphore        → many tasks, cap concurrent I/O (crawler)")
	fmt.Println("  Pool + semaphore → queue workers + hard limit on in-flight work")
}
