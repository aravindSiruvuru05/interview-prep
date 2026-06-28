# Cycle Detection & Topological Sort

**Repo:** `find_cycles_undirected.py`, `find_cycles_directed.py`, `topologicalsort.py`, `unionfind.py`  
**Overview:** [graphs/README.md](README.md) links here for all cycle/topo detail.

---

## Important: Not the same thing

| Question | What you need |
|----------|----------------|
| "Give me a valid course order" | Topological sort |
| "Can all courses be finished?" | Cycle detection (or Kahn: `len(order) < V`) |
| Both | Kahn's algorithm does **both** in one pass |

**Interview rule:**

```text
Topological sort exists  ⇔  Directed graph has NO cycle  ⇔  Graph is a DAG
```

---

## What is Topological Sort?

A topological ordering lists vertices so that for **every** directed edge `u → v`, **`u` appears before `v`**.

**Real life:**

```text
Wake Up → Brush → Breakfast → Office
```

**Graph:**

```text
0 → 1
↓
2
```

Valid orders: `0 1 2` or `0 2 1` (both respect all edges).

A topological sort exists **only** on a **DAG** (Directed Acyclic Graph). If there is a cycle, no valid ordering exists.

---

## All algorithms at a glance (don't confuse them)

| Algorithm | Graph | BFS/DFS | Topological sort? | Cycle detection? |
|-----------|-------|---------|-------------------|------------------|
| **DFS/BFS + parent check** | **Undirected** | Both | ❌ No | ✅ Yes (`nbr in visited` and `nbr != parent`) |
| **Union-Find** | **Undirected** | — | ❌ No | ✅ Yes (`union(u,v)` fails → cycle edge) |
| **Kahn's algorithm** | **Directed** | BFS | ✅ Yes | ✅ Yes (`len(topo) < V`) |
| **DFS + `visited` + `path_vis`** | **Directed** | DFS | ❌ No | ✅ Yes only (`nbr in path_vis`) |
| **DFS + stack (postorder)** | **Directed** | DFS | ✅ Yes | ❌ Not alone — add `path_vis` for cycles |

```text
UNDIRECTED — cycle only (no topo sort):
  DFS/BFS + parent check  →  find_cycles_undirected.py
  Union-Find              →  unionfind.py (Redundant Connection)

DIRECTED — topological sort (2 ways):
  1. Kahn's (BFS + indegree)
  2. DFS postorder + reverse stack

DIRECTED — cycle detection only:
  DFS + visited + path_vis  →  find_cycles_directed.py

Kahn's = topo + cycle in one (directed).
DFS path_vis = cycle only (directed).
DFS postorder = topo only (directed; add path_vis for cycles).
```

---

## 1. Kahn's Algorithm ✅ Topological Sort + Cycle Detection

**Is a topological sort algorithm.** Uses **BFS + indegree**.

- Produces a topological ordering if the graph is a DAG
- If it cannot order **all** vertices → cycle exists

### Intuition

Repeatedly remove nodes with **indegree = 0** (nothing blocking them). Each removal frees dependents.

```text
In a cycle, every node depends on another node in the cycle —
none can be "first" (indegree 0), so Kahn's gets stuck.
```

### Indegree

**Indegree** = number of incoming edges to a node.

### Steps

1. Compute indegree of every node
2. Push all nodes with indegree `0` into a queue
3. While queue not empty:
   - Pop node → add to topo order
   - For each neighbor: decrement indegree; if `0`, push neighbor
4. If `len(topo) == V` → valid DAG, no cycle  
   Else → cycle exists

### Code

```python
from collections import deque

indeg = [0] * len(adj)
for u in range(len(adj)):
    for v in adj[u]:
        indeg[v] += 1

q = deque(i for i in range(len(adj)) if indeg[i] == 0)
topo = []

while q:
    node = q.popleft()
    topo.append(node)
    for nbr in adj[node]:
        indeg[nbr] -= 1
        if indeg[nbr] == 0:
            q.append(nbr)

has_cycle = len(topo) != len(adj)
```

### Example — DAG (no cycle)

```text
0 → 1
↓
2
```

```text
Indegrees: 0:0  1:1  2:1

Queue: [0] → pop 0, topo [0] → 1,2 become 0
Queue: [1,2] → pop 1, topo [0,1] → pop 2, topo [0,1,2]

len(topo) == 3 == V  →  no cycle
Output: [0, 1, 2]  (or [0, 2, 1] depending on queue order)
```

### Example — cycle (Kahn stuck)

```text
0 → 1
↑   ↓
└── 2
```

```text
Indegrees: 0:1  1:1  2:1

Queue starts EMPTY — no node with indegree 0
Can't remove anyone → topo = []

len(topo) != V  →  cycle exists
```

**File:** `topologicalsort.py` (top), `find_cycles_directed.py` (`isCyclicInDirectedGraph`)

---

## 2. DFS + `visited` + `path_vis` ❌ Cycle Detection ONLY

**Not a topological sort algorithm.** Only answers: **does a cycle exist?**

### Intuition

If DFS reaches a node **already on the current recursion path** → back-edge → cycle.

### Two sets

| Set | Meaning |
|-----|---------|
| `visited` | Node explored in some previous DFS branch |
| `path_vis` | Nodes on the **current** DFS stack (active path) |

### Code

```python
def dfs(node, graph, visited, path_vis):
    visited.add(node)
    path_vis.add(node)

    for nbr in graph[node]:
        if nbr not in visited:
            if dfs(nbr, graph, visited, path_vis):
                return True
        elif nbr in path_vis:   # back-edge
            return True

    path_vis.remove(node)       # leave current path
    return False

visited, path_vis = set(), set()
for node in graph:
    if node not in visited:
        if dfs(node, graph, visited, path_vis):
            print("Cycle!")
```

