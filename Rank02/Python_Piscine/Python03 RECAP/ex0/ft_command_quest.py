#!/usr/bin/env python3

import sys

def main():
    print("=== Command Quest ===")
    if (len(sys.argv) == 1):
        print("No Arguments Provided!")
        print(f"Program name: {sys.argv[0]}")
    else:
        print(f"Program name: {sys.argv[0]}")
        print(f"Arguments given: {len(sys.argv[1:])}")
        i = 1
        for arg in sys.argv[1:]:
            print(f"Argument {i}: {arg}")
            i += 1
    print(f"Total Arguments: {len(sys.argv)}")

if __name__ == "__main__":
    main()
