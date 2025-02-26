package main

type CacheLayer struct {
	Users map[int]*User
}

var Cache = NewCache()

func NewCache() *CacheLayer {
	return &CacheLayer{
		Users: make(map[int]*User),
	}
}

func (c *CacheLayer) Get(key int) (*User, bool) {
	if u, ok := c.Users[key]; ok {
		return u, true
	}
	return nil, false
}

func (c *CacheLayer) Set(key int, val *User) bool {
	c.Users[key] = val
	return true
}
