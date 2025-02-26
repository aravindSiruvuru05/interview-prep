package main

type User struct {
	ID   int    `json:"id"`
	Name string `json:"name"`
}

type IUserRepository interface {
	GetByID(id int) (*User, error)
}
