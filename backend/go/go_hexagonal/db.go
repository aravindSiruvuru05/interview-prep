package main

import "fmt"

type DB struct {
	Hits  int
	users map[int]*User
}

func NewDB() *DB {
	users := make(map[int]*User)
	for i := range 1000 {
		users[i+1] = &User{
			ID:   i + 1,
			Name: fmt.Sprintf("%d - Name", i),
		}
	}
	return &DB{
		users: users,
		Hits:  0,
	}
}
