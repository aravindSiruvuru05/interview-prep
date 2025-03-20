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

