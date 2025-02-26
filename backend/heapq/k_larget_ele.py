import heapq

def find_k_largest(nums, k):
    minHeap = nums[:k]
    heapq.heapify(minHeap)
    
    for num in nums[k:]:
        if num > minHeap[0]:
            heapq.heappushpop(minHeap, num)
    
    return sorted(minHeap, reverse=True)

nums = [7, 10, 4, 3, 20, 15]
k = 3
print(find_k_largest(nums, k))


def kth_largest(nums, k):
    min_heap = nums[:k]  # Step 1: Create a Min Heap of first K elements
    heapq.heapify(min_heap)  # Convert list to a heap (O(K))
    
    for num in nums[k:]:  # Step 2: Iterate through the rest of the array
        if num > min_heap[0]:  # If num is greater than heap's root
            heapq.heappushpop(min_heap, num)  # Push num and pop the smallest
    
    return min_heap[0]  # The root of the heap is the Kth largest

# Example Usage
nums = [7, 10, 4, 3, 20, 15]
k = 3
print(kth_largest(nums, k))  # Output: 10
