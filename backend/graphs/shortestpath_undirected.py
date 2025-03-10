import heapq

def dijkstra(n, edges):
    graph = {i: [] for i in range(1, n + 1)}
    
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    dist = {i: float('inf') for i in range(1, n + 1)}
    prev = {i: None for i in range(1, n + 1)}
    dist[1] = 0  
    
    pq = [(0, 1)]  
    
    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        
        for neighbor, weight in graph[node]:
            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))
    
    if dist[n] == float('inf'):
        return [-1]  
    path = []
    current = n
    while current is not None:
        path.append(current)
        current = prev[current]
    
    path.reverse()  
    return [dist[n]] + path  

n = 5
m = 6
edges = [[1, 2, 2], [2, 5, 5], [2, 3, 4], [1, 4, 1], [4, 3, 3], [3, 5, 1]]

result = dijkstra(n, edges)
print(result)  # [5, 1, 4, 3, 5]  // [totsldist, path... ]
