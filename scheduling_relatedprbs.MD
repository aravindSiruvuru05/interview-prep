**a list of LeetCode problems that follow this type of pattern** — involving concepts like:

- Round-robin scheduling / modulo-based assignment
- Managing availability / busy states (like server or resource management)
- Using **heap + bisect** or **heap + tree set** to efficiently manage timelines and scheduling.

### 🔥 Here's a curated list of similar LeetCode problems you’ll love:

---

### **1. 1882. Process Tasks Using Servers**  
> https://leetcode.com/problems/process-tasks-using-servers/

- Given a list of servers with weights and tasks arriving over time, assign tasks using a similar "find next available server" strategy.
- **Concepts**: Min-heap, scheduling, greedy.

---

### **2. 862. Shortest Subarray with Sum at Least K**  
> https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/

- Using deque or monotonic queue to manage windows, similar to "when to release/load next".
- **Concepts**: Sliding window + deque.

---

### **3. 253. Meeting Rooms II**  
> https://leetcode.com/problems/meeting-rooms-ii/

- Count the minimum number of meeting rooms required by tracking busy/free slots.
- **Concepts**: Min-heap for end times.

---

### **4. 981. Time Based Key-Value Store**  
> https://leetcode.com/problems/time-based-key-value-store/

- Store values along a timeline and binary search for the latest valid value at or before a certain time.
- **Concepts**: HashMap + `bisect_right`.

---

### **5. 759. Employee Free Time**  
> https://leetcode.com/problems/employee-free-time/

- Given schedules of employees, find common free slots.
- **Concepts**: Merging intervals with heap.

---

### **6. 1730. Shortest Path to Get Food**  
> https://leetcode.com/problems/shortest-path-to-get-food/

- While it’s a grid BFS, it relates to how resources (like servers) are used to "find the next best move".
- **Concepts**: BFS + Queue.

---

### **7. 218. The Skyline Problem**  
> https://leetcode.com/problems/the-skyline-problem/

- Track active buildings (similar to servers) and output key points.
- **Concepts**: Sweep line + max-heap.

---

### **8. 1057. Campus Bikes**  
> https://leetcode.com/problems/campus-bikes/

- Assign workers to bikes based on closest available pairings.
- **Concepts**: Greedy + heap.

---

### **9. 621. Task Scheduler**  
> https://leetcode.com/problems/task-scheduler/

- Schedule tasks with cooldown periods between them, minimizing idle time.
- **Concepts**: Priority Queue + greedy.

---

### **10. 1700. Number of Students Unable to Eat Lunch**  
> https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/

- Round-robin style queue where students either take food or move to the end.
- **Concepts**: Queue + simulation.

---

---

### 🛠 Most of these problems involve:
- **scheduling/assignment**
- **queues or heaps**
- **binary search (`bisect_left`/`bisect_right`)**
- **modulo-based round-robin logic**

---

Want me to also create a **study plan** based on these kinds of problems? 🚀

Sure! Here's a **comprehensive list of scheduling-related problems on LeetCode**, perfect for sharpening your understanding of resource allocation, task assignment, and scheduling strategies.

---

### 🗓️ **Top Scheduling Problems on LeetCode:**

---

### **1. 253. Meeting Rooms II**  
🔗 https://leetcode.com/problems/meeting-rooms-ii/  
- Find the minimum number of meeting rooms needed to schedule all meetings.  
- **Key Concepts**: Min-heap, interval overlap.

---

### **2. 1094. Car Pooling**  
🔗 https://leetcode.com/problems/car-pooling/  
- Can you schedule all trips without exceeding capacity?  
- **Key Concepts**: Prefix sum (sweep line).

---

### **3. 1109. Corporate Flight Bookings**  
🔗 https://leetcode.com/problems/corporate-flight-bookings/  
- Use range updates to process bulk bookings efficiently.  
- **Key Concepts**: Difference array.

---

### **4. 621. Task Scheduler**  
🔗 https://leetcode.com/problems/task-scheduler/  
- Schedule tasks with cooldown (n) periods between the same task.  
- **Key Concepts**: Greedy + max-heap.

---

### **5. 759. Employee Free Time**  
🔗 https://leetcode.com/problems/employee-free-time/  
- Find common free time slots for all employees' schedules.  
- **Key Concepts**: Interval merging + min-heap.

---

### **6. 1700. Number of Students Unable to Eat Lunch**  
🔗 https://leetcode.com/problems/number-of-students-unable-to-eat-lunch/  
- A circular queue scheduling problem (round-robin logic).  
- **Key Concepts**: Queue + simulation.

---

### **7. 1882. Process Tasks Using Servers**  
🔗 https://leetcode.com/problems/process-tasks-using-servers/  
- Assign tasks to servers based on availability & weight.  
- **Key Concepts**: Min-heap + scheduling.

---

### **8. 1834. Single-Threaded CPU**  
🔗 https://leetcode.com/problems/single-threaded-cpu/  
- Schedule tasks based on when the CPU is free.  
- **Key Concepts**: Greedy + heap.

---

### **9. 1361. Validate Binary Tree Nodes**  
🔗 https://leetcode.com/problems/validate-binary-tree-nodes/  
- Schedule/validate tree node relations (single parent rule).  
- **Key Concepts**: Union-Find or graph traversal.

---

### **10. 1399. Count Largest Group**  
🔗 https://leetcode.com/problems/count-largest-group/  
- This is about grouping and counting, similar to bucketing or scheduling by digit sum.  
- **Key Concepts**: HashMap + counting.

---

### **11. 253. Meeting Rooms II**  
🔗 https://leetcode.com/problems/meeting-rooms-ii/  
- **Reinforcing scheduling** concepts using intervals + heaps.

---

### **12. 1851. Minimum Interval to Include Each Query**  
🔗 https://leetcode.com/problems/minimum-interval-to-include-each-query/  
- For each query, find the smallest interval that includes it.  
- **Key Concepts**: Offline queries + min-heap.

---

### **13. 632. Smallest Range Covering Elements from K Lists**  
🔗 https://leetcode.com/problems/smallest-range-covering-elements-from-k-lists/  
- Merge k sorted streams with scheduling insight.  
- **Key Concepts**: Min-heap + sliding window.

---

### **14. 759. Employee Free Time**  
🔗 https://leetcode.com/problems/employee-free-time/  
- Yes, this is here again because it’s *very* core to scheduling interviews or slots.

---

### **15. 846. Hand of Straights**  
🔗 https://leetcode.com/problems/hand-of-straights/  
- Scheduling consecutive cards in valid groups.  
- **Key Concepts**: Greedy + min-heap.

---

---

### 🏆 **Bonus Pattern: Sweep Line + Greedy + Heap**
Most scheduling problems revolve around:
- **Sorting by time/intervals**
- **Managing ongoing tasks/events using a heap**
- **Greedy assignment (e.g., next available server/resource)**

---

Would you like me to also group these into **easy / medium / hard** buckets or maybe build you a **custom roadmap** to master scheduling problems? 🚀