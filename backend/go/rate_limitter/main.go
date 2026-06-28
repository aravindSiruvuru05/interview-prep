package main

import (
	"sync"
	"time"
)

type RateLimiter struct {
	Limit          int
	Window         time.Duration
	PrevTimeStamps []time.Time
	MU             sync.Mutex
}

func NewRateLimiter(limit int, withInTime time.Duration) *RateLimiter {
	return &RateLimiter{
		Limit:          limit,
		Window:         withInTime,
		PrevTimeStamps: []time.Time{},
		MU:             sync.Mutex{},
	}
}

func (r *RateLimiter) Allow() bool {
	r.MU.Lock()
	defer r.MU.Unlock()
	// check the existing timestaps are still valid and remove all invalid and expired by checking if they are outside the limit
	newTS := []time.Time{}
	now := time.Now()
	for _, ts := range r.PrevTimeStamps {
		if now.Sub(ts) < r.Window {
			newTS = append(newTS, ts)
		}
	}
	r.PrevTimeStamps = newTS

	if len(r.PrevTimeStamps) < r.Limit {
		r.PrevTimeStamps = append(r.PrevTimeStamps, now)
		return true
	}
	return false
}



// -------------------------------------------------------------

package main

import (
	"sync"
	"time"
)

type FixedWindowLimiter struct {
	Limit       int
	Window      time.Duration
	count       int
	windowStart time.Time
	mu          sync.Mutex
}

func NewFixedWindowLimiter(limit int, window time.Duration) *FixedWindowLimiter {
	return &FixedWindowLimiter{
		Limit:       limit,
		Window:      window,
		windowStart: time.Now(),
	}
}

func (r *FixedWindowLimiter) Allow() bool {
	r.mu.Lock()
	defer r.mu.Unlock()

	now := time.Now()
	if now.Sub(r.windowStart) >= r.Window {
		// window expired; start a fresh one
		r.windowStart = now
		r.count = 0
	}

	if r.count < r.Limit {
		r.count++
		return true
	}
	return false
}