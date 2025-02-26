# Comes under DFS

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    # 🔹 Inorder Traversal (Left, Root, Right)
    def inorder(self, node):
        if node:
            self.inorder(node.left)
            print(node.val, end=" ")  # Process root
            self.inorder(node.right)

    # 🔹 Preorder Traversal (Root, Left, Right)
    def preorder(self, node):
        if node:
            print(node.val, end=" ")  # Process root
            self.preorder(node.left)
            self.preorder(node.right)

    # 🔹 Postorder Traversal (Left, Right, Root)
    def postorder(self, node):
        if node:
            self.postorder(node.left)
            self.postorder(node.right)
            print(node.val, end=" ")  # Process root

    #  Iterative

    def preorderItr(self):

        stack = [self.root]

        while stack:
            node = stack.pop()
            print(node.val, end=' ')
            if node.right: stack.append(node.right)
            if node.left: stack.append(node.left)
    
    def inorderIts(self):
        stack = []
        curr = root
        while stack or curr:
            while curr:  # Push all left children
                stack.append(curr)
                curr = curr.left
            curr = stack.pop()  # Process node
            print(curr.val, end=" ")
            curr = curr.right  # Move to right child

    def postorderItr(root):
        if not root:
            return
        stack1, stack2 = [root], []
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            if node.left:
                stack1.append(node.left)
            if node.right:
                stack1.append(node.right)
        while stack2:
            print(stack2.pop().val, end=" ")    


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

# 🔹 Run Traversals
print("Inorder Traversal: ", end="")
tree.inorder(tree.root)
print("\nPreorder Traversal: ", end="")
tree.preorder(tree.root)
print("\nPostorder Traversal: ", end="")
tree.postorder(tree.root)

print("\nPreorder Itrr Traversal: ", end="")
tree.preorderItr()


# Traversal Type	Time Complexity	Space Complexity (Recursion)
# Inorder	O(N)	O(H) (H = height of tree)
# Preorder	O(N)	O(H)
# Postorder	O(N)	O(H)