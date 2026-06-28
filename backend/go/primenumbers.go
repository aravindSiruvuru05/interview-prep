package main

import (
	"fmt"
	"math"
	"sync"
)

func isPrime(num int) bool {
	if num < 2 {
		return false
	}
	for i := 2; i <= int(math.Sqrt(float64(num))); i++ {
		if num%i == 0 {
			return false
		}
	}
	return true
}

func worker(tasks <-chan int, result chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()
	for t := range tasks {
		if isPrime(t) {
			result <- t
		}
	}
}

// -----------------------------------------------------------------------------
// Unbuffered channels — synchronous hand-off (producer ↔ worker ↔ collector)
//
//   tasks := make(chan int)   // capacity 0 — send blocks until a worker receives
//   result := make(chan int)  // worker blocks on send until main receives
// -----------------------------------------------------------------------------
func findPrimesUnbuffered(start, end, workersCnt int) []int {
	tasks := make(chan int)
	result := make(chan int)
	// var wg sync.WaitGroup
	wg := sync.WaitGroup{}


	for i := 0; i < workersCnt; i++ {
		wg.Add(1)
		go worker(tasks, result, &wg)
	}

	go func() {
		for i := start; i < end; i++ {
			tasks <- i // blocks until a worker is ready
		}
		close(tasks)
	}()

	go func() {
		wg.Wait()
		close(result)
	}()

	primes := make([]int, 0)
	for r := range result {
		primes = append(primes, r)
	}
	return primes
}

// -----------------------------------------------------------------------------
// Buffered channels — queue tasks upfront; decouple worker sends from collector
//
//   tasks := make(chan int, taskCount)   // preload all jobs, then close
//   result := make(chan int, taskCount)  // workers won't block sending primes
// -----------------------------------------------------------------------------
func findPrimesBuffered(start, end, workersCnt int) []int {
	taskCount := end - start
	tasks := make(chan int, taskCount)
	result := make(chan int, taskCount)
	var wg sync.WaitGroup

	for i := 0; i < workersCnt; i++ {
		wg.Add(1)
		go worker(tasks, result, &wg)
	}

	// Preload buffer — producer does not wait for workers
	for i := start; i < end; i++ {
		tasks <- i
	}
	close(tasks)

	go func() {
		wg.Wait()
		close(result)
	}()

	primes := make([]int, 0)
	for r := range result {
		primes = append(primes, r)
	}
	return primes
}

// Rename to main() to run
func maindd() {
	start := 1
	end := 100
	workersCnt := 4

	fmt.Println("--- Unbuffered ---")
	primesUnbuf := findPrimesUnbuffered(start, end, workersCnt)
	fmt.Println(primesUnbuf)

	fmt.Println("\n--- Buffered ---")
	primesBuf := findPrimesBuffered(start, end, workersCnt)
	fmt.Println(primesBuf)
}
