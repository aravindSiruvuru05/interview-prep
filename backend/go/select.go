package main

import (
	"context"
	"fmt"
	"time"
)

// Simulate slow or fast work
func doWork(ctx context.Context, ch chan<- string) {
	// Simulate a job that might finish late or early
	select {
	case <-time.After(3 * time.Second): // simulate a long task
		ch <- "Work completed successfully!"
	case <-ctx.Done(): // listen for context cancellation
		fmt.Println("Worker aborted due to:", ctx.Err())
	}
}

func maisn() {
	// Create context with a timeout
	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel() // always clean up context

	ch := make(chan string)

	// Launch worker goroutine
	go doWork(ctx, ch)

	select {
	case msg := <-ch:
		fmt.Println("Received:", msg)
	case <-ctx.Done():
		fmt.Println("Main aborted due to:", ctx.Err())
	}
}
