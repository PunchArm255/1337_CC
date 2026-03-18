#!/usr/bin/env python3

from posixpath import split
import sys
import math

def stats(x, y, z):
    coords = (x, y, z)
    dist = math.sqrt((x ** 2) + (y ** 2) + (z ** 2))
    print(f"Position created: {coords}")
    print(f"Distance between (0, 0, 0) and {coords}: {dist:.2f}")
    print("\nUnpacking demonstration:")
    print(f"Player at: x={x}, y={y}, z={z}")
    print(f"Coordinates at: X={x}, Y={y}, Z={z}")


def main():
    print("=== Game Coordinate System ===\n")
    if (len(sys.argv) == 4):
        try:
            x2, y2, z2 = [int(x) for x in sys.argv[1:]]
            stats(x2, y2, z2)
        except ValueError as e:
            print("Error: Invalid Coordinates!")
            print(f"Error details - Type: ValueError, Args: {e}")

    elif (len(sys.argv) == 2):
        values = sys.argv[1].split(",")
        if len(values) != 3:
            print("You must input 3 coordinates!")
            return

        try:
            x2, y2, z2 = [int(x) for x in values]
            print(f"Parsing coordinates: \"{sys.argv[1]}\"")
            stats(x2, y2, z2)
        except ValueError as e:
            print(f"Error parsing coordinates: {e}")
            print(f"Error details - Type: ValueError, Args: {e}")

    elif (len(sys.argv) == 1):
        print("No Coordinates Given.")

    else:
        print("You must input 3 coordinates!")


if __name__ == "__main__":
    main()
