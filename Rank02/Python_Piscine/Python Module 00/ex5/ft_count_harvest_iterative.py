#!/usr/bin/env python3

def ft_count_harvest_iterative():
    a = int(input("Days until harvest: "))
    for i in range(1, a+1):
        print(f"Day {i}")
    print("Harvest time!")
