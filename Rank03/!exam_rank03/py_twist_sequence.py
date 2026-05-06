def twister(nums: list, n: int):
    if not nums: return []
    n = n % len(nums)
    return nums[-n:] + nums[:-n]

# print(twister([4, 2, 1, -1, 'a'], 4))