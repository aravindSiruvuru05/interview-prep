package main

import (
	"fmt"
	"net/http"
)

func maiasn() {

	db := NewDB()

	userRepo := NewUserRepository(db)

	userService := NewUserService(userRepo)

	UserController := &UserController{
		Service: userService,
	}

	http.HandleFunc("/users/", UserController.HandleUsersRouter)
	fmt.Println("Started server on port 8080.")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Printf("Error starting server: %v\n", err)
	}
}
