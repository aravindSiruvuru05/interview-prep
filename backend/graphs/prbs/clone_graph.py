# LeetCode 133 — Clone Graph

from collections import deque

class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

def clone_graph_dfs(node):
    if not node:
        return None
    clones = {}

    def dfs(original):
        if original in clones:
            return clones[original]
        copy = Node(original.val)
        clones[original] = copy
        for nei in original.neighbors:
            copy.neighbors.append(dfs(nei))
        return copy

    return dfs(node)

def clone_graph_bfs(node):
    if not node:
        return None
    clones = {node: Node(node.val)}
    queue = deque([node])

    while queue:
        curr = queue.popleft()
        for nei in curr.neighbors:
            if nei not in clones:
                clones[nei] = Node(nei.val)
                queue.append(nei)
            clones[curr].neighbors.append(clones[nei])

    return clones[node]

# --- Example Usage ---
# adj = [[2, 4], [1, 3], [2, 4], [1, 3]]
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)
n4 = Node(4)
n1.neighbors = [n2, n4]
n2.neighbors = [n1, n3]
n3.neighbors = [n2, n4]
n4.neighbors = [n1, n3]

cloned = clone_graph_dfs(n1)
print(cloned.val)  # 1
print([n.val for n in cloned.neighbors])  # [2, 4]