### Why `path_vis`? (not just `visited`)

```text
0 → 1 → 2
      ↑   |
      └───┘
```

At node `2`, neighbor `1` is in `path_vis` → cycle.

### Why `path_vis.remove(node)`?

When backtracking, the node is **no longer on the current path**. Without removing it, edges to finished nodes would be wrongly flagged as cycles.

```text
path_vis.remove(node)  →  "this node is no longer in the recursion stack"
```

### `visited` alone is NOT enough

```text
    0 → 1
    ↓
    2
```

At `2`, neighbor `0` may be in `visited` (from branch `0→1`) but **not** in `path_vis` (current path is `0→2`). That's **not** a cycle.

**File:** `find_cycles_directed.py` (bottom `detect_cycle`)

---

## 3. DFS + Stack (Postorder) ✅ Topological Sort

**Different from the `path_vis` code above.** This is the **DFS topological sort**.

### Intuition

Finish a node **after** all its descendants are processed (postorder). Push to stack on exit. Reverse stack = valid topo order.

```text
dfs(children) first  →  then push self  →  reverse stack
```

No `path_vis` needed **unless** you also want cycle detection in the same pass.

### Code

```python
def dfs(node, graph, visited, stack):
    visited.add(node)
    for nbr in graph[node]:
        if nbr not in visited:
            dfs(nbr, graph, visited, stack)
    stack.append(node)          # push AFTER all descendants

visited, stack = set(), []
for node in graph:
    if node not in visited:
        dfs(node, graph, visited, stack)

topo_order = stack[::-1]        # reverse = topological order
```

### Trace on `0 → 1 → 2 → 3`

```text
dfs(0) → dfs(1) → dfs(2) → dfs(3) → push 3 → push 2 → push 1 → push 0
stack = [3, 2, 1, 0]
reverse → [0, 1, 2, 3]  ✓
```

### Example — same DAG as Kahn

```text
0 → 1
↓
2
```

Valid output after reverse: `0 1 2` or `0 2 1` (depends on neighbor order).

**File:** `topologicalsort.py` (`topological_sort` with stack)

---

## 4. DFS Topo + Cycle Detection (combined)

To get **both** topo order and cycle check in DFS, use `path_vis` **and** push to order on exit:

```python
def dfs(node):
    visited.add(node)
    path_vis.add(node)

    for nbr in graph[node]:
        if nbr not in visited:
            if not dfs(nbr):
                return False
        elif nbr in path_vis:
            return False          # cycle

    path_vis.remove(node)
    topo_order.append(node)       # postorder push
    return True
```

Return `topo_order[::-1]` if all nodes processed; else cycle.

**File:** `topologicalsort.py` (`dfs_topological_sort` — note: must `path_vis.remove(node)`, not `path_vis.add` again)

---

## Comparison Table

| | Graph | Kahn (BFS) | DFS `path_vis` | DFS postorder + stack | Parent check | Union-Find |
|---|-------|------------|----------------|------------------------|--------------|------------|
| **Graph type** | — | Directed | Directed | Directed | Undirected | Undirected |
| **Purpose** | — | Topo + cycle | Cycle only | Topo (+ cycle w/ `path_vis`) | Cycle only | Cycle / redundant edge |
| **Cycle rule** | — | `len(topo) < V` | `nbr in path_vis` | needs `path_vis` | `nbr in visited` ∧ `nbr != parent` | `find(u)==find(v)` before union |
| **Topo output** | — | Yes | No | Yes (`stack[::-1]`) | No | No |
| **Time** | — | O(V + E) | O(V + E) | O(V + E) | O(V + E) | ~O(α(n)) per op |
| **File** | — | `topologicalsort.py` | `find_cycles_directed.py` | `topologicalsort.py` | `find_cycles_undirected.py` | `unionfind.py` |

---

## Memory Hooks

```text
Kahn:        "Peel indegree-0 nodes. Stuck? Cycle."
DFS path_vis: "Neighbor on my current path? Cycle."
DFS postorder: "Finish kids first, push self, reverse."
```

```text
Topological sort exists  ⇔  No directed cycle  ⇔  DAG
```

---

## Which file in this repo?

| Goal | File | Function |
|------|------|----------|
| Kahn topo + cycle | `topologicalsort.py` | `kahn_topological_sort` |
| DFS topo (no cycle check) | `topologicalsort.py` | `topological_sort` |
| DFS topo + cycle | `topologicalsort.py` | `dfs_topological_sort` |
| DFS cycle only | `find_cycles_directed.py` | `detect_cycle` |
| Kahn cycle only | `find_cycles_directed.py` | `isCyclicInDirectedGraph` |

---

## Interview Quick Answers

**Q: How many ways to do topological sort?**  
Two: Kahn's (BFS + indegree) and DFS postorder + reverse stack.

**Q: Is DFS with `path_vis` a topological sort?**  
No — cycle detection only.

**Q: How does Kahn detect cycles?**  
Can't peel all nodes → `len(topo) < V`.

**Q: How does DFS detect cycles?**  
Back-edge: neighbor in `path_vis`.

**Q: When to use Kahn vs DFS topo?**  
Both O(V+E). Kahn gives cycle check naturally; DFS topo fits when you're already in a DFS problem.

---

## Related

- Full graph learning path → [README.md](README.md)
- Undirected cycle code → `find_cycles_undirected.py`
- Shortest path on DAG → `shortestpath_directed.py`, `minpathbtwnodesDAG.py`
