#!/usr/bin/env python3

import sys
import math


def display_stats(x, y, z):
    """Handles the common math and printing logic."""
    coords = (x, y, z)
    distance = math.sqrt(x**2 + y**2 + z**2)

    print(f"Position created: {coords}")
    print(f"Distance between (0, 0, 0) and {coords}: {distance:.2f}\n")
    print("Unpacking demonstration:")
    print(f"Player at: x={x}, y={y}, z={z}")
    print(f"Coordinates at: X={x}, Y={y}, Z={z}")


def main():
    print("=== Game Coordinate System ===\n")

    if len(sys.argv) == 1:
        print("No scores provided. Usage: python3 ft_coordinate_system.py "
              "<score1> <score2> ...")
        return

    if len(sys.argv) == 2:
        try:
            values = sys.argv[1].split(',')
            if len(values) != 3:
                print("Error: You must input 3 coordinates (x, y, z)")
                return
            x, y, z = [int(v) for v in values]
            print(f"Parsing coordinates: \"{sys.argv[1]}\"")
            display_stats(x, y, z)

        except ValueError as e:
            print(f"Parsing invalid coordinates: \"{sys.argv[1]}\"")
            print(f"Error parsing coordinates: {e}")
            print(f"Error details - Type: ValueError, Args: (\"{e}\")")

    elif len(sys.argv) == 4:
        try:
            x, y, z = [int(v) for v in sys.argv[1:]]
            display_stats(x, y, z)

        except ValueError as e:
            print(f"Error initializing coordinates: {e}")
            print(f"Error details - Type: ValueError, Args: (\"{e}\")")

    else:
        print("Error: You must input 3 coordinates (x, y, z)")


if __name__ == "__main__":
    main()
