package main

import (
	"encoding/json"
	"net/http"
	"strconv"
	"strings"
)

type UserController struct {
	Service *UserService
}

func (uc *UserController) HandleUsersRouter(w http.ResponseWriter, r *http.Request) {
	pathSegments := strings.Split(r.URL.Path, "/")
	if len(pathSegments) == 2 && pathSegments[1] == "users" {
		// uc.handleUsers(w, r)
		return
	}

	if len(pathSegments) == 3 && pathSegments[1] == "users" {
		uc.HandleGetUser(w, r)
		return
	}

	http.Error(w, "Not Found", http.StatusNotFound)
}

func (c *UserController) HandleGetUser(w http.ResponseWriter, req *http.Request) {
	// id := req.URL.Query().Get("id")
	pathSegments := strings.Split(req.URL.Path, "/")

	if len(pathSegments) != 3 || pathSegments[1] != "users" {
		http.Error(w, "Invalid URL path", http.StatusBadRequest)
		return
	}

	id := pathSegments[2]
	userId, _ := strconv.Atoi(id)
	user, err := c.Service.GetUserByID(userId)
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}
	userJson, err := json.Marshal(user)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.Write(userJson)
}
