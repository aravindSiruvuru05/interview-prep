package main

import (
	"fmt"
	"log"
	"net/http"
)

// RecoveryMiddleware applied globally
func RecoveryMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				log.Printf("Recovered from panic: %v", err)
				http.Error(w, "Internal Server Error", http.StatusInternalServerError)
			}
		}()
		next.ServeHTTP(w, r)
	})
}

// Normal handlers
func RiskyHandler(w http.ResponseWriter, r *http.Request) {
	panic("oops! something broke here.")
}

func SafeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Hello from a safe handler!")
}

func main123() {
	// Register handlers as usual
	http.HandleFunc("/panic", RiskyHandler)
	http.HandleFunc("/safe", SafeHandler)

	// Apply recovery middleware globally
	log.Println("Server started on :8080")
	http.ListenAndServe(":8080", RecoveryMiddleware(http.DefaultServeMux))
}
