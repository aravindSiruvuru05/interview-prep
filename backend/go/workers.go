package main

import (
	"fmt"
	"sync"
	"time"
)

type WorkerPool struct {
	tasks   chan int
	results chan int
	wg      sync.WaitGroup
}

func NewWorkerPool(numWorkers, taskBufferSize int) *WorkerPool {
	wp := &WorkerPool{
		tasks:   make(chan int, taskBufferSize),
		results: make(chan int, taskBufferSize),
	}

	for i := 0; i < numWorkers; i++ { // Corrected loop
		wp.wg.Add(1)
		go wp.worker()
	}

	go func() {
		wp.wg.Wait()
		close(wp.results)
	}()

	return wp
}

func (wp *WorkerPool) worker() {
	defer wp.wg.Done()
	for task := range wp.tasks {
		wp.results <- processTasks(task)
	}
}

func (wp *WorkerPool) AddTask(task int) {
	wp.tasks <- task
}

func (wp *WorkerPool) GetResults() <-chan int {
	return wp.results
}

func processTasks(n int) int {
	time.Sleep(time.Millisecond * 10)
	return n * 2
}

func main1() {
	wp := NewWorkerPool(3, 10) // 3 workers, buffer 10 tasks

	for i := 1; i <= 20; i++ {
		wp.AddTask(i)
	}
	close(wp.tasks) // Signal no more tasks

	for result := range wp.GetResults() {
		fmt.Println("Result:", result)
	}
}
