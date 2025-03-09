package main

import (
	"errors"
	"fmt"
	"sync"
)

// Simulated database record
type Record struct {
	ID      int
	Value   string
	Version int // This is the version for optimistic locking
}

// Global map to simulate our database
var db = make(map[int]*Record)

// Mutex to simulate database locking
var dbMutex sync.Mutex

// Function to simulate fetching a record from the database
func fetchRecord(id int) (*Record, error) {
	dbMutex.Lock()
	defer dbMutex.Unlock()

	record, exists := db[id]
	if !exists {
		return nil, errors.New("record not found")
	}
	return record, nil
}

// Function to simulate updating a record with optimistic locking
func updateRecord(id int, newValue string, version int) error {
	dbMutex.Lock()
	defer dbMutex.Unlock()

	record, exists := db[id]
	if !exists {
		return errors.New("record not found")
	}

	// Check if the version matches
	if record.Version != version {
		return errors.New("optimistic lock failed: record has been modified")
	}

	// Proceed with the update if the version matches
	record.Value = newValue
	record.Version++ // Increment the version to indicate an update
	return nil
}

// Simulate a user updating a record
func simulateUpdate(id int, newValue string, version int) {
	err := updateRecord(id, newValue, version)
	if err != nil {
		fmt.Println("Error:", err)
	} else {
		fmt.Println("Update successful!")
	}
}

func Main2() {
	// Initialize the database with a record
	db[1] = &Record{ID: 1, Value: "Original Value", Version: 1}

	// Simulate fetching the record
	record, err := fetchRecord(1)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	fmt.Printf("Fetched Record: ID=%d, Value=%s, Version=%d\n", record.ID, record.Value, record.Version)

	// Simulate two users trying to update the same record concurrently
	go simulateUpdate(1, "Updated by User 1", record.Version)
	go simulateUpdate(1, "Updated by User 2", record.Version)

	// Wait for goroutines to finish
	var input string
	fmt.Scanln(&input)
}
