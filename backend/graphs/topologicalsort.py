from collections import defaultdict, deque

def kahn_topological_sort(V, edges):
    graph = defaultdict(list)
    in_degree = [0] * V
    
    for u, v, _ in edges:
        graph[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(V) if in_degree[i] == 0])
    topo_order = []
    
    while queue:
        node = queue.popleft()
        topo_order.append(node)
        
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(topo_order) == V:
        return topo_order
    else:
        return "Cycle detected"

V = 6
edges = [[0,1,2], [0,4,1], [4,5,4], [4,2,2], [1,2,3], [2,3,6], [5,3,1]]
print(kahn_topological_sort(V, edges)) 





# Function for DFS-based Topological Sort with cycle detection
def dfs_topological_sort(V, edges):
    graph = defaultdict(list)
    visited = set()
    path_visited = set()
    topo_order = []
    
    # Build the graph
    for u, v, _ in edges:
        graph[u].append(v)
    
    def dfs(node):
        visited.add(node)
        path_visited.add(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in path_visited:
                    return False
        
        path_visited.add(node)
        topo_order.append(node)
        return True
    
    # Perform DFS for all nodes
    for node in range(V):
        if not visited[node]:
            if not dfs(node):
                return "Cycle detected"
    
    # Return reverse of topo_order as DFS gives reversed topological order
    return topo_order[::-1]

# Example Usage
V = 6
edges = [[0,1,2], [0,4,1], [4,5,4], [4,2,2], [1,2,3], [2,3,6], [5,3,1]]
print(dfs_topological_sort(V, edges))  # Output: [0, 1, 4, 5, 2, 3]
