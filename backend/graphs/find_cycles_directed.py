from collections import deque

def isCyclicInDirectedGraph(adj) -> bool :
    indeg = [0] * len(adj)
    
    for nbr in adj:
        for n in nbr:
            indeg[n] += 1
    q = deque([])
    
    for i in range(len(indeg)):
        if indeg[i] == 0:
            q.append(i)
    stk = []
    while q:
        curr = q.popleft()
        stk.append(curr)
        for nbr in adj[curr]:
            indeg[nbr] -= 1
            if indeg[nbr] == 0:
                q.append(nbr)
    
    return len(stk) != len(adj)



# noting but topo logical sort , for topo sort we use one stak to push once its getting removed from path_vis
def dfs(v, graph, visited, path_vis):
    visited.add(v)
    path_vis.add(v)
    
    for neighbor in graph[v]:
        if neighbor not in visited:
            if dfs(neighbor, graph, visited, path_vis):
                return True
        elif neighbor in path_vis:  
            return True
    
    path_vis.remove(v)
    return False

def detect_cycle(graph):
    visited = set()  
    path_vis = set()  
    for node in graph:
        if node not in visited:
            if dfs(node, graph, visited, path_vis):
                return True
    return False


graph = {
    0: [1],
    1: [2],
    2: [0],  
    3: [4],
    4: []
}

print(detect_cycle(graph))  
