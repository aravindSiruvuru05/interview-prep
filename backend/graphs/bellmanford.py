# Bellman-Ford: shortest path with negative edge weights
# Use when: graph has negative weights OR you need to detect negative-weight cycles
# Time: O(VE)  |  Cannot use Dijkstra with negative weights

from collections import defaultdict

def bellman_ford(n, edges, start):
    """Returns shortest distances from start to all nodes. None if negative cycle reachable."""
    dist = {i: float('inf') for i in range(n)}
    dist[start] = 0

    # Relax all edges (n - 1) times
    for _ in range(n - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    # nth pass: if any edge still relaxes, negative cycle exists
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return None  # negative cycle

    return dist

def bellman_ford_with_path(n, edges, start, target):
    dist = {i: float('inf') for i in range(n)}
    prev = {i: None for i in range(n)}
    dist[start] = 0

    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u

    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            return [-1]

    if dist[target] == float('inf'):
        return [-1]

    path = []
    current = target
    while current is not None:
        path.append(current)
        current = prev[current]
    path.reverse()
    return [dist[target]] + path

# --- Example: graph with negative edge ---
n = 5
edges = [
    (0, 1, 6),
    (0, 2, 7),
    (1, 2, 8),
    (1, 3, 5),
    (1, 4, -4),   # negative edge
    (2, 3, -3),
    (2, 4, 9),
    (3, 1, -2),
    (4, 0, 2),
    (4, 3, 7),
]
start = 0
print(bellman_ford(n, edges, start))
# {0: 0, 1: 2, 2: 7, 3: 4, 4: -2}

print(bellman_ford_with_path(n, edges, start, 3))
# [4, 0, 1, 4, 3]

# --- Negative cycle example ---
cycle_edges = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]
print(bellman_ford(3, cycle_edges, 0))  # None
