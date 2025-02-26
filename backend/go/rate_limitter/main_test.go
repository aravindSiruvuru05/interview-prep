package main

import (
	"fmt"
	"sync"
	"testing"
	"time"
)

func TestRatelimiter(t *testing.T) {
	rl := NewRateLimiter(5, time.Second)

	wg := &sync.WaitGroup{}
	mu := &sync.Mutex{}
	var accepted int
	for range 10 { // Corrected the range loop
		wg.Add(1)
		go func() {
			defer wg.Done()
			if rl.Allow() {
				mu.Lock()
				accepted++
				mu.Unlock()
			}
		}()
	}
	wg.Wait()

	fmt.Println(accepted)
	if accepted > 5 {
		t.Errorf("Expected at most 5 requests to be accepted, but got %d", accepted)
	}

	// Test time window
	time.Sleep(time.Second) // Wait for the time window to expire

	accepted2 := 0
	for range 5 {
		if rl.Allow() {
			accepted2++
		}
	}

	if accepted2 != 5 {
		t.Errorf("Expected 5 requests to be accepted after time window expired, but got %d", accepted2)
	}

	//Test for concurrency safety.
	rl2 := NewRateLimiter(5, time.Second)
	var accepted3 int
	var wg2 sync.WaitGroup

	for range 100 {
		wg2.Add(1)
		go func() {
			defer wg2.Done()
			if rl2.Allow() {
				mu.Lock()
				accepted3++
				mu.Unlock()
			}
		}()
	}
	wg2.Wait()

	if accepted3 > 5 {
		t.Errorf("Expected no more than 5 requests to be accepted in the time window, got %d", accepted3)
	}

}
