# Graph Algorithms — Interview Prep Guide

Runnable Python templates for graph patterns commonly asked at top companies. Each file is self-contained — run with `python <file>.py` from this folder.

**Quick jump:** [Learning Path](#learning-path-bfs--dfs--advanced) · [Cycle Detection & Topo Sort](cycle_detection.MD) · [Algorithm Intuitions](#algorithm-intuitions) · [Cheat Sheet](#study-cheat-sheet-revision) · [When to Use Which](#when-to-use-which-algorithm) · [Problems](#problems-to-cover-by-topic)

---

## How to Use This Guide

### Per-file routine

1. **Read** the function and trace the example graph on paper
2. **Run** `python <file>.py` and match printed output
3. **Rewrite** the core function from memory (blank editor, 15 min timer)
4. **Solve** 2 LeetCode problems from the problem list below for that topic
5. **Compare** your solution to the template — note what differed (input format, return type)

### Folder structure

| Path | Purpose |
|------|---------|
| `*.py` (root) | Core algorithm templates |
| `prbs/` | LeetCode-style problems applying those templates |
| `cycle_detection.MD` | Topo sort vs cycle detection — Kahn vs DFS (`path_vis` vs postorder) |

---

## Learning Path: BFS / DFS → Advanced

Everything builds on **BFS/DFS**. Topological sort and Kahn's algorithm are not separate magic — they are specialized uses of BFS/DFS on **directed** graphs.

### The big picture (one sentence per level)

```text
BFS/DFS          →  "visit every node / explore a region"
Cycle detection  →  "can I loop back?"
Topological sort →  "in what order can I do things?" (directed, no cycle)
Shortest path    →  "what's the minimum cost/distance?"
Union-Find       →  "are these two connected?"
Interview prbs   →  mix patterns above
```

### 4-week study plan

```
Week 1: Traversal + Cycles
  bfs_dfs_templates.py → find_cycles_undirected.py → find_cycles_directed.py

Week 2: Ordering + Shortest Path (unweighted / DAG)
  topologicalsort.py → shortestpath_undirected.py → minpathbtwnodesDAG.py

Week 3: Weighted Shortest Path
  shortestpath_directed.py → bellmanford.py → multisource_bfs.py → bidirectional_bfs.py

Week 4: Union-Find + Interview Problems
  unionfind.py → prbs/* (pick 2–3 per day)
```

---

### Level 0 — Foundations (start here)

**File:** `bfs_dfs_templates.py`

| Tool | What it does | Mental model |
|------|----------------|--------------|
| **BFS** | Queue, layer by layer | "Closest first" — shortest path when no weights |
| **DFS** | Stack/recursion, go deep | Flood fill, islands, explore all paths |

```text
BFS:  start → neighbors → neighbors of neighbors ...
DFS:  start → go deep → backtrack → go deep elsewhere ...
```

**Interview uses:** Number of Islands, flood fill, clone graph, grid exploration.

---

### Level 1 — Cycle detection (first step after BFS/DFS)

You must understand cycles **before** topological sort makes sense (topo only works on a **DAG**).

**Full guide with examples, code, Kahn vs DFS `path_vis` vs postorder:**  
→ **[cycle_detection.MD](cycle_detection.MD)**

| Graph | Code | One-line rule |
|-------|------|---------------|
| Undirected | `find_cycles_undirected.py` | `neighbor in visited and neighbor != parent` |
| Directed | `find_cycles_directed.py` | `neighbor in path_vis` OR Kahn `len(order) < V` |

---

### Level 2 — Topological sort

**File:** `topologicalsort.py` · **Deep dive:** [cycle_detection.MD](cycle_detection.MD)

#### What problem does it solve?

```text
"Do A before B, B before C" → valid order: A, B, C
```

**Interview signals:** prerequisite, dependency, course schedule, build order, alien dictionary.

#### Two ways to topological sort

| Method | Based on | Topo? | Cycle check? |
|--------|----------|-------|--------------|
| **Kahn's algorithm** | BFS + indegree | ✅ | ✅ `len(order) < V` |
| **DFS postorder + reverse stack** | DFS | ✅ | ❌ alone — needs `path_vis` |

**Not topo sort:** DFS + `visited` + `path_vis` without postorder push → **cycle detection only**. See [cycle_detection.MD](cycle_detection.MD).

**Topo sort template (Kahn — mental model):**
1. Count in-degrees → push indegree-0 nodes to queue
2. Pop, append to order, reduce neighbor in-degrees
3. `len(order) == V` ? valid DAG : cycle

---

### Level 3 — Shortest path (builds on BFS)

| Graph | Weights | Algorithm | File |
|-------|---------|-----------|------|
| Any | None | **BFS** | `shortestpath_undirected.py` |
| DAG | Any (even negative) | **Topo sort + relax** | `minpathbtwnodesDAG.py` |
| General | ≥ 0 | **Dijkstra** (min-heap) | `shortestpath_directed.py` |
| General | Negative | **Bellman-Ford** | `bellmanford.py` |
| Many sources | Unweighted | **Multi-source BFS** | `multisource_bfs.py` |
| Start + end | Unweighted | **Bidirectional BFS** | `bidirectional_bfs.py` |

**DAG shortest path** connects Level 2 → Level 3:
1. Topo sort nodes
2. Relax edges in that order (O(V+E), handles negative weights on DAG)

---

### Level 4 — Union-Find (different family)

**File:** `unionfind.py`

Not BFS/DFS — used for:
- Connected components
- "Does adding this edge create a cycle?" (undirected)
- Dynamic connectivity

```text
Cycle in undirected?  → DFS parent check  OR  Union-Find while adding edges
```

---

### Level 5 — Interview problems

**Folder:** `prbs/`

| Problem | Pattern |
|---------|---------|
| `course_schedule.py` | Kahn's topo + cycle |
| `alien_dictionary.py` | Build graph from order → topo |
| `network_delay_time.py` | Dijkstra |
| `mincostflightkstops.py` | Dijkstra + K stops |
| `pacific_atlantic.py` | DFS/BFS from borders |
| `clone_graph.py` | BFS/DFS + hash map |

---

### Full flow diagram (repo file order)

```text
                    bfs_dfs_templates.py
                    (BFS + DFS basics)
                           │
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
   find_cycles_      find_cycles_     (grid/islands
   undirected.py     directed.py       stay on BFS/DFS)
           │               │
           │               ▼
           │        topologicalsort.py  ← Kahn's (BFS) + DFS topo
           │               │
           │               ▼
           │        minpathbtwnodesDAG.py  (topo + shortest path)
           │               │
           ▼               ▼
      unionfind.py    shortestpath_undirected.py
           │               │
           │               ▼
           │        shortestpath_directed.py (Dijkstra)
           │               │
           │               ▼
           │        bellmanford.py
           │               │
           └───────┬───────┘
                   ▼
        multisource_bfs.py / bidirectional_bfs.py
                   │
                   ▼
              prbs/* (LeetCode style)
```

---

### Memory hooks

```text
BFS        → "shortest unweighted, layers, multi-source"
DFS        → "deep explore, islands, backtrack, DFS topo"
Kahn       → "BFS on in-degree 0, peel layers, cycle if order < V"
Topo DFS   → "finish node after kids, reverse stack"
Dijkstra   → "min-heap, non-negative weights"
Bellman    → "negative weights, relax V-1 times"
Union-Find → "connected? redundant edge?"
```

```text
Undirected / Directed / Kahn / path_vis:  see cycle_detection.MD
Union-Find:  "Are these two already connected before I add this edge?"
```

---

### One-line interview answers

| Question | Answer |
|----------|--------|
| What is topological sort? | Linear ordering of DAG where every edge u→v has u before v — [cycle_detection.MD](cycle_detection.MD) |
| What is Kahn's algorithm? | BFS topo: repeatedly remove in-degree-0 nodes — [cycle_detection.MD](cycle_detection.MD) |
| When use Kahn vs DFS topo? | See comparison table in [cycle_detection.MD](cycle_detection.MD) |
| Why learn cycles before topo? | Topo only exists if no directed cycle — [cycle_detection.MD](cycle_detection.MD) |
| BFS vs Dijkstra? | BFS = unweighted; Dijkstra = weighted (≥ 0) |
| What is a DAG? | Directed Acyclic Graph — directed, no cycles |
| Cycle detection? | [cycle_detection.MD](cycle_detection.MD) |

---

## When to Use Which Algorithm

| Scenario | Algorithm | Time | File |
|----------|-----------|------|------|
| Shortest path, **unweighted** (fewest edges) | BFS | O(V + E) | `shortestpath_undirected.py`, `bfs_dfs_templates.py` |
| Shortest path, **non-negative weights** | Dijkstra (min-heap) | O(E log V) | `shortestpath_directed.py`, `shortestpath_undirected.py` |
| Shortest path, **weighted DAG** (can have negative edges) | Topo sort + relax | O(V + E) | `minpathbtwnodesDAG.py`, `shortestpath_directed.py` |
| Shortest path, **negative weights** (general graph) | Bellman-Ford | O(VE) | `bellmanford.py` |
| Shortest path, **0/1 weights only** | 0-1 BFS (deque) | O(V + E) | `multisource_bfs.py` |
| Shortest path, **two endpoints**, unweighted | Bidirectional BFS | O(V + E) | `bidirectional_bfs.py` |
| **Multiple sources** spreading together | Multi-source BFS | O(V + E) | `multisource_bfs.py` |
| **Cycle** in undirected graph | BFS/DFS (parent check) or Union-Find | O(V + E) | `find_cycles_undirected.py` — [guide](cycle_detection.MD) |
| **Cycle** in directed graph | Kahn's topo OR DFS + `path_vis` | O(V + E) | `find_cycles_directed.py` — [guide](cycle_detection.MD) |
| **Ordering** with dependencies (DAG) | Topological sort (Kahn or DFS postorder) | O(V + E) | `topologicalsort.py` — [guide](cycle_detection.MD) |
| **Connected components** / dynamic connectivity | Union-Find (DSU) | ~O(α(n)) per op | `unionfind.py` |
| **Explore region** (islands, flood fill, clone) | DFS or BFS on graph/grid | O(V + E) | `bfs_dfs_templates.py` |
| **Eulerian path** (use every edge once) | Hierholzer's DFS | O(E log E) | `prbs/reconstruct_itinerary.py` |
| Shortest path with **at most K stops** | Modified Dijkstra (cost, node, stops) | O(EK log V) | `prbs/mincostflightkstops.py` |
| **Enumerate all paths** with K stops | DFS backtracking | exponential | `prbs/flightpathkstops.py` |

### Quick decision tree

```
Need shortest path?
├── Unweighted?          → BFS (or bidirectional if you know start + end)
├── Weights all 0 or 1?  → 0-1 BFS
├── DAG?                 → Topological sort + relax
├── Non-negative weights?→ Dijkstra
└── Negative weights?    → Bellman-Ford (watch for negative cycles)

Need to detect cycle?
├── Undirected?          → see cycle_detection.MD + find_cycles_undirected.py
└── Directed?            → see cycle_detection.MD + find_cycles_directed.py

Need ordering / prerequisites? → cycle_detection.MD + topologicalsort.py

Need connectivity / redundant edge? → Union-Find

Need explore all cells in a region? → DFS/BFS on grid
```

### Directed vs undirected — key differences

| | Undirected | Directed |
|---|-----------|----------|
| Adjacency list | Add edge both ways `(u,v)` and `(v,u)` | Add edge one way `(u,v)` |
| Cycle detection | See [cycle_detection.MD](cycle_detection.MD) | See [cycle_detection.MD](cycle_detection.MD) |
| BFS shortest path | Same algorithm | Same algorithm |
| Topo sort | Not applicable | Kahn or DFS postorder — [guide](cycle_detection.MD) |

---

## Algorithm Intuitions

Read these when you forget **why** an algorithm works, not just **what** to code. One intuition per pattern — interview gold.

---

### BFS (unweighted shortest path)

**Intuition:** Ripples in a pond — every node at distance `d` is discovered before any node at distance `d+1`.

Because all edges cost the same, the **first time** you reach a node is always via the fewest edges. Queue = FIFO = expand outward in rings.

```text
Start → layer 1 → layer 2 → layer 3 ...
        (dist 1)   (dist 2)   (dist 3)
```

**When it fails:** Weighted edges — a longer path with a cheap edge can beat a shorter path with expensive edges. → use Dijkstra.

**File:** `bfs_dfs_templates.py`, `shortestpath_undirected.py`

---

### DFS (explore / flood fill / backtrack)

**Intuition:** Maze explorer with chalk — go as deep as possible, hit a dead end, backtrack, try another branch.

Stack/recursion = LIFO = depth-first. Great when you need to **visit every cell once** (islands) or **try all paths** (backtracking), not when you need minimum distance.

```text
Go deep → dead end → backtrack → go deep another way
```

**File:** `bfs_dfs_templates.py`

---

### Cycle detection & topological sort

**→ Full intuitions, examples, and code:** [cycle_detection.MD](cycle_detection.MD)

Covers: undirected parent check, directed `path_vis`, Kahn's cycle check, DFS postorder topo, and which algorithm does what.

**Code:** `find_cycles_undirected.py`, `find_cycles_directed.py`, `topologicalsort.py`

---

### Shortest path on directed graphs — when to use which

From `shortestpath_directed.py`:

| Scenario | Algorithm | Time | Why |
|----------|-----------|------|-----|
| **DAG** (directed acyclic) | Topo sort + relax | O(V + E) | Process each node once in order — no heap rebalancing |
| **General graph, non-negative weights** | Dijkstra | O(E log V) | Works on any graph; greedy min-dist is safe when weights ≥ 0 |
| **General graph, negative weights** | Bellman-Ford | O(VE) | Must reconsider edges; greedy fails with negatives |

**DAG vs Dijkstra intuition:**

Dijkstra repeatedly pops the min from a heap and relaxes neighbors — each `heappush` costs O(log V). On a DAG, topo sort gives a **fixed processing order**: visit each node once, relax its outgoing edges once. No priority queue, no rebalancing → **O(V + E)** and even handles **negative edge weights** on a DAG.

```text
DAG:       topo order → relax each edge once     (one pass, no heap)
General:   Dijkstra → greedy best-so-far + heap   (needs non-negative weights)
Negative:  Bellman-Ford → relax ALL edges V-1 times (slow but correct)
```

**Files:** `shortestpath_directed.py` (`dijkstra` + `min_sum_path_dag`), `minpathbtwnodesDAG.py`, `bellmanford.py`

---

### Dijkstra

**Intuition:** Greedy best-first search with a scoreboard. Always expand the **closest unvisited** node — safe only when edge weights are **non-negative**.

```text
pq: (dist, node) → pop min → update neighbors if shorter path found
```

**Why not negative weights?** You might commit to a "short" path early, then a negative edge later makes a longer-looking path actually cheaper. Greedy is wrong.

**File:** `shortestpath_directed.py`

---

### Bellman-Ford

**Intuition:** Don't trust greedy — relax **every edge** repeatedly. After V-1 rounds, shortest paths have propagated. One more round detects negative cycles.

```text
Repeat V-1 times: for every edge (u,v,w): dist[v] = min(dist[v], dist[u] + w)
```

Slow O(VE) but handles negative weights on general graphs.

**File:** `bellmanford.py`

---

### Multi-source BFS

**Intuition:** Many fires start at once — all spread at the same speed. Whoever reaches a cell first wins (minimum distance to **nearest** source).

```text
Seed queue with ALL sources at dist 0 → single BFS wave
```

**Signal:** "minimum time for all oranges to rot", "distance to nearest gate/0".

**File:** `multisource_bfs.py`

---

### Bidirectional BFS

**Intuition:** Two people walk toward each other from start and end — meet in the middle. Search space grows as a ball; two smaller balls meet faster than one big ball.

```text
START → → → ← ← ← END
         meet here
```

**Signal:** one start, one end, unweighted, huge graph, short answer path.

**File:** `bidirectional_bfs.py`

---

### 0-1 BFS

**Intuition:** BFS with a twist — weight-0 edges go to the **front** of the deque (same layer), weight-1 edges go to the **back** (next layer). Still O(V+E), no heap.

```text
deque: push_front for 0-weight, push_back for 1-weight
```

**Signal:** grid with cost 0 or 1 only.

**File:** `multisource_bfs.py`

---

### Union-Find (DSU)

**Intuition:** Groups of friends merging. "Are A and B in the same group?" — if yes and you add edge A—B, that edge is **redundant** (creates a cycle).

```text
find(x) → root of x's group
union(a,b) → merge groups; if same root already → cycle edge
```

**Signal:** connected components, redundant connection, dynamic connectivity.

**File:** `unionfind.py`

---

### Modified Dijkstra (K stops / hops)

**Intuition:** Regular Dijkstra but state is `(cost, node, stops_left)`. You pay an extra dimension when the problem limits **number of edges**, not just total weight.

```text
pq: (cost, node, k_remaining) → pop min → relax with k-1
```

**Signal:** "cheapest flight with at most K stops".

**File:** `prbs/mincostflightkstops.py`

---

### Quick intuition index

| Pattern | One-line intuition |
|---------|-------------------|
| BFS | Ripples outward — first arrival = shortest (unweighted) |
| DFS | Go deep, backtrack — explore regions / all paths |
| Cycle / topo | See [cycle_detection.MD](cycle_detection.MD) |
| DAG shortest path | Topo order → relax once per edge, no heap |
| Dijkstra | Always expand closest node (weights ≥ 0) |
| Bellman-Ford | Relax all edges V-1 times (negatives OK) |
| Multi-source BFS | Many fires spreading together |
| Bidirectional BFS | Two waves meet in the middle |
| 0-1 BFS | Deque: 0-cost front, 1-cost back |
| Union-Find | Same group + new edge = redundant / cycle |
| K stops | Dijkstra + extra state for hops remaining |

---

## Study Cheat Sheet (Revision)

Read this section before interviews or when you forget **which pattern to pick**. Each block answers: *what is it → when to use → how to recognize → which file*.

---

### 1. Graph basics (30-second recall)

| Term | Meaning |
|------|---------|
| **V** | Number of vertices (nodes) |
| **E** | Number of edges |
| **Adjacency list** | `graph[u] = [neighbors]` — default for interviews |
| **Adjacency matrix** | `grid[i][j]` — use when graph is a 2D matrix (islands, maze) |
| **Weighted edge** | `(u, v, weight)` — shortest path needs Dijkstra/Bellman-Ford/topo |
| **Unweighted edge** | `(u, v)` — BFS gives shortest path |
| **Connected** | Path exists between every pair of nodes (undirected) |
| **Strongly connected** | Path both ways between every pair (directed only) |

**Build adjacency list from edges:**
```python
graph = defaultdict(list)
for u, v in edges:
    graph[u].append(v)          # directed
    graph[v].append(u)          # undirected — add BOTH directions
```

---

### 2. Undirected vs Directed (uni vs bi-directional)

**Undirected (bi-directional):** edge `A—B` means you can go `A→B` and `B→A`.
- Road between two cities (two-way street)
- Friendship graph
- Build: `graph[u].append(v)` AND `graph[v].append(u)`

**Directed (uni-directional):** edge `A→B` means only `A→B`, not back.
- Course prerequisites (`prereq → course`)
- One-way street, Twitter follow
- Build: `graph[u].append(v)` only

| Question type | Graph type |
|---------------|------------|
| "Can finish all courses?" | Directed |
| "Redundant connection" | Undirected |
| "Alien dictionary order" | Directed (char precedence) |
| "Number of islands" | Grid (treat as undirected 4/8 neighbors) |
| "Word ladder" | Directed (implicit graph: word → word) |
| "Clone graph" | Undirected (LeetCode 133) |

**Cycle detection & topological sort** — full walkthrough with step-by-step examples (undirected parent check, directed `path_vis`, Kahn's, DFS postorder):

→ **[cycle_detection.MD](cycle_detection.MD)**

**Code:** `find_cycles_undirected.py`, `find_cycles_directed.py`, `topologicalsort.py`, `unionfind.py` (undirected redundant edge)

---

### 3. DAG — what it is and everything you do with it

**DAG = Directed Acyclic Graph** — directed, no cycles.

```
A → B → D
↓       ↑
C ──────┘   ✓ DAG (no cycle)

A → B → C → A   ✗ NOT a DAG (cycle)
```

**Why DAGs matter:** many problems hide a dependency order. If you remove cycles, you get a valid sequence.

| Operation on DAG | Algorithm | When to use | File |
|------------------|-----------|-------------|------|
| **Valid ordering exists?** | Topo sort; if len(order) `< V` → cycle | "Can finish courses?" | `topologicalsort.py`, `prbs/course_schedule.py` |
| **Print order** | Kahn (BFS on in-degree 0) or DFS post-order reverse | Course schedule II, build order | `topologicalsort.py` |
| **Shortest path (weighted, can have negative edges on DAG)** | Topo sort → relax edges in order | Faster than Dijkstra on DAG; handles negative weights | `minpathbtwnodesDAG.py` |
| **Longest path on DAG** | Same as shortest but maximize | Critical path, max height | Same template, flip `<` to `>` |
| **Count paths from source to target** | Topo sort + DP | All paths in DAG (no exponential blow-up) | DP on topo order |
| **Detect if graph is DAG** | Cycle detection OR topo length == V | Pre-check before topo-based DP | `find_cycles_directed.py` |

**Interview signals for DAG / topo sort:**
- "prerequisite", "dependency", "order", "before/after"
- "schedule", "course", "build sequence"
- " alien dictionary", "character precedence"
- "longest increasing path" (grid can be treated as DAG if you only move one direction)

**Topo sort algorithms & cycle rules:** → [cycle_detection.MD](cycle_detection.MD)

---

### 4. BFS vs DFS — when to use which

| Use **BFS** when | Use **DFS** when |
|------------------|------------------|
| Shortest path (unweighted) | Explore all paths / backtracking |
| Level-by-level (rotting oranges) | Flood fill / islands / connected component |
| Multi-source spread | Clone graph (recursive natural) |
| 0-1 BFS (deque) | Topological sort (DFS variant) |
| "Minimum steps / days / distance" | "All paths", "permutations on graph" |
| Grid shortest path | Pacific Atlantic (DFS from borders) |

**BFS = queue, FIFO → explores layer by layer (closest first)**
**DFS = stack/recursion, LIFO → goes deep first**

| Pattern | BFS or DFS? |
|---------|-------------|
| Number of Islands | DFS or BFS (either works) |
| Word Search (backtrack) | DFS |
| Shortest path binary matrix | BFS |
| Clone Graph | DFS or BFS |
| Course Schedule | BFS (Kahn) or DFS |
| Rotting Oranges | Multi-source BFS |

---

### 5. Shortest path — complete revision table

| Graph type | Weights | Algorithm | Key state | File |
|------------|---------|-----------|-----------|------|
| Any | None (unweighted) | BFS | `(node, dist)` in queue | `shortestpath_undirected.py` |
| Any | None, know start + end | Bidirectional BFS | Two frontiers meet | `bidirectional_bfs.py` |
| Any | 0 or 1 only | 0-1 BFS | Deque: weight 0 → front | `multisource_bfs.py` |
| DAG | Any (incl. negative) | Topo + relax | Process nodes in topo order | `minpathbtwnodesDAG.py` |
| General | Non-negative | Dijkstra | Min-heap `(dist, node)` | `shortestpath_directed.py` |
| General | Negative allowed | Bellman-Ford | Relax all edges V-1 times | `bellmanford.py` |
| Directed | Non-neg + max K edges | Modified Dijkstra | `(cost, node, stops_left)` | `prbs/mincostflightkstops.py` |

**One-line rules:**
- No weights → **BFS**
- Weights ≥ 0 → **Dijkstra**
- DAG → **Topo + relax** (beats Dijkstra, allows negative on DAG)
- Negative on general graph → **Bellman-Ford**
- Limit on number of edges/hops → add **extra dimension** to state (K stops)

**Why not Dijkstra with negative weights?** Greedy pick of min dist fails; a longer path with negative edge can become shorter later.

**Directed graph shortest path — pick one:**

| Scenario | Use | Intuition |
|----------|-----|-----------|
| DAG | Topo + relax | One pass in order — O(V+E), negatives OK on DAG |
| General, weights ≥ 0 | Dijkstra | Greedy closest-first with heap |
| General, negative weights | Bellman-Ford | Relax all edges V-1 times |

See [Algorithm Intuitions → Shortest path on directed graphs](#shortest-path-on-directed-graphs--when-to-use-which) and `shortestpath_directed.py`.

---

### 6. Multi-source BFS vs Bidirectional BFS

These sound similar but solve **different problems**.

**Multi-source BFS** — many starting points, all spread at the same time.
- Seed queue with ALL sources at distance 0
- Example: all rotten oranges, all gates, all border cells
- Question signal: "minimum time for ALL to reach state", "distance to nearest X"
- File: `multisource_bfs.py`

**Bidirectional BFS** — ONE start, ONE end, meet in the middle.
- BFS from start AND from end simultaneously
- Stop when frontiers overlap
- Faster when graph is huge and path is short
- Question signal: "shortest transformation", "minimum steps from A to B"
- File: `bidirectional_bfs.py`

```
Multi-source:     [S1][S2][S3] → spread outward together
Bidirectional:    START ←→ → → END  (two waves meet)
```

---

### 7. Cycle detection & topological sort

**→ Full guide:** [cycle_detection.MD](cycle_detection.MD) — undirected, directed, Kahn's, DFS `path_vis`, DFS postorder, comparison tables, interview Q&A.

**Linked list cycle** = directed cycle with out-degree 1 (Floyd's slow/fast) — see `backend/linkedlist/`

---

### 8. Union-Find — when to use

Use when edges are added **incrementally** and you need connectivity without full graph traversal.

| Signal | Example |
|--------|---------|
| "Redundant edge" | LeetCode 684 |
| "Connected components count" | LeetCode 323 |
| "Valid tree?" | n-1 edges + all connected |
| "Accounts merge" (same email group) | LeetCode 721 |
| "Dynamic connectivity" | Offline: process edges in order |

**Not Union-Find:** shortest path, topo order, level-by-level BFS.

**Template:** `find(x)` with path compression + `union(x,y)` by rank → `components` count.

---

### 9. Problem → algorithm (interview night before)

| You see this in the problem | Reach for |
|-----------------------------|-----------|
| Grid of 0/1, count regions | DFS/BFS flood |
| Prerequisites / ordering | Topo sort |
| "Shortest path" + no weights | BFS |
| "Shortest path" + weights ≥ 0 | Dijkstra |
| "Shortest path" + DAG | Topo + relax |
| "Shortest path" + negative weights | Bellman-Ford |
| "At most K stops/flights/hops" | Dijkstra + K in state |
| "All paths with K steps" | DFS backtrack |
| "Spread from multiple sources" | Multi-source BFS |
| "Transform A to B in min steps" | Bidirectional BFS |
| "Cycle in undirected" | [cycle_detection.MD](cycle_detection.MD) + `find_cycles_undirected.py` |
| "Cycle in directed" | [cycle_detection.MD](cycle_detection.MD) + `find_cycles_directed.py` |
| "Merge connected groups" | Union-Find |
| "Use every edge exactly once" | Hierholzer (Euler) |
| "Clone / copy graph" | DFS/BFS + hashmap `{old: new}` |

---

### 10. Complexity cheat sheet

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS / DFS | O(V + E) | O(V) |
| Dijkstra | O(E log V) | O(V + E) |
| Bellman-Ford | O(VE) | O(V) |
| Topo sort | O(V + E) | O(V) |
| Union-Find (m ops) | O(m α(n)) | O(V) |
| Bidirectional BFS | O(V + E) worst, often faster | O(V) |
| 0-1 BFS | O(V + E) | O(V) |

---

### 11. Pre-interview 5-minute drill

1. **Undirected vs directed** — how do you build adj list? → [cycle_detection.MD](cycle_detection.MD) for cycle rules
2. **DAG** — what is it? 3 things you can do (order, shortest path, DP on order)
3. **Shortest path** — unweighted → ? weighted non-neg → ? DAG → ? negative → ?
4. **Topo sort / cycles** — [cycle_detection.MD](cycle_detection.MD)
5. **Multi-source vs bidirectional** — one sentence each
6. **Union-Find** — one problem it solves that BFS cannot do easily

If you can answer all six from memory, you are ready for 80% of graph interviews.

---

## File Index

### Core templates (study in order)

| # | File | Topics |
|---|------|--------|
| 1 | `bfs_dfs_templates.py` | Graph DFS/BFS, islands, flood fill, clone graph, grid shortest path |
| 2 | `find_cycles_undirected.py` | Undirected cycle — [cycle_detection.MD](cycle_detection.MD) |
| 3 | `find_cycles_directed.py` | Directed cycle — [cycle_detection.MD](cycle_detection.MD) |
| 4 | `topologicalsort.py` | Kahn's algo, DFS topo — [cycle_detection.MD](cycle_detection.MD) |
| 5 | `shortestpath_undirected.py` | BFS unweighted + Dijkstra undirected |
| 6 | `minpathbtwnodesDAG.py` | DAG weighted shortest path + BFS |
| 7 | `shortestpath_directed.py` | Dijkstra directed + DAG topo shortest path |
| 8 | `bellmanford.py` | Negative weights + negative cycle detection |
| 9 | `multisource_bfs.py` | Rotting oranges, walls/gates, 0-1 BFS |
| 10 | `bidirectional_bfs.py` | Word Ladder pattern |
| 11 | `unionfind.py` | DSU, connected components, redundant connection |

### Interview problems (`prbs/`)

| File | LeetCode | Pattern |
|------|----------|---------|
| `course_schedule.py` | [207](https://leetcode.com/problems/course-schedule/), [210](https://leetcode.com/problems/course-schedule-ii/) | Topo sort + cycle |
| `network_delay_time.py` | [743](https://leetcode.com/problems/network-delay-time/) | Dijkstra |
| `alien_dictionary.py` | [269](https://leetcode.com/problems/alien-dictionary/) | Topo sort on chars |
| `eventual_safe_states.py` | [802](https://leetcode.com/problems/find-eventual-safe-states/) | Reverse topo / cycle |
| `clone_graph.py` | [133](https://leetcode.com/problems/clone-graph/) | DFS/BFS + hashmap |
| `mincostflightkstops.py` | [787](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Dijkstra + stop limit |
| `flightpathkstops.py` | — | DFS enumerate paths |
| `pacific_atlantic.py` | [417](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Multi-source from borders |
| `reconstruct_itinerary.py` | [332](https://leetcode.com/problems/reconstruct-itinerary/) | Eulerian path |

---

## Problems to Cover by Topic

### BFS / DFS (foundations)
- [Number of Islands](https://leetcode.com/problems/number-of-islands/) — `bfs_dfs_templates.py`
- [Flood Fill](https://leetcode.com/problems/flood-fill/) — `bfs_dfs_templates.py`
- [Max Area of Island](https://leetcode.com/problems/max-area-of-island/)
- [Clone Graph](https://leetcode.com/problems/clone-graph/) — `prbs/clone_graph.py`
- [Keys and Rooms](https://leetcode.com/problems/keys-and-rooms/)
- [All Paths From Source to Target](https://leetcode.com/problems/all-paths-from-source-to-target/)
- [Pacific Atlantic Water Flow](https://leetcode.com/problems/pacific-atlantic-water-flow/) — `prbs/pacific_atlantic.py`
- [Surrounded Regions](https://leetcode.com/problems/surrounded-regions/)
- [Word Search](https://leetcode.com/problems/word-search/) — see `backend/backtraking/`

### Multi-source BFS
- [Rotting Oranges](https://leetcode.com/problems/rotting-oranges/) — `multisource_bfs.py`
- [01 Matrix](https://leetcode.com/problems/01-matrix/)
- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
- [Walls and Gates](https://leetcode.com/problems/walls-and-gates/) — `multisource_bfs.py`

### Bidirectional BFS
- [Word Ladder](https://leetcode.com/problems/word-ladder/) — `bidirectional_bfs.py`
- [Word Ladder II](https://leetcode.com/problems/word-ladder-ii/) (hard — backtracking)

### Topological Sort
- [Course Schedule](https://leetcode.com/problems/course-schedule/) — `prbs/course_schedule.py`
- [Course Schedule II](https://leetcode.com/problems/course-schedule-ii/)
- [Alien Dictionary](https://leetcode.com/problems/alien-dictionary/) — `prbs/alien_dictionary.py`
- [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees/)
- [Sequence Reconstruction](https://leetcode.com/problems/sequence-reconstruction/)
- [Find Eventual Safe States](https://leetcode.com/problems/find-eventual-safe-states/) — `prbs/eventual_safe_states.py`

### Cycle Detection
- [Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) — see `backend/linkedlist/`
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/) — `unionfind.py`
- [Redundant Connection II](https://leetcode.com/problems/redundant-connection-ii/) (hard)

### Shortest Path — Unweighted
- [Shortest Path in Binary Matrix](https://leetcode.com/problems/shortest-path-in-binary-matrix/)
- [Jump Game III](https://leetcode.com/problems/jump-game-iii/)
- [Snakes and Ladders](https://leetcode.com/problems/snakes-and-ladders/)

### Shortest Path — Dijkstra
- [Network Delay Time](https://leetcode.com/problems/network-delay-time/) — `prbs/network_delay_time.py`
- [Path with Minimum Effort](https://leetcode.com/problems/path-with-minimum-effort/)
- [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) — `prbs/mincostflightkstops.py`
- [Path With Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/)
- [Swim in Rising Water](https://leetcode.com/problems/swim-in-rising-water/) (hard)

### Shortest Path — DAG / Bellman-Ford
- [Parallel Courses](https://leetcode.com/problems/parallel-courses/)
- [Cheapest Flights Within K Stops](https://leetcode.com/problems/cheapest-flights-within-k-stops/) (Bellman-Ford variant also works)
- [Find the City With the Smallest Number of Neighbors at a Threshold Distance](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/)

### Union-Find
- [Number of Connected Components in an Undirected Graph](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) — `unionfind.py`
- [Redundant Connection](https://leetcode.com/problems/redundant-connection/)
- [Accounts Merge](https://leetcode.com/problems/accounts-merge/)
- [Graph Valid Tree](https://leetcode.com/problems/graph-valid-tree/)
- [Number of Provinces](https://leetcode.com/problems/number-of-provinces/)
- [Most Stones Removed with Same Row or Column](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)

### Eulerian Path / Advanced Graph
- [Reconstruct Itinerary](https://leetcode.com/problems/reconstruct-itinerary/) — `prbs/reconstruct_itinerary.py`
- [Critical Connections in a Network](https://leetcode.com/problems/critical-connections-in-a-network/) (bridges — Tarjan)
- [Evaluate Division](https://leetcode.com/problems/evaluate-division/) (weighted Union-Find)

---

## Mandatory Top-50 Graph Problems (priority order)

Work through in this order after completing core templates:

| Priority | Problem | Difficulty | Template |
|----------|---------|------------|----------|
| 1 | Number of Islands | Medium | `bfs_dfs_templates.py` |
| 2 | Course Schedule | Medium | `prbs/course_schedule.py` |
| 3 | Course Schedule II | Medium | `prbs/course_schedule.py` |
| 4 | Clone Graph | Medium | `prbs/clone_graph.py` |
| 5 | Rotting Oranges | Medium | `multisource_bfs.py` |
| 6 | Network Delay Time | Medium | `prbs/network_delay_time.py` |
| 7 | Word Ladder | Hard | `bidirectional_bfs.py` |
| 8 | Cheapest Flights Within K Stops | Medium | `prbs/mincostflightkstops.py` |
| 9 | Redundant Connection | Medium | `unionfind.py` |
| 10 | Pacific Atlantic Water Flow | Medium | `prbs/pacific_atlantic.py` |
| 11 | Alien Dictionary | Hard | `prbs/alien_dictionary.py` |
| 12 | Find Eventual Safe States | Medium | `prbs/eventual_safe_states.py` |
| 13 | Reconstruct Itinerary | Hard | `prbs/reconstruct_itinerary.py` |
| 14 | Graph Valid Tree | Medium | `unionfind.py` |
| 15 | Number of Connected Components | Medium | `unionfind.py` |
| 16 | 01 Matrix | Medium | `multisource_bfs.py` |
| 17 | All Paths From Source to Target | Medium | DFS |
| 18 | Path with Minimum Effort | Medium | Dijkstra |
| 19 | Accounts Merge | Medium | Union-Find |
| 20 | Evaluate Division | Medium | Union-Find / BFS |

---

## Gaps Still Worth Adding Later

These are less common but appear in hard rounds:

- **Bellman-Ford** — covered in `bellmanford.py`
- **Floyd-Warshall** — all-pairs shortest path O(V³), rare in interviews
- **Tarjan's SCC / bridges** — Critical Connections
- **Kruskal's / Prim's MST** — Min Cost to Connect All Points
- **A\*** — game pathfinding, rare in FAANG

---

## Run All Examples

```bash
cd backend/graphs

# Core
python bfs_dfs_templates.py
python find_cycles_undirected.py
python find_cycles_directed.py
python topologicalsort.py
python shortestpath_undirected.py
python minpathbtwnodesDAG.py
python shortestpath_directed.py
python bellmanford.py
python multisource_bfs.py
python bidirectional_bfs.py
python unionfind.py

# Problems
python prbs/course_schedule.py
python prbs/network_delay_time.py
python prbs/alien_dictionary.py
python prbs/eventual_safe_states.py
python prbs/clone_graph.py
python prbs/mincostflightkstops.py
python prbs/flightpathkstops.py
python prbs/pacific_atlantic.py
python prbs/reconstruct_itinerary.py
```
