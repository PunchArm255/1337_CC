#!/usr/bin/env python3
"""Position Tracker: 3D coordinate system using tuples."""

import sys
from math import sqrt


def stats(x: int, y: int, z: int) -> None:
    """Showcase tuple unpacking."""
    print("\nUnpacking demonstration:")
    print(f"Player at x={x}, y={y}, z={z}")
    print(f"Coordinates: X={x}, Y={y}, Z={z}")


def main() -> None:
    """Parse coordinate arguments and display results."""
    print("=== Game Coordinate System ===\n")

    if len(sys.argv) == 4:
        try:
            coords = tuple([int(a) for a in sys.argv[1:]])
            start = (0, 0, 0)
            x1, y1, z1 = start
            x2, y2, z2 = coords
            dist = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
            print(f"Position created: {coords}")
            print(f"Distance between {start} and {coords}: {dist:.2f}")
            stats(x2, y2, z2)
        except ValueError:
            print("ERROR: Coordinates can only be numbers.")
    elif len(sys.argv) == 2:
        try:
            splitted = sys.argv[1].split(",")
            coords = tuple([int(a) for a in splitted])
            if len(coords) != 3:
                print("ERROR: You must input 3 coordinates.")
                return
            start = (0, 0, 0)
            x1, y1, z1 = start
            x2, y2, z2 = coords
            dist = sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)
            print(f"Parsing coordinates: \"{sys.argv[1]}\"")
            print(f"Parsed position: {coords}")
            print(f"Distance between {start} and {coords}: {dist:.1f}")
            stats(x2, y2, z2)
        except ValueError as e:
            print(f"Parsing invalid coordinates: \"{sys.argv[1]}\"")
            print(f"Error parsing coordinates: {e}")
            print(f"Error details - Type: ValueError, Args: {e.args}")
    elif len(sys.argv) < 2:
        print("No coordinates provided. Usage: python3 ft_coordinate_system.py"
              " <X> <Y> <Z> OR \"X,Y,Z\"")
    else:
        print("ERROR: You must input 3 coordinates.")


if __name__ == "__main__":
    main()
