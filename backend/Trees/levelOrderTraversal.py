from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    # 🔹 Level Order Traversal (BFS)
    def level_order(self, node):
        if not node:
            return
        
        queue = deque([node])  # Use a queue to process nodes level by level
        
        while queue:
            current = queue.popleft()  # Remove front node
            print(current.val, end=" ")  # Process current node
            
            if current.left:
                queue.append(current.left)  # Add left child to queue
            if current.right:
                queue.append(current.right)  # Add right child to queue

    # If you want to print each level on a new line, modify the code to track levels:
    def level_order_by_levels(self, node):
        if not node:
            return
        
        queue = deque([node])
        
        while queue:
            level_size = len(queue)  # Number of nodes in current level
            for _ in range(level_size):
                current = queue.popleft()
                print(current.val, end=" ")  
                if current.left:
                    queue.append(current.left)
                if current.right:
                    queue.append(current.right)
            print()  # New line after each level

# 🔹 Example Tree:
#       1
#      / \
#     2   3
#    / \   \
#   4   5   6

root = TreeNode(1, 
        TreeNode(2, TreeNode(4), TreeNode(5)), 
        TreeNode(3, None, TreeNode(6))
    )

tree = BinaryTree(root)

# 🔹 Run Level Order Traversal
print("Level Order Traversal: ", end="")
tree.level_order(tree.root)

print("Level Order (Each Level in New Line):")
tree.level_order_by_levels(tree.root)


# 🔹 Complexity Analysis
# Traversal Type	Time Complexity	Space Complexity
# Level Order	   O(N)  	O(N) (Queue stores nodes)