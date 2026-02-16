#!/usr/bin/env python3

import sys


def main():

    print("=== Command Quest ===")

    if len(sys.argv) == 1:
        print("No arguments provided!")

    print(f"Program name: {sys.argv[0]}")

    if len(sys.argv) > 1:
        print(f"Arguments received: {len(sys.argv) - 1}")
        nb = 1
        for arg in sys.argv[1:]:
            print(f"Argument {nb}: {arg}")
            nb += 1

    print(f"Total Arguments: {len(sys.argv)}\n")


if __name__ == "__main__":
    main()
