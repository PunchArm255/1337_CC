def pattern_tracker(s: str):
    count = 0
    for a, b in zip(s, s[1:]):
        if a.isdigit() and b.isdigit() and int(b) == int(a) + 1:
            count += 1
    return count

# print(pattern_tracker("111111"))