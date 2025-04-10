import heapq
from collections import defaultdict

def find_cheapest_price(n, flights, start, end, k):
    graph = defaultdict(list)
    
    # Build adjacency list
    for u, v, cost in flights:
        graph[u].append((v, cost))
    
    # (cost, current_node, stops_remaining)
    pq = [(0, start, k + 1)]
    
    while pq:
        cost, node, stops = heapq.heappop(pq)
        
        if node == end:
            return cost
        
        if stops > 0:
            for nei, price in graph[node]:
                heapq.heappush(pq, (cost + price, nei, stops - 1))
    
    return -1

n = 5
flights = [
    [0, 1, 100],
    [1, 2, 100],
    [0, 2, 500],
    [2, 3, 100],
    [3, 4, 100]
]
start = 0
end = 4
k = 3
