# Multi-source BFS
# Use when: multiple starting points spread simultaneously (rotting oranges, walls and gates,
#           01 BFS with deque for 0-weight vs 1-weight edges)
# Key idea: seed queue with ALL sources at distance 0, then normal BFS

from collections import deque

def rotting_oranges(grid):
    """LeetCode 994 — minutes until all oranges rot. -1 if impossible."""
    m, n = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 2:
                queue.append((i, j, 0))
            elif grid[i][j] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    while queue:
        i, j, t = queue.popleft()
        minutes = t
        for di, dj in deltas:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                grid[ni][nj] = 2
                fresh -= 1
                queue.append((ni, nj, t + 1))

    return minutes if fresh == 0 else -1

def walls_and_gates(rooms):
    """LeetCode 286 — fill empty rooms with distance to nearest gate."""
    if not rooms:
        return
    m, n = len(rooms), len(rooms[0])
    INF = 2147483647
    queue = deque()

    for i in range(m):
        for j in range(n):
            if rooms[i][j] == 0:
                queue.append((i, j))

    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        i, j = queue.popleft()
        for di, dj in deltas:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and rooms[ni][nj] == INF:
                rooms[ni][nj] = rooms[i][j] + 1
                queue.append((ni, nj))

# 01 BFS: edges with weight 0 go to front, weight 1 go to back
def shortest_path_01_bfs(n, edges, start, end):
    graph = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((v, w))

    dist = [float('inf')] * n
    dist[start] = 0
    dq = deque([start])

    while dq:
        node = dq.popleft()
        for nei, w in graph[node]:
            new_dist = dist[node] + w
            if new_dist < dist[nei]:
                dist[nei] = new_dist
                if w == 0:
                    dq.appendleft(nei)
                else:
                    dq.append(nei)

    return dist[end] if dist[end] != float('inf') else -1

# --- Example Usage ---
grid = [
    [2, 1, 1],
    [1, 1, 0],
    [0, 1, 1],
]
print(rotting_oranges([row[:] for row in grid]))  # 4

rooms = [
    [2147483647, -1, 0, 2147483647],
    [2147483647, 2147483647, 2147483647, -1],
    [2147483647, -1, 2147483647, -1],
    [0, -1, 2147483647, 2147483647],
]
walls_and_gates(rooms)
print(rooms)

# 0-1 weighted graph: 0->1 (0), 0->2 (1), 1->3 (0), 2->3 (1)
edges = [(0, 1, 0), (0, 2, 1), (1, 3, 0), (2, 3, 1)]
print(shortest_path_01_bfs(4, edges, 0, 3))  # 0  (0 -> 1 -> 3)
