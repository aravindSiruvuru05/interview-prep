package main

import "fmt"

type UserService struct {
	Repo IUserRepository
}

func NewUserService(userRepo IUserRepository) *UserService {
	return &UserService{
		Repo: userRepo,
	}
}

func (s *UserService) GetUserByID(id int) (*User, error) {

	if user, ok := Cache.Get(id); ok {
		fmt.Println("returned from cache")
		return user, nil
	}
	user, err := s.Repo.GetByID(id)
	Cache.Set(id, user)
	if err != nil {
		return nil, err
	}

	return user, nil
}
