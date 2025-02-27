package main

import (
	"fmt"
	"sync"
	"time"
)

func process(n int) int {
	time.Sleep(time.Millisecond * 10)
	return n * 2
}

func ChannelsAndDeadloackBehaviour() {
	arr := []int{2, 3, 4, 5, 5, 6, 77, 8, 12}
	numWorkers := 3

	tasks := make(chan int, len(arr))
	for _, el := range arr {
		tasks <- el
	}
	close(tasks)

	results := make(chan int, len(arr))
	wg := &sync.WaitGroup{}

	for range numWorkers {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for task := range tasks {
				results <- process(task)
			}
		}()
	}

	go func() {
		wg.Wait()
		// if you dont close the channel here. it will result in deadloack
		// fatal error: all goroutines are asleep - deadlock!
		// for result := range results Loop:
		// If you omit close(results), the results channel will remain open.
		// The for result := range results loop will continue to wait for more values,
		// even after all worker goroutines have finished.

		// The for result := range results loop in the main function is designed
		//  to receive values from the results channel.
		// This loop will continue to iterate as long as the channel is open
		// and has values to receive.
		// Once the channel is closed, the loop will terminate.
		close(results)

	}()

	var resultArray []int
	for result := range results {
		resultArray = append(resultArray, result)
	}

	fmt.Println(resultArray)
}

// Consequences

// Program Hangs: The program will stop responding.
// No Further Execution: Any code after the for result := range results loop will not be executed.
// Resource Leaks: If your program is part of a larger system, it might lead to resource leaks.
// Why close(results) Is Essential

// Signal Completion: close(results) explicitly signals that no more values will be sent on the channel.
// Terminate the Loop: It allows the for result := range results loop to terminate gracefully.
// Prevent Deadlocks: It prevents the program from hanging indefinitely.
// In summary:

// Closing channels is crucial when you're using for range loops to receive data from them.
//  It prevents deadlocks and ensures that your program terminates correctly.
// In the provided example, close(results) is essential to signal the end of the data stream and
// allow the for result := range results loop to complete.
