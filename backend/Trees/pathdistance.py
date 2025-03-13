def find_distance(root, target, distance=0):
    """Finds the distance from root to the target node."""
    if not root:
        return -1  # Target not found
    if root.val == target:
        return distance
    
    return max(find_distance(root.left, target, distance + 1), 
               find_distance(root.right, target, distance + 1))

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def find_lca(root, node1, node2):
    """Finds the Lowest Common Ancestor (LCA) of two nodes."""
    if not root or root.val == node1 or root.val == node2:
        return root
    
    left_lca = find_lca(root.left, node1, node2)
    right_lca = find_lca(root.right, node1, node2)
    
    if left_lca and right_lca:
        return root  # This is the LCA
    
    return left_lca if left_lca else right_lca

def min_path_in_binary_tree(root, node1, node2):
    """Finds the shortest path between two nodes in a binary tree."""
    lca = find_lca(root, node1, node2)  # Step 1: Find LCA
    if not lca:
        return -1  # If LCA not found, nodes are not in tree

    dist1 = find_distance(lca, node1)  # Step 2: Distance from LCA to node1
    dist2 = find_distance(lca, node2)  # Step 2: Distance from LCA to node2

    return dist1 + dist2  # Step 3: Sum of distances

# --- Example Usage ---
# Constructing a sample binary tree
'''
         1
       /   \
      2     3
     / \   / \
    4   5 6   7
'''
root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)
root.left.left = TreeNode(4)
root.left.right = TreeNode(5)
root.right.left = TreeNode(6)
root.right.right = TreeNode(7)

# Find minimum path between nodes
print(min_path_in_binary_tree(root, 4, 5))  # Output: 2
print(min_path_in_binary_tree(root, 4, 6))  # Output: 4
print(min_path_in_binary_tree(root, 3, 4))  # Output: 3
print(min_path_in_binary_tree(root, 2, 4))  # Output: 1
