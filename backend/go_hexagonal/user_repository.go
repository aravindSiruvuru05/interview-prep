package main

import "fmt"

type UserRepository struct {
	DB *DB
}

func NewUserRepository(db *DB) IUserRepository {
	return &UserRepository{
		DB: db,
	}
}

func (r *UserRepository) GetByID(id int) (*User, error) {
	user, ok := r.DB.users[id]
	r.DB.Hits++
	if !ok {
		return nil, fmt.Errorf("user with %d not found", id)
	}

	return user, nil
}
