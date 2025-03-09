package main

import "fmt"

func main() {

	c := NewCoffee()

	mc := &Mocha{
		b:     c,
		price: 20,
	}
	fmt.Println(mc.getPrice())

	card1 := &Cardamom{
		b:     mc,
		price: 2,
	}
	fmt.Println(card1.getPrice())

	card2 := &Cardamom{
		b:     c,
		price: 4,
	}

	fmt.Println(card2.getPrice())

}
