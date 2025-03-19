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
	ResultChan chan interface{} // optional when we want to return some value back
	Results    []interface{}
}

func NewWorker(wCnt int) *Worker {
	return &Worker{
		Tasks:      make(chan interface{}),
		ResultChan: make(chan interface{}),
		WorkersCnt: wCnt,
		Results:    []interface{}{},
	}
}

func (w *Worker) Start(do func(task interface{}) interface{}) {
	w.AccumlateResults()
	for i := range w.WorkersCnt {
		fmt.Println(i)
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

func (w *Worker) AccumlateResults() {
	go func() {
		for r := range w.ResultChan {
			w.Results = append(w.Results, r)
		}
	}()
}

func (w *Worker) Add(input interface{}) {
	w.TaskWg.Add(1)
	w.Tasks <- input
}

func (w *Worker) Wait() {
	w.TaskWg.Wait()
	close(w.Tasks)
	close(w.ResultChan)
	w.WG.Wait()
}

func main12() {
	pool := NewWorker(5)

	workerFunc := func(task interface{}) interface{} {
		taskID := task.(int)
		time.Sleep(time.Millisecond * 10)
		fmt.Printf("Processing task %d\n", taskID)
		return taskID * taskID
	}

	pool.Start(workerFunc)

	for i := 1; i <= 200; i++ {
		pool.Add(i)
	}

	pool.Wait()

	fmt.Println("All tasks processed!", pool.Results)
}
