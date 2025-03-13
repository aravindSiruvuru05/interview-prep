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

from collections import deque, defaultdict

def shortest_path_unweighted(graph, source, target):
    """Finds the shortest path between two nodes in an undirected, unweighted graph using BFS."""
    if source == target:
        return 0  # Source is the same as target
    
    queue = deque([(source, 0)])  # (node, distance)
    visited = set([source])  # Track visited nodes

    while queue:
        node, dist = queue.popleft()  # Get the current node and distance

        for neighbor in graph[node]:  # Explore neighbors
            if neighbor == target:
                return dist + 1  # Found the target, return shortest path length
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # No path found

# --- Example Usage ---
graph = defaultdict(list)

# Undirected Graph (Adjacency List)
graph[0] = [1, 2]
graph[1] = [0, 3, 2]
graph[2] = [0, 1, 4, 5]
graph[3] = [1, 5, 4]
graph[4] = [2, 3, 5]
graph[5] = [2, 3, 4]

source, target = 0, 5
print(shortest_path_unweighted(graph, source, target))  # Output: 2 (0 -> 2 -> 5)
