# LeetCode 743 — Network Delay Time (Dijkstra from single source to all nodes)

import heapq
from collections import defaultdict

def network_delay_time(times, n, k):
    """Time for signal to reach all nodes from k. -1 if any node unreachable."""
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {i: float('inf') for i in range(1, n + 1)}
    dist[k] = 0
    pq = [(0, k)]

    while pq:
        d, node = heapq.heappop(pq)
        if d > dist[node]:
            continue
        for nei, w in graph[node]:
            new_dist = d + w
            if new_dist < dist[nei]:
                dist[nei] = new_dist
                heapq.heappush(pq, (new_dist, nei))

    max_dist = max(dist.values())
    return max_dist if max_dist != float('inf') else -1

# --- Example Usage ---
times = [[2, 1, 1], [2, 3, 1], [3, 4, 1]]
n = 4
k = 2
print(network_delay_time(times, n, k))  # 2

times2 = [[1, 2, 1]]
print(network_delay_time(times2, 2, 1))  # 1

times3 = [[1, 2, 1], [2, 1, 3]]
print(network_delay_time(times3, 2, 1))  # 3
