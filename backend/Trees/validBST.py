

def validBST(root):

    def dfs(node, low, high):
        if not node:
            return True
        
        if low > node.val or node.val > high:
            return False

        left = dfs(node.left, low, node.val)
        right = dfs(node.right, node.val, high)
        
        return left and right

    dfs(root, float('-inf'), float('inf'))