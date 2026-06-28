# Union-Find (Disjoint Set Union)
# Use when: dynamic connectivity, cycle detection in undirected graph (Kruskal's MST),
#           counting connected components, redundant connection
# Time: nearly O(1) per op with path compression + union by rank

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def count_components(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.components

def has_cycle_undirected(n, edges):
    """Returns True if adding edges creates a cycle (undirected)."""
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return True
    return False

def redundant_connection(edges):
    """First edge that creates a cycle. LeetCode 684 pattern."""
    n = len(edges)
    uf = UnionFind(n + 1)
    for u, v in edges:
        if not uf.union(u, v):
            return [u, v]
    return []

# --- Example Usage ---
edges = [[1, 2], [1, 3], [2, 3]]
print(has_cycle_undirected(4, edges))  # True

edges2 = [[1, 2], [2, 3], [1, 3]]
print(redundant_connection(edges2))  # [1, 3]

print(count_components(5, [[0, 1], [1, 2], [3, 4]]))  # 2
