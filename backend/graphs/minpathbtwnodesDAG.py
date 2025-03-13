from collections import defaultdict, deque

def topological_sort(graph, V):
    """Returns a topological order of the graph."""
    in_degree = {i: 0 for i in range(V)}  # Track in-degrees of nodes
    for u in graph:
        for v, _ in graph[u]:  # Only look at destinations
            in_degree[v] += 1

    # Queue for nodes with in-degree 0
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    topo_order = []

    while queue:
        node = queue.popleft()
        topo_order.append(node)
        for neighbor, _ in graph[node]:  # Decrease in-degree for neighbors
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return topo_order

def shortest_path_DAG_weighted(graph, V, source, target):
    """Finds the shortest path from source to target in a DAG."""
    topo_order = topological_sort(graph, V)
    
    # Initialize distances
    dist = {i: float('inf') for i in range(V)}
    dist[source] = 0

    # Relax edges in topological order
    for u in topo_order:
        if dist[u] != float('inf'):
            for v, weight in graph[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight

    return dist[target] if dist[target] != float('inf') else -1  # Return -1 if unreachable

# --- Example Usage ---
graph = defaultdict(list)

# DAG with weighted edges
graph[0].append((1, 5))
graph[0].append((2, 3))
graph[1].append((3, 6))
graph[1].append((2, 2))
graph[2].append((4, 4))
graph[2].append((5, 2))
graph[2].append((3, 7))
graph[3].append((5, 1))
graph[3].append((4, -1))
graph[4].append((5, -2))

V = 6  # Number of nodes

source, target = 0, 5
print(shortest_path_DAG(graph, V, source, target))  # Output: 6 (shortest path from 0 to 5)


from collections import deque, defaultdict

def shortest_path_unweighted(graph, source, target):
    """Finds the shortest path between two nodes in an unweighted graph using BFS."""
    if source == target:
        return 0  # Source is the same as target
    
    queue = deque([(source, 0)])  # (node, distance)
    visited = set([source])  # Track visited nodes

    while queue:
        node, dist = queue.popleft()

        for neighbor in graph[node]:
            if neighbor == target:
                return dist + 1  # Found target, return distance
            
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))

    return -1  # No path found

# --- Example Usage ---
graph = defaultdict(list)

# Unweighted graph (Adjacency List)
graph[0] = [1, 2]
graph[1] = [0, 3, 2]
graph[2] = [0, 1, 4, 5]
graph[3] = [1, 5, 4]
graph[4] = [2, 3, 5]
graph[5] = [2, 3, 4]

source, target = 0, 5
print(shortest_path_unweighted(graph, source, target))  # Output: 2 (0 -> 2 -> 5)
