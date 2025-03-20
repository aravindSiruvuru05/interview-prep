package main

import (
	"fmt"
	"sync"
)

func printNumbers() {
	oddChan := make(chan bool)
	evenChan := make(chan bool)
	var wg sync.WaitGroup

	wg.Add(2)

	// Goroutine 1: Prints odd numbers
	go func() {
		defer wg.Done()
		for i := 1; i <= 9; i += 2 {
			<-oddChan
			fmt.Print(i, " ")
			evenChan <- true
		}
	}()

	// Goroutine 2: Prints even numbers
	go func() {
		defer wg.Done()
		for i := 2; i <= 10; i += 2 {
			<-evenChan
			fmt.Print(i, " ")
			if i == 10 {
				break
			}
			oddChan <- true
		}
	}()

	// Start the sequence by triggering oddChan
	oddChan <- true

	wg.Wait()
}

func main423() {
	printNumbers()
}
