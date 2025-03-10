from collections import defaultdict, deque

#  topological sort along with cyccle detection
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



def dfs(v, graph, visited, stack):
    visited[v] = True
    
    for neighbor in graph[v]:
        if not visited[neighbor]:
            dfs(neighbor, graph, visited, stack)
    stack.append(v)

def topological_sort(graph):
    visited = {node: False for node in graph} 
    stack = [] 
    
    for node in graph:
        if not visited[node]:
            dfs(node, graph, visited, stack)

    return stack[::-1]
graph = {
    0: [1],
    1: [2],
    2: [3],
    3: []
}

top_order = topological_sort(graph)
print(top_order)  # Output: [0, 1, 2, 3]



# topological sort along with if cycle detected return []
def dfs_topological_sort(V, edges):
    graph = defaultdict(list)
    visited = set()
    path_visited = set()
    topo_order = []
    
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
    
    for node in range(V):
        if not visited[node]:
            if not dfs(node):
                return "Cycle detected"
    
    return topo_order[::-1]

V = 6
edges = [[0,1,2], [0,4,1], [4,5,4], [4,2,2], [1,2,3], [2,3,6], [5,3,1]]
print(dfs_topological_sort(V, edges))  # Output: [0, 1, 4, 5, 2, 3]
