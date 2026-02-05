#!/usr/bin/env python3

def ft_water_reminder():
    a = int(input("Days since last watering: "))
    if a > 2:
        print("Water the plants!")
    else:
        print("Plants are fine.")
