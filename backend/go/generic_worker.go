package main

import (
	"fmt"
	"sync"
	"time"
)

// Step 2: Generic worker struct
type WorkerPoolG[T any, R any] struct {
	Tasks      chan T
	Results    []R
	WorkersCnt int
	ResultChan chan R
	WG         sync.WaitGroup
	TaskWg     sync.WaitGroup
}

// Step 3: Generic factory function
func NewWorkerPool[T any, R any](wpCnt int) *WorkerPoolG[T, R] {
	return &WorkerPoolG[T, R]{
		Tasks:      make(chan T),
		ResultChan: make(chan R),
		WorkersCnt: wpCnt,
		Results:    []R{},
	}
}

// Step 4: Worker logic stays the same
func (w *WorkerPoolG[T, R]) Start(do func(task T) R) {
	w.accumulateResults()
	for i := 0; i < w.WorkersCnt; i++ {
		w.WG.Add(1)
		go func(workerID int) {
			defer w.WG.Done()
			for t := range w.Tasks {
				w.ResultChan <- do(t)
				w.TaskWg.Done()
			}
		}(i)
	}
}

func (w *WorkerPoolG[T, R]) accumulateResults() {
	go func() {
		for r := range w.ResultChan {
			w.Results = append(w.Results, r)
		}
	}()
}

func (w *WorkerPoolG[T, R]) Add(input T) {
	w.TaskWg.Add(1)
	w.Tasks <- input
}

func (w *WorkerPoolG[T, R]) Wait() {
	w.TaskWg.Wait()
	close(w.Tasks)
	close(w.ResultChan)
	w.WG.Wait()
}

func main234() {
	// Later, attach generic types!
	pool := NewWorkerPool[int, int](5)

	workerFunc := func(task int) int {
		time.Sleep(time.Millisecond * 10)
		fmt.Printf("Processing task %d\n", task)
		return task * task
	}

	pool.Start(workerFunc)

	for i := 1; i <= 200; i++ {
		pool.Add(i)
	}

	pool.Wait()

	fmt.Println("All tasks processed!", pool.Results)
}
