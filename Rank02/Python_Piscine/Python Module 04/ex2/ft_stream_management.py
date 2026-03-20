#!/usr/bin/env python3

import sys


def main() -> None:
    print("=== CYBER ARCHIVES - COMMUNICATION SYSTEM ===\n")

    id = input("Input Stream active. Enter archivist ID: ")
    status = input("Input Stream active. Enter status report: ")

    sys.stdout.write(f"\n[STANDARD] Archive status from {id}: {status}\n")
    sys.stderr.write("[ALERT] System diagnostic: "
                     "Communication channels verified\n")
    sys.stdout.write("[STANDARD] Data transmission complete\n")

    print("\nThree-channel communication test successful.")


if __name__ == "__main__":
    main()
