package main

import "fmt"

func main1() {
	arr := []int{1, 2, 3, 4, 5}

	ch := make(chan int, 4)

	go func() {
		for el := range arr {
			ch <- el
		}
	}()

	for r := 0; r < len(arr); r++ {
		fmt.Println(<-ch)
	}

}
