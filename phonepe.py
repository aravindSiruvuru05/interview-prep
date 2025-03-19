# import requests
# import mysql.connector
# import pandas as pd

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


# You have k servers numbered from 0 to k-1 that are being used to handle multiple requests simultaneously. Each server has infinite computational capacity but cannot handle more than one request at a time. The requests are assigned to servers according to a specific algorithm:

# The ith (0-indexed) request arrives.
# If all servers are busy, the request is dropped (not handled at all).
# If the (i % k)th server is available, assign the request to that server.
# Otherwise, assign the request to the next available server (wrapping around the list of servers and starting from 0 if necessary). For example, if the ith server is busy, try to assign the request to the (i+1)th server, then the (i+2)th server, and so on.
# You are given a strictly increasing array arrival of positive integers, where arrival[i] represents the arrival time of the ith request, and another array load, where load[i] represents the load of the ith request (the time it takes to complete). Your goal is to find the busiest server(s). A server is considered busiest if it handled the most number of requests successfully among all the servers.

# Return a list containing the IDs (0-indexed) of the busiest server(s). You may return the IDs in any order.

# Input: k = 3, arrival_time = [1,2,3,4,5], load = [5,2,3,3,3] 
# Output: [1] 
# Explanation: 
# All of the servers start out available.
# The first 3 requests are handled by the first 3 servers in order.
# Request 3 comes in. Server 0 is busy, so it's assigned to the next available server, which is 1.
# Request 4 comes in. It cannot be handled since all servers are busy, so it is dropped.
# Servers 0 and 2 handled one request each, while server 1 handled two requests. Hence server 1 is the busiest server.

# Example 1:

# {
#     0: 6,
#     1: 4, 7
#     2: 6
# }
{
    0: 6v
    1: 4
    2: 3
}
set = (2, ) 
[(nexttime, ki)] (3, 2) ---  (4, 1), (6, 0) 

servers = [{6 1}, {4 1}, {6, 1}]
    
     
    
    
    
