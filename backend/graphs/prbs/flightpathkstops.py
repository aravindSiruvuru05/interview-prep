# Given a directed graph represented as an adjacency list and two nodes start and end,
# print all paths from start to end with exactly k stops (which means the path should 
# have k + 1 nodes).

from collections import defaultdict

def find_paths_with_k_stops(graph, start, end, k):
    def dfs(node, path, stops_left):
        if stops_left < 0:
            return
        if node == end and stops_left == 0:
            print(path)
            return
        for neighbor in graph[node]:
            dfs(neighbor, path + [neighbor], stops_left - 1)

    dfs(start, [start], k)

# Example Usage
edges = [
    (0, 1),
    (1, 2),
    (0, 2),
    (2, 3),
    (3, 4)
]

graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)

start = 0
end = 4
k = 4  # 4 stops → 5 nodes in path

find_paths_with_k_stops(graph, start, end, k)
