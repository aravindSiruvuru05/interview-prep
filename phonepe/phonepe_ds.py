# Q1
# In a connected undirected graph with n nodes labeled 1 to n and n edges, there is exactly one redundant edge. You need to find and remove it, ensuring that the resulting graph is a tree of n nodes.
# Example:
# Input: [[1, 2], [1, 3], [2, 3]]
# Output: [2, 3]
# Input: [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]
# Output: [1, 4]

from collections import defaultdict, deque


def checkredundent(edges, n):
    adj = defaultdict(list)
    vis = set()
    for e in edges:
        u, v = e[0], e[1]
        adj[u].append(v)
        adj[v].append(u)
    res = []
    
    def bfs(node):
        q = deque([(node, None)]) #   3 1
        while q:
            k, parent = q.popleft() #  3 1
            if k in vis:
                res.append((parent, k))
                continue
                
            vis.add(k)# 1, 2
            
            for neigh in adj[k]:
                if neigh not in vis:
                    q.append((neigh, k))
    
    for i in range(1, n):
        if i not in vis:
            bfs(i)
    return res
    
result = checkredundent([[1, 2], [2, 3], [3, 1]], 3)
print(result)


# You have k servers numbered from 0 to k-1 that are being used to handle multiple requests simultaneously.
#  Each server has infinite computational capacity but cannot handle more than one request at a time.
#  The requests are assigned to servers according to a specific algorithm:

# The ith (0-indexed) request arrives.
# If all servers are busy, the request is dropped (not handled at all).
# If the (i % k)th server is available, assign the request to that server.
# Otherwise, assign the request to the next available server (wrapping around the 
# list of servers and starting from 0 if necessary). 
# For example, if the ith server is busy, try to assign the request to the (i+1)th server,
#  then the (i+2)th server, and so on.
# You are given a strictly increasing array arrival of positive integers, 
# where arrival[i] represents the arrival time of the ith request, 
# and another array load, where load[i] represents the load of the ith request
#  (the time it takes to complete). Your goal is to find the busiest server(s).
#  A server is considered busiest if it handled the most number of requests successfully 
# among all the servers.

# Return a list containing the IDs (0-indexed) of the busiest server(s). 
# You may return the IDs in any order.

# Input: k = 3, arrival_time = [1,2,3,4,5], load = [5,2,3,3,3] 
# Output: [1] 
# Explanation: 
# All of the servers start out available.
# The first 3 requests are handled by the first 3 servers in order.
# Request 3 comes in. Server 0 is busy, so it's assigned to the next available server, which is 1.
# Request 4 comes in. It cannot be handled since all servers are busy, so it is dropped.
# Servers 0 and 2 handled one request each, while server 1 handled two requests. Hence server 1 is the busiest server.



from heapq import heappush, heappop
from sortedcontainers import SortedList

def busiestServers(k, arrival, load):
    available = SortedList(range(k))  # All servers initially available
    busy = []  # Min-heap for busy servers: (end_time, server_id)
    requests = [0] * k  # Count of requests handled by each server

    for i, (start, duration) in enumerate(zip(arrival, load)):
        # Free up servers that are done before this request arrives
        while busy and busy[0][0] <= start:
            end_time, server_id = heappop(busy)
            available.add(server_id)
        
        if not available:
            continue  # Drop the request
        
        # Find the next available server >= (i % k)
        idx = available.bisect_left(i % k)
        if idx == len(available):
            idx = 0  # wrap around
        
        server_id = available[idx]
        available.remove(server_id)
        requests[server_id] += 1
        heappush(busy, (start + duration, server_id))
    
    max_requests = max(requests)
    return [i for i, count in enumerate(requests) if count == max_requests]


# In bisect_left(arr, x):

# If x is found, it returns the index of the first occurrence of x.

# If x is not found, it returns the index of the smallest element greater than x, i.e., where x could be inserted to keep the list sorted.

# Special Case:
# If x is larger than all elements in arr, it will return len(arr).

# ### Time Complexity Breakdown:

# 1. **Loop over `n` requests:**  
#    - `n = len(arrival)` → We process each request once → **O(n)**

# 2. **Inside each request:**

#    - **Free up servers using heap (`busy`):**  
#      Each server is pushed and popped from the heap exactly once per request it processes.  
#      Heap operations are **O(log k)**, and since at most **n** requests can be processed, this step contributes **O(n log k)** overall.

#    - **Find next available server using `SortedList.bisect_left()`:**  
#      The `bisect_left` on `SortedList` is **O(log k)** per request.

#    - **Insertion/Removal in `SortedList`:**  
#      Adding or removing a server ID is **O(log k)** per operation.

# ---

# ### **Total Time Complexity:**

# - Outer loop: **O(n)**
# - Heap operations: **O(n log k)**
# - SortedList operations: **O(n log k)**

# ### **Final Time Complexity:**  
# \[
# O(n \log k)
# \]

# ---

# ### Space Complexity:
# - **Heap (busy):** Up to **O(k)** elements (worst case all servers busy).
# - **SortedList (available):** Up to **O(k)**.
# - **Request counter array:** **O(k)**.

# ### **Final Space Complexity:**  
# \[
# O(k)
# \]

# ---

# ⚠ **Note:**  
# This is optimal because you need at least **O(log k)** per request to search for the next server or manage busy servers efficiently.

# ---

# Want me to also discuss edge cases or compare it to a naïve brute-force approach?