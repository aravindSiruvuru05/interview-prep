Print odd and even numbers in sequence using two goroutines and channels.



func main() {
	// even shuld be locked until odd finish and so on

	odd := make(chan, bool)
	even := make(chan, bool)
	curr := 1


	wg := sync.WaitGroup{}


	wg.Add(1)
	go func() {
		for el range odd {
			print(curr)
			curr += 1
			even <- true
		}
		wg.Done()
	}()
	wg.Add(1)
	go func() {
		for el range odd {
			print(curr)
			odd <- true
		}
		wg.Done()
	}()


	odd <- true
	wg.Wait()
	


}