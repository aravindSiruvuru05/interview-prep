package main

import (
	"encoding/json"
	"fmt"
)

type MyUser struct {
	Name  string `json:"name"`
	Email string `json:"email"`
	Age   int    `json:"age"`
}

func maiwen() {
	// Original struct
	user := MyUser{
		Name:  "Alice",
		Email: "alice@example.com",
		Age:   30,
	}

	// === JSON Marshal ===
	data, err := json.Marshal(user)
	if err != nil {
		fmt.Println("Marshal Error:", err)
		return
	}
	fmt.Println("Marshalled JSON:", string(data))

	// === JSON Unmarshal ===
	var newUser User
	err = json.Unmarshal(data, &newUser)
	if err != nil {
		fmt.Println("Unmarshal Error:", err)
		return
	}
	fmt.Println("Unmarshalled Struct:", newUser)
}
