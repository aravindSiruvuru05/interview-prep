package main

import (
	"fmt"
	"net/http"
)

func homeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Welcome to the Home Page!")
}

func aboutHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "This is the About Page!")
}

func contactHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintln(w, "Contact us at contact@example.com")
}

func main32() {
	// Create a custom mux (router)
	mux := http.NewServeMux()

	// Register handlers with paths
	mux.HandleFunc("/", homeHandler)
	mux.HandleFunc("/about", aboutHandler)
	mux.HandleFunc("/contact", contactHandler)

	// Start server with the custom mux
	fmt.Println("Server is running on :8080")
	http.ListenAndServe(":8080", mux)
}
