# LeetCode 802 — Find Eventual Safe States (nodes that cannot reach a cycle)
# Pattern: reverse graph + nodes with out-degree 0 are safe, peel like topological sort

from collections import deque, defaultdict

def eventual_safe_nodes(graph):
    n = len(graph)
    reverse = defaultdict(list)
    out_degree = [0] * n

    for u in range(n):
        out_degree[u] = len(graph[u])
        for v in graph[u]:
            reverse[v].append(u)

    queue = deque([i for i in range(n) if out_degree[i] == 0])
    safe = []

    while queue:
        node = queue.popleft()
        safe.append(node)
        for parent in reverse[node]:
            out_degree[parent] -= 1
            if out_degree[parent] == 0:
                queue.append(parent)

    return sorted(safe)

# --- Example Usage ---
graph = [[1, 2], [2, 3], [5], [0], [5], [], []]
print(eventual_safe_nodes(graph))  # [2, 4, 5, 6]

graph2 = [[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []]
print(eventual_safe_nodes(graph2))  # [4]
