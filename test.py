from sortedcontainers import SortedDict

class StockTrackerWithHeap:
    
    def __init__(self):
        self.priceToCount = SortedDict()
        self.timeToPrice = {}

    def update(self, time, price):
        if time in self.timeToPrice:
            oldPrice = self.timeToPrice[time]
            self.priceToCount[oldPrice] -= 1
            if self.priceToCount[oldPrice] == 0:
                del self.priceToCount[oldPrice]

        self.timeToPrice[time] = price
        self.priceToCount[price] = self.priceToCount.get(price, 0) + 1
    
    def get_max(self):
        if not self.priceToCount:
            return None
        maxPrice = self.priceToCount.peekitem(-1)[0]
        
        return maxPrice
        








         

s = StockTrackerWithHeap()
s.update("T1", 5)
s.update("T4", 5)
s.update("T2", 2)

s.update("T3", 7)    # we use price to count to keep how many times that value is repeated so that we dont just remove 5 here from top as its twice

print(s.get_max())  # (5, "T1")
s.update("T1", 1)
print(s.get_max())  # (2, "T2")
s.update("T3", 6)
print(s.get_max())  # (7, "T3")

