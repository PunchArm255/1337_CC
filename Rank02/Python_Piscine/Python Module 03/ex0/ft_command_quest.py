#!/usr/bin/env python3
"""Command Quest: discover command-line argument handling."""

import sys


def main() -> None:
    """Parse and display command-line arguments."""
    print("=== Command Quest ===")

    if len(sys.argv) < 2:
        print("No arguments provided!")
        print(f"Program name: {sys.argv[0]}")
    else:
        print(f"Program name: {sys.argv[0]}")
        print(f"Arguments received: {len(sys.argv[1:])}")
        x = 1
        for arg in sys.argv[1:]:
            print(f"Argument {x}: {arg}")
            x += 1
    print(f"Total arguments: {len(sys.argv)}")


if __name__ == "__main__":
    main()
