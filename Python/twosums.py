# Problem was asking to Find two numbers in an array, that sum up to a given target value.
# ex.
# nums = [2, 7, 11, 15]
# target = 9
# Output = [0,1] Because in the list, 0 and 1 added together equals 9

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n = len(nums)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if nums[i] + nums[j] == target:
                    return [i, j]
        return []  # No solution found