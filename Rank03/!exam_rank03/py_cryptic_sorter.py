def cryptic_sorter(tlist: list):
    def count_vowels(s):
        return sum(1 for c in s.lower() if c in "aeiou")
    
    return sorted(tlist, key=lambda x: (count_vowels(x), len(x), x))

# print(cryptic_sorter(["bbb", "ccc", "ddd"]))