# Core BFS / DFS templates for graphs and grids
# Use when: explore connected region, clone graph, path existence, flood fill

from collections import deque, defaultdict

# --- Graph DFS (recursive) ---
def dfs_graph(node, graph, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_graph(neighbor, graph, visited)

def count_components_graph(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    count = 0
    for node in range(n):
        if node not in visited:
            dfs_graph(node, graph, visited)
            count += 1
    return count

# --- Graph BFS ---
def bfs_graph(start, graph):
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order

# --- Clone Graph (LeetCode 133 pattern) ---
class Node:
    def __init__(self, val=0, adj=None):
        self.val = val
        self.adj = adj if adj is not None else []

class Solution:
    def cloneGraph(self, node):
        if not node:
            return None

        oldToNew = {}

        def dfs(node):
            if node in oldToNew:
                return oldToNew[node]

            copy = Node(node.val)
            oldToNew[node] = copy

            for nbr in node.adj:
                copy.adj.append(dfs(nbr))

            return copy

        return dfs(node)

# --- Grid: Number of Islands (LeetCode 200) ---
def num_islands(grid):
    if not grid:
        return 0
    m, n = len(grid), len(grid[0])
    count = 0

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or grid[i][j] != '1':
            return
        grid[i][j] = '0'

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for a, b in directions:
            dfs(i + a, j + b)


    def bfs(i, j):
        q = deque()
        q.append((i, j))

        directions = [(1,0), (-1, 0), (0, 1), (0, -1)]

        while q:
            i, j = q.popleft()
            grid[i][j] = '0'

            for a, b in directions:
                x, y = i+a, j+b
                if x < 0 or x > rows - 1 or y < 0 or  y > cols -1 or grid[x][y] == '0':
                    continue
                q.append((x, y))




    for i in range(m):
        for j in range(n):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count



# --- Grid: Flood Fill (LeetCode 733) ---
def flood_fill(image, sr, sc, color):
    original = image[sr][sc]
    if original == color:
        return image
    m, n = len(image), len(image[0])

    def dfs(i, j):
        if i < 0 or i >= m or j < 0 or j >= n or image[i][j] != original:
            return
        image[i][j] = color
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)

    dfs(sr, sc)
    return image

# --- Grid BFS: shortest path in unweighted matrix ---
def shortest_path_grid(grid, start, end):
    m, n = len(grid), len(grid[0])
    if grid[start[0]][start[1]] == 1 or grid[end[0]][end[1]] == 1:
        return -1
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    queue = deque([(start[0], start[1], 0)])
    visited = {start}
    while queue:
        i, j, dist = queue.popleft()
        if (i, j) == end:
            return dist
        for di, dj in deltas:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in visited and grid[ni][nj] == 0:
                visited.add((ni, nj))
                queue.append((ni, nj, dist + 1))
    return -1

# --- Example Usage ---

# dfs_graph — visits all nodes reachable from start
# graph: 0—1—2    3—4  (two components; DFS from 0 visits {0,1,2})
graph_dfs = defaultdict(list)
edges_dfs = [[0, 1], [1, 2], [3, 4]]
for u, v in edges_dfs:
    graph_dfs[u].append(v)
    graph_dfs[v].append(u)
visited_dfs = set()
dfs_graph(0, graph_dfs, visited_dfs)
print(sorted(visited_dfs))  # [0, 1, 2]

# count_components_graph
# n=5, edges connect {0,1,2} and {3,4} → 2 components
print(count_components_graph(5, [[0, 1], [1, 2], [3, 4]]))  # 2

# bfs_graph — BFS visit order from start node
# graph: 0—1—3
#        |   |
#        2   4
graph_bfs = defaultdict(list)
edges_bfs = [[0, 1], [0, 2], [1, 3], [3, 4]]
for u, v in edges_bfs:
    graph_bfs[u].append(v)
    graph_bfs[v].append(u)
print(bfs_graph(0, graph_bfs))  # [0, 1, 2, 3, 4]

# clone_graph — adjacency list [[2,4],[1,3],[2,4],[1,3]] for nodes 1,2,3,4
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n1.adj = [n2, n4]
n2.adj = [n1, n3]
n3.adj = [n2, n4]
n4.adj = [n1, n3]
cloned = clone_graph(n1)
print(cloned.val)  # 1
print([n.val for n in cloned.adj])  # [2, 4]

# num_islands — '1' = land, '0' = water
grid = [
    ['1', '1', '0', '0'],
    ['1', '1', '0', '0'],
    ['0', '0', '1', '0'],
]
print(num_islands([row[:] for row in grid]))  # 2

# flood_fill — sr=1, sc=1, new color=2
image = [[1, 1, 1], [1, 1, 0], [1, 0, 1]]
print(flood_fill([row[:] for row in image], 1, 1, 2))
# [[2, 2, 2], [2, 2, 0], [2, 0, 1]]

# shortest_path_grid — 0=walkable, 1=blocked; start (0,0) → end (2,2)
matrix = [
    [0, 0, 0],
    [1, 1, 0],
    [0, 0, 0],
]
print(shortest_path_grid(matrix, (0, 0), (2, 2)))  # 4
