# Bidirectional BFS
# Use when: shortest path between two nodes in unweighted graph (Word Ladder, etc.)
# Key idea: BFS from both start and end; stop when frontiers meet
# Often faster than single-source BFS on large sparse graphs

from collections import deque, defaultdict

def bidirectional_bfs(graph, start, end):
    """Returns shortest path length in unweighted directed/undirected graph."""
    if start == end:
        return 0

    front = {start}
    back = {end}
    visited = {start: 0, end: 0}
    depth = 0

    while front:
        depth += 1
        next_front = set()
        for node in front:
            for nei in graph[node]:
                if nei in back:
                    return depth
                if nei not in visited:
                    visited[nei] = depth
                    next_front.add(nei)
        front = next_front

        # swap to expand smaller frontier (optimization)
        if len(front) > len(back):
            front, back = back, front

    return -1

def word_ladder(begin_word, end_word, word_list):
    """LeetCode 127 — shortest transformation sequence length."""
    word_set = set(word_list)
    if end_word not in word_set:
        return 0

    def neighbors(word):
        for i in range(len(word)):
            for c in 'abcdefghijklmnopqrstuvwxyz':
                nxt = word[:i] + c + word[i + 1:]
                if nxt in word_set:
                    yield nxt

    front = {begin_word}
    back = {end_word}
    visited = {begin_word, end_word}
    steps = 1

    while front:
        steps += 1
        next_front = set()
        for word in front:
            for nxt in neighbors(word):
                if nxt in back:
                    return steps
                if nxt not in visited:
                    visited.add(nxt)
                    next_front.add(nxt)
        front = next_front
        if len(front) > len(back):
            front, back = back, front

    return 0

def build_graph(edges, undirected=True):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if undirected:
            graph[v].append(u)
    return graph

# --- Example Usage ---
edges = [(0, 1), (1, 2), (2, 3), (0, 3), (3, 4)]
graph = build_graph(edges)
print(bidirectional_bfs(graph, 0, 4))  # 2  (0 -> 3 -> 4)

begin = "hit"
end = "cog"
words = ["hot", "dot", "dog", "lot", "log", "cog"]
print(word_ladder(begin, end, words))  # 5
