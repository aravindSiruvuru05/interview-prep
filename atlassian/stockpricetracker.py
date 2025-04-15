from sortedcontainers import SortedDict 

class StockPriceTracker:
    def __init__(self):
        self.timeToPrice = {}
        self.priceCount = SortedDict()

    def update(self, timestamp, price):
        if timestamp in self.timeToPrice:
            old_price = self.timeToPrice[timestamp]
            self.priceCount[old_price] -= 1
            if self.priceCount[old_price] == 0:
                del self.priceCount[old_price]
        
        self.timeToPrice[timestamp] = price
        self.priceCount[price] = self.priceCount.get(price, 0) + 1

    def get_max(self):
        if not self.priceCount:
            return None
        max_price = self.priceCount.peekitem(-1)
        print(max_price)
        
        # Find one timestamp with that price
        for ts, price in self.timeToPrice.items():
            if price == max_price:
                return max_price, ts
        return max_price, None  # fallback

s = StockPriceTracker()
s.update("T1", 5)
s.update("T2", 2)
s.update("T3", 5)    # we use price to count to keep how many times that value is repeated so that we dont just remove 5 here from top as its twice

print(s.get_max())  # (5, "T1")
s.update("T1", 1)
print(s.get_max())  # (2, "T2")
s.update("T3", 7)
print(s.get_max())  # (7, "T3")
