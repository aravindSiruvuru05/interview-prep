# When to Use Which?
# Scenario	Use Algorithm
# DAG (Directed Acyclic Graph)	Topological Sort (O(V + E))   -  efficieant for DAGs
# General Graph with non-negative weights	Dijkstra’s Algorithm (O(E log V)) -- works for all directed undirected non negative but
# specially for directed graph topo method give beter time complexity as for evey node we are not rebalancing the nodes (happush (logN)) in pq in relaxation phase
# General Graph with negative weights	Bellman-Ford Algorithm (O(VE))



from collections import defaultdict, deque
import heapq

def dijkstra(n, edges):
    graph = {i: [] for i in range(1, n + 1)}
    
    for u, v, w in edges:
        graph[u].append((v, w))  
    
    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[1] = 0
    prev = {i: None for i in range(1, n + 1)}
    
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

# Example directed graph
n = 5
edges = [
    [1, 2, 2], [2, 3, 4], [1, 4, 1], [4, 3, 3], [3, 5, 1]
]

result = dijkstra(n, edges)
print(result)  # Output: [5, 1, 4, 3, 5]  // [totsldist, path... ]



def min_sum_path_dag(n, edges, start):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))

    # Step 1: Topological Sort
    indegree = [0] * n
    for u in graph:
        for v, _ in graph[u]:
            indegree[v] += 1
    
    queue = deque([i for i in range(n) if indegree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor, _ in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    
    # Step 2: Relax edges in topological order
    dist = [float('inf')] * n
    dist[start] = 0
    
    for u in topo_order:
        if dist[u] != float('inf'):
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

    return dist

# Example Usage
n = 6  # Number of nodes
edges = [(0, 1, 5), (0, 2, 3), (1, 3, 6), (1, 2, 2), (2, 4, 4), (2, 5, 2), (2, 3, 7), (3, 5, 1), (4, 5, 3)]
start = 0
print(min_sum_path_dag(n, edges, start))  # Output: Shortest path from start node to all others


