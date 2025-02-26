# Word Search in a Matrix (Backtracking)
# Given an m x n board and a word, check if the word exists in the grid.

# You can move up, down, left, and right.
# You cannot reuse the same cell more than once in a single search.

def exist(board, word):
    if not board or not board[0]:
        return False

    rows, cols = len(board), len(board[0])

    def dfs(r, c, index):
        if index == len(word):  # Found the word
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[index]:
            return False

        # Mark the cell as visited temporarily
        temp, board[r][c] = board[r][c], "#"

        # Explore 4 possible directions (up, down, left, right)
        found = (dfs(r+1, c, index+1) or 
                 dfs(r-1, c, index+1) or 
                 dfs(r, c+1, index+1) or 
                 dfs(r, c-1, index+1))

        # Restore the cell after backtracking
        board[r][c] = temp

        return found

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0] and dfs(r, c, 0):  # Start search from matching letter
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
