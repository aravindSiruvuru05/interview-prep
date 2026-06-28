# LeetCode 207 / 210 — Course Schedule (cycle detection + topological sort)

from collections import deque, defaultdict

def can_finish(num_courses, prerequisites):
    """Return True if all courses can be finished (no cycle)."""
    graph = defaultdict(list)
    indegree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    count = 0

    while queue:
        node = queue.popleft()
        count += 1
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    return count == num_courses

def find_order(num_courses, prerequisites):
    """Return topological order of courses, or [] if cycle exists."""
    graph = defaultdict(list)
    indegree = [0] * num_courses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    queue = deque([i for i in range(num_courses) if indegree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for nei in graph[node]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                queue.append(nei)

    return order if len(order) == num_courses else []

# --- Example Usage ---
num_courses = 4
prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
print(can_finish(num_courses, prerequisites))  # True
print(find_order(num_courses, prerequisites))  # [0, 1, 2, 3] or [0, 2, 1, 3]

prerequisites_cycle = [[1, 0], [0, 1]]
print(can_finish(2, prerequisites_cycle))  # False
print(find_order(2, prerequisites_cycle))  # []
