# LeetCode 332 — Reconstruct Itinerary (Eulerian path — Hierholzer's algorithm)
# Pattern: DFS on multigraph, always pick lexicographically smallest next edge

from collections import defaultdict

def find_itinerary(tickets):
    graph = defaultdict(list)
    for src, dst in sorted(tickets):
        graph[src].append(dst)

    route = []

    def dfs(airport):
        while graph[airport]:
            nxt = graph[airport].pop(0)
            dfs(nxt)
        route.append(airport)

    dfs("JFK")
    return route[::-1]

# --- Example Usage ---
tickets = [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
print(find_itinerary(tickets))  # ["JFK", "MUC", "LHR", "SFO", "SJC"]

tickets2 = [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
print(find_itinerary(tickets2))  # ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]
