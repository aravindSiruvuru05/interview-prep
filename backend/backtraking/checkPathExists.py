


def checkPathExists(mat):
    m, n = len(mat), len(mat[0])
    path = []
    visited = set()
    delta = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    def dfs(i, j):
        if i == m - 1 and j == n-1:
            path.append((i, j))
            return True

        path.append((i, j))
        visited.add((i, j))
        for dx, dy in delta:
            k, l = i + dx , j + dy
            if 0 <= k  < m and 0 <= l < n and  (k, l) not in visited and mat[k][l] != 0:
                if dfs(k, l):
                    return True
        path.pop()
        return False

    dfs(0, 0)
    return path

matrix = [
    [1, 1, 0, 1],
    [0, 1, 1, 0],
    [1, 0, 1, 1],
    [1, 1, 1, 1]
]

print(checkPathExists(matrix))  