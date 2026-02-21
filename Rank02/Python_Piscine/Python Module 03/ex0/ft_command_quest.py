#!/usr/bin/env python3

import sys

def main():
    print("=== Command Quest ===")
    
    if len(sys.argv) < 2:
        print("No arguments provided!")
    else:
        print(f"Arguments received: {len(sys.argv[1:])}")
        x = 1
        for arg in sys.argv[1:]:
            print(f"Argument {x}: {arg}")
            x += 1
    print(f"Total arguments: {len(sys.argv)}")

if __name__ == "__main__":
    main()
