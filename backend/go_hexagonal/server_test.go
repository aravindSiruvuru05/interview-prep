package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/http/httptest"
	"sync"
	"testing"
	"time"
)

func TestHandleGetUser(t *testing.T) {
	db := NewDB()

	userRepo := NewUserRepository(db)

	userService := NewUserService(userRepo)

	UserController := &UserController{
		Service: userService,
	}

	ts := httptest.NewServer(http.HandlerFunc(UserController.HandleUsersRouter))
	wg := &sync.WaitGroup{}

	for i := range 1000 { // Run 1000 goroutines concurrently without limits
		wg.Add(1)
		go func(idx int) {
			defer wg.Done()

			id := idx%100 + 1
			url := fmt.Sprintf("%s/users/%d", ts.URL, id)
			res, err := http.Get(url)
			if err != nil {
				t.Error(err)
				return
			}
			defer res.Body.Close()

			// Read the response body
			body, err := io.ReadAll(res.Body)
			if err != nil {
				t.Error(err)
				return
			}

			user := &User{}
			err = json.Unmarshal(body, user)
			if err != nil {
				t.Error("Error unmarshalling response:", err)
				return
			}

			fmt.Printf("User ID: %d, User Name: %s\n", user.ID, user.Name)
		}(i)
		time.Sleep(time.Millisecond * 1)
	}
	wg.Wait() // Wait for all goroutines to finish
	fmt.Printf("Total hits: %d", db.Hits)
}
