# LeetCode 417 — Pacific Atlantic Water Flow (multi-source DFS/BFS from borders)

from collections import deque

def pacific_atlantic(heights):
    if not heights:
        return []
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def dfs(i, j, visited):
        visited.add((i, j))
        for di, dj in deltas:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in visited:
                if heights[ni][nj] >= heights[i][j]:
                    dfs(ni, nj, visited)

    for j in range(n):
        dfs(0, j, pacific)
        dfs(m - 1, j, atlantic)
    for i in range(m):
        dfs(i, 0, pacific)
        dfs(i, n - 1, atlantic)

    return sorted(pacific & atlantic)

def pacific_atlantic_bfs(heights):
    if not heights:
        return []
    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()
    deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def bfs(queue, visited):
        while queue:
            i, j = queue.popleft()
            visited.add((i, j))
            for di, dj in deltas:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and (ni, nj) not in visited:
                    if heights[ni][nj] >= heights[i][j]:
                        queue.append((ni, nj))

    p_queue = deque((i, 0) for i in range(m)) + deque((0, j) for j in range(1, n))
    a_queue = deque((i, n - 1) for i in range(m)) + deque((m - 1, j) for j in range(n - 1))
    bfs(p_queue, pacific)
    bfs(a_queue, atlantic)

    return sorted(pacific & atlantic)

# --- Example Usage ---
heights = [
    [1, 2, 2, 3, 5],
    [3, 2, 3, 4, 4],
    [2, 4, 5, 3, 1],
    [6, 7, 1, 4, 5],
    [5, 1, 1, 2, 4],
]
print(pacific_atlantic(heights))  # [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
