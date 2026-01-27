#!/usr/bin/env python3

def ft_count_harvest_recursive():
    a = int(input("Days until harvest: "))
    i = 1
    def count(i):
        if i == a+1:
            return
        elif i < a+1:
            print(f"Day {i}")
        i += 1
        count(i)
    count(i)
    print("Harvest time!!!!!! 🎈")

ft_count_harvest_recursive()