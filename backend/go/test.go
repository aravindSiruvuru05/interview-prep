package main

import (
	"fmt"
	"sync"
	"time"
)

type RateLimiter struct {
	Limit          int
	Window         time.Duration
	PrevTimestamps []time.Time
}

func (r *RateLimiter) Allow() bool {
	now := time.Now()
	var newTS []time.Time
	for _, prev := range r.PrevTimestamps {
		if now.Sub(prev) < r.Window {
			newTS = append(newTS, prev)
		}
	}
	r.PrevTimestamps = newTS
	if len(newTS) < r.Limit {
		r.PrevTimestamps = append(r.PrevTimestamps, now)
		return true
	}
	return false

}

func main() {

	rl := &RateLimiter{
		Limit:          5,
		Window:         time.Second,
		PrevTimestamps: []time.Time{},
	}
	var counter int
	var mu sync.Mutex
	var wg sync.WaitGroup
	for i := range 10 {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			mu.Lock()
			if rl.Allow() {
				counter += 1
			} else {
				fmt.Println("not allowed")
			}
			mu.Unlock()
		}(i)
	}

	wg.Wait()
	fmt.Println(counter)
}
