from collections import deque

def bfs_cycle_detection(graph, start):
    visited = set() 
    queue = deque([(start, None)])  
    while queue:
        node, parent = queue.popleft()

        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, node))
            
            elif neighbor != parent:  # except its parent non of the elements shuld be in visited set
                return True
    return False

def detect_cycle(graph):
    visited = set()
    for node in graph:
        if node not in visited:
            if bfs_cycle_detection(graph, node):
                return True
    return False


graph_with_cycle = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]  
}

graph_without_cycle = {
    0: [1],
    1: [0, 2],
    2: [1]  
}

print(detect_cycle(graph_with_cycle))  
print(detect_cycle(graph_without_cycle))  


def dfs(v, graph, visited, parent):
    visited.add(v)
    
    for neighbor in graph[v]:
        if neighbor not in visited:
            if dfs(neighbor, graph, visited, v):
                return True
        elif neighbor != parent:  
            return True
    
    return False

def detect_cycle(graph):
    visited = set()  
    
    for node in graph:
        if node not in visited:
            if dfs(node, graph, visited, None):  
                return True
    
    return False


graph_with_cycle = {
    0: [1, 2],
    1: [0, 2],
    2: [0, 1]  
}

graph_without_cycle = {
    0: [1],
    1: [0, 2],
    2: [1]  
}

print(detect_cycle(graph_with_cycle))  
print(detect_cycle(graph_without_cycle))  
