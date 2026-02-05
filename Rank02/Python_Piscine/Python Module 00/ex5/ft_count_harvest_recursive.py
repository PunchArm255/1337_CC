#!/usr/bin/env python3

def ft_count_harvest_recursive():
    a = int(input("Days until harvest: "))
    i = 1

    def counter(i):
        if i > a:
            return
        elif i <= a:
            print(f"Day {i}")
            i = i + 1
        counter(i)
    counter(i)
    print("Harvest time!")
