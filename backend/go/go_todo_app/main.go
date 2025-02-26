package main

import (
	"fmt"
)

type Person struct {
	name string
}

func (p *Person) changeName() {
	p.name = "asdf"
}

func main() {

	p := Person{
		name: "qqwer",
	}
	p.changeName()

	fmt.Println(p.name)
}
