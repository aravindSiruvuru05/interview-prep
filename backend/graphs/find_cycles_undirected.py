from collections import deque

def bfs_cycle_detection(graph, start):
    visited = set() 
    queue = deque([(start, None)])  
    visited.add(node)

    while queue:
        node, parent = queue.popleft()

        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, node))
                visited.add(node)

            
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


# The moment you decide **"I'll visit this node later"** (enqueue it), you should mark it as visited.
# Let's trace your code **step by step**.

# Graph:

# ```text
#     0
#    / \
#   1---2
# ```

# Edges:

# ```text
# 0-1
# 0-2
# 1-2
# ```

# ### Your code (mark visited after popping)

# Initially:

# ```python
# q = [(0, -1)]
# vis = {}
# ```

# ---

# ### Step 1

# Pop `0`:

# ```python
# curr = 0
# vis = {0}
# ```

# Neighbors of `0` are `1` and `2`.

# Both are not visited, so you enqueue both:

# ```python
# q = [(1, 0), (2, 0)]
# vis = {0}
# ```

# Notice that **1 and 2 are in the queue, but not in `vis` yet.**

# ---

# ### Step 2

# Pop `1`:

# ```python
# curr = 1
# vis = {0, 1}
# ```

# Neighbors of `1` are:

# * `0` → parent, ignore.
# * `2` → Is `2` in `vis`?

# No!

# Why? Because `2` is still waiting in the queue. It hasn't been popped yet.

# So your code says:

# ```python
# q.append((2, 1))
# ```

# Now the queue becomes:

# ```python
# [(2, 0), (2, 1)]
# ```

# 👉 **Node 2 is in the queue twice.**

# ---

# ### Correct approach (mark when enqueuing)

# Start:

# ```python
# q = [(0, -1)]
# vis = {0}
# ```

# Pop `0`:

# Neighbor `1`:

# ```python
# vis = {0, 1}
# q = [(1, 0)]
# ```

# Neighbor `2`:

# ```python
# vis = {0, 1, 2}
# q = [(1, 0), (2, 0)]
# ```

# Now pop `1`.

# When it checks neighbor `2`:

# ```python
# if 2 not in vis:
# ```

# This is **False**, because `2` was marked visited when it was enqueued.

# So it **does not enqueue `2` again**.

# ---

# ### The key idea

# There are two states:

# ```text
# Not discovered
#       ↓
# Enqueued  ← Mark visited HERE ✅
#       ↓
# Dequeued
#       ↓
# Processed
# ```

# The moment you decide **"I'll visit this node later"** (enqueue it), you should mark it as visited.

# Otherwise, another node may also discover it before it gets popped, causing duplicates in the queue.

# **Rule for BFS:**

# ```python
# vis.add(node)
# q.append(node)
# ```

# These two lines should always go together.
