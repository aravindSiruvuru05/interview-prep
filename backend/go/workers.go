package main

import (
	"fmt"
	"sync"
	"time"
)

type Worker struct {
	Tasks      chan interface{}
	WorkersCnt int
	WG         sync.WaitGroup
	TaskWg     sync.WaitGroup
}

func NewWorker(wCnt int) *Worker {
	return &Worker{
		Tasks:      make(chan interface{}),
		WorkersCnt: wCnt,
	}
}

func (w *Worker) Start(do func(task interface{})) {
	for i := range w.WorkersCnt {
		fmt.Println(i)
		w.WG.Add(1)
		go func(workerID int) {
			defer w.WG.Done()
			for t := range w.Tasks {
				do(t)
				w.TaskWg.Done()
			}
		}(i)
	}
}

func (w *Worker) Add(input interface{}) {
	w.TaskWg.Add(1)
	w.Tasks <- input
}

func (w *Worker) Wait() {
	w.TaskWg.Wait()
	close(w.Tasks)
	w.WG.Wait()
}

func main() {
	pool := NewWorker(5)

	workerFunc := func(task interface{}) {
		taskID := task.(int)
		time.Sleep(time.Millisecond * 10)
		fmt.Printf("Processing task %d\n", taskID)
	}

	pool.Start(workerFunc)

	for i := 1; i <= 200; i++ {
		pool.Add(i)
	}

	pool.Wait()

	fmt.Println("All tasks processed!")
}
