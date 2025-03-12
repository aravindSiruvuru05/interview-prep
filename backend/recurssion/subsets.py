def subsets(self, nums):
    result = []
    def solve(i, curr):
        if i == len(nums):
            result.append(curr)
            return 
        
        solve(i+1, curr + [nums[i]])
        solve(i+1, curr)
    solve(0, [])

    return result
