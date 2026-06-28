# LeetCode 269 — Alien Dictionary (topological sort on character precedence graph)

from collections import deque, defaultdict

def alien_order(words):
    """Return lexicographic order of alien alphabet, or '' if invalid."""
    graph = defaultdict(set)
    indegree = {c: 0 for word in words for c in word}

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]
        if len(w1) > len(w2) and w1[:len(w2)] == w2:
            return ''  # invalid: prefix longer word comes first
        for a, b in zip(w1, w2):
            if a != b:
                if b not in graph[a]:
                    graph[a].add(b)
                    indegree[b] += 1
                break

    queue = deque([c for c in indegree if indegree[c] == 0])
    order = []

    while queue:
        c = queue.popleft()
        order.append(c)
        for nei in graph[c]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    return ''.join(order) if len(order) == len(indegree) else ''

# --- Example Usage ---
words = ["wrt", "wrf", "er", "ett", "rftt"]
print(alien_order(words))  # "wertf"

words2 = ["z", "x"]
print(alien_order(words2))  # "zx"

words3 = ["abc", "ab"]
print(alien_order(words3))  # "" (invalid)
