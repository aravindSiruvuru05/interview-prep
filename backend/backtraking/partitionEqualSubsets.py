
class Solution:
    def canPartitionKSubsets(self, nums, k):
        total = sum(nums)
        if total % k != 0:
            return False
        target = total // k
        nums.sort(reverse=True)
        
        buckets = [0] * k
        
        def backtrack(index):
            if index == len(nums):
                return all(b == target for b in buckets)
            
            for i in range(k):
                if buckets[i] + nums[index] <= target:
                    buckets[i] += nums[index]
                    if backtrack(index + 1):
                        return True
                    buckets[i] -= nums[index]
                if buckets[i] == 0:
                    break  # avoid duplicate work
            return False
        
        return backtrack(0)
    