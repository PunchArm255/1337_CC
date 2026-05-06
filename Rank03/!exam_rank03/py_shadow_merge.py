def merge(list1: list[int], list2: list[int]):
    return sorted((list1 or []) + (list2 or []))

# print(merge([-5, -2], [-3, -1]))
