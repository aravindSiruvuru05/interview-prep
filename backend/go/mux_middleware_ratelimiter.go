package main

import (
	"fmt"
	"net"
	"net/http"
	"sync"
	"time"
)

type MRateLimiter struct {
	Limit          int
	Window         time.Duration
	PrevTimeStamps []time.Time
	MU             sync.Mutex
}

func NewMRateLimiter(limit int, withInTime time.Duration) *MRateLimiter {
	return &MRateLimiter{
		Limit:          limit,
		Window:         withInTime,
		PrevTimeStamps: []time.Time{},
	}
}

func (r *MRateLimiter) Allow() bool {
	r.MU.Lock()
	defer r.MU.Unlock()

	now := time.Now()
	newTS := []time.Time{}

	// Filter valid timestamps within the window
	for _, ts := range r.PrevTimeStamps {
		if now.Sub(ts) < r.Window {
			newTS = append(newTS, ts)
		}
	}
	r.PrevTimeStamps = newTS

	// Check if under limit
	if len(r.PrevTimeStamps) < r.Limit {
		r.PrevTimeStamps = append(r.PrevTimeStamps, now)
		return true
	}
	return false
}

// === IP-based limiter storage ===
type MRateLimiterManager struct {
	limiters map[string]*MRateLimiter
	mu       sync.Mutex
	Limit    int
	Window   time.Duration
}

func NewMRateLimiterManager(limit int, window time.Duration) *MRateLimiterManager {
	return &MRateLimiterManager{
		limiters: make(map[string]*MRateLimiter),
		Limit:    limit,
		Window:   window,
	}
}

func (rm *MRateLimiterManager) getLimiter(ip string) *MRateLimiter {
	rm.mu.Lock()
	defer rm.mu.Unlock()

	if limiter, ok := rm.limiters[ip]; ok {
		return limiter
	}
	limiter := NewMRateLimiter(rm.Limit, rm.Window)
	rm.limiters[ip] = limiter
	return limiter
}

// Middleware
func (rm *MRateLimiterManager) Middleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		ip, _, _ := net.SplitHostPort(r.RemoteAddr)
		limiter := rm.getLimiter(ip)
		if !limiter.Allow() {
			w.WriteHeader(http.StatusTooManyRequests)
			fmt.Fprintln(w, "429 - Too Many Requests")
			return
		}
		next.ServeHTTP(w, r)
	})
}

func apiHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "✅ Success! You're within the rate limit.")
}

func maasin() {
	rm := NewMRateLimiterManager(5, 5*time.Second) // 5 requests per 5 seconds window

	mux := http.NewServeMux()
	mux.HandleFunc("/api", apiHandler)

	handler := rm.Middleware(mux)

	fmt.Println("Server running on :8080 with sliding window rate limiter")
	http.ListenAndServe(":8080", handler)
}
