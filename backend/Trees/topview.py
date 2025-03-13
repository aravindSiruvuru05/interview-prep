from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def verticalView(self, root):
        if not root:
            return []

        column_table = {}  # Stores first encountered node for each column
        min_col, max_col = 0, 0
        queue = deque([(root, 0)])  # BFS queue (node, column index)

        while queue:
            node, col = queue.popleft()

            # Store the first node encountered at this column
            if col not in column_table:
                column_table[col] = node.val
                min_col = min(min_col, col)
                max_col = max(max_col, col)

            # Add child nodes to the queue
            if node.left:
                queue.append((node.left, col - 1))
            if node.right:
                queue.append((node.right, col + 1))

        # Extract the values in sorted column order
        return [column_table[col] for col in range(min_col, max_col + 1)]

# Example Usage
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

sol = Solution()
print(sol.verticalView(root))  # Expected Output: [9, 3, 20, 7]
