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

func worker(tasks chan int, result chan int, wg *sync.WaitGroup) {
	defer wg.Done()
	for t := range tasks {
		if isPrime(t) {
			result <- t
		}
	}
}
func maindd() {


	
	start := 1
	end := 100
	workersCnt := 4

	tasks := make(chan int)
	var wg sync.WaitGroup
	result := make(chan int)

	for range workersCnt {
		wg.Add(1)
		go worker(tasks, result, &wg)
	}

	go func() {
		for i := start; i < end; i += 1 {
			tasks <- i
		}
		close(tasks)
	}()

	go func() {
		wg.Wait()
		close(result)
	}()

	var primes []int
	for r := range result {
		primes = append(primes, r)
	}

	fmt.Println(primes)

}
