package main

import (
	"fmt"
	"reflect"
)

type KUser struct {
	Name string
	Age  int
}

type Product struct {
	ID    int
	Price float64
}

func maiasn() {
	ch := make(chan interface{})

	go func() {
		ch <- KUser{Name: "Alice", Age: 30}
		ch <- Product{ID: 101, Price: 19.99}
		close(ch)
	}()

	for msg := range ch {
		// Reflection to detect type dynamically
		t := reflect.TypeOf(msg)
		fmt.Println("Received type:", t.Name())

		// Type assertions
		switch v := msg.(type) {
		case KUser:
			fmt.Printf("KUser: %s (Age: %d)\n", v.Name, v.Age)
		case Product:
			fmt.Printf("Product ID: %d, Price: %.2f\n", v.ID, v.Price)
		default:
			fmt.Println("Unknown type")
		}
	}
}
