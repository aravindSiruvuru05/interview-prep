from collections import deque

# Word Search in a Matrix (Backtracking)
# Given an m x n board and a word, check if the word exists in the grid.

# You can move up, down, left, and right.
# You cannot reuse the same cell more than once in a single search.

def exist(board, word):
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])
    delta = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(r, c, index):
        if index == len(word):  # Found the word
            return True

        temp, board[r][c] = board[r][c], "#"
        found = False

        for x, y in delta:
            xx, yy = r + x, c + y
            
            if 0 <= xx < rows and 0 <= yy < cols and board[xx][yy] != word[index]:
                if dfs(xx, yy, index + 1):
                    found = True
                    break 
        board[r][c] = temp

        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0): 
                return True

    return False

# Example Usage
board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]
word = "ABCCED"

print(exist(board, word))  # Output: True


# BFS

def exist(board, word):
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])
    delta = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def bfs(r, c):
        queue = deque([(r, c, 0)])  
        visited = set()  

        while queue:
            x, y, idx = queue.popleft()
            if idx == len(word):
                return True
            if board[x][y] != word[idx]:
                continue

            visited.add((x, y))
            for dx, dy in delta:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                    queue.append((nx, ny, idx + 1))

        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and bfs(r, c):
                return True

    return False

board = [
    ['A', 'B', 'C', 'E'],
    ['S', 'F', 'C', 'S'],
    ['A', 'D', 'E', 'E']
]
word = "ABCCED"

print(exist(board, word)) 
