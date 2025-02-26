from collections import deque, defaultdict

class Solution(object):
    def verticalTraversal(self, root):
        if not root:
            return []

        # Dictionary to store nodes based on vertical index
        result = defaultdict(list)
        min_col, max_col = 0, 0  # Track min and max column indices

        # BFS traversal queue (node, column index, row index)
        queue = deque([(root, 0, 0)])

        while queue:
            size = len(queue)
            level_nodes = []

            for _ in range(size):
                node, col, row = queue.popleft()
                level_nodes.append((row, node.val, col))  # Store row for sorting

                # Track min and max col indices
                min_col = min(min_col, col)
                max_col = max(max_col, col)

                # Add left and right children to the queue
                if node.left:
                    queue.append((node.left, col - 1, row + 1))
                if node.right:
                    queue.append((node.right, col + 1, row + 1))

            # Insert into result
            for row, val, col in level_nodes:
                result[col].append((row, val))

        # Construct result using min_col and max_col instead of sorting dict keys
        final_result = []
        for col in range(min_col, max_col + 1):
            final_result.append([val for _, val in sorted(result[col])])

        return final_result

# Example Usage
class TreeNode(object):
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Example Tree
root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

sol = Solution()
print(sol.verticalTraversal(root))  # Expected Output: [[9], [3, 15], [20], [7]]
