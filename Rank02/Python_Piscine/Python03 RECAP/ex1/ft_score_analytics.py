#!/usr/bin/env python3

import sys

def main():
    print("=== Player Score Analytics ===")
    if (len(sys.argv) == 1):
        print("No Scores Provided.")
    else:
        scores = [int(x) for x in sys.argv[1:]]
        print(f"Scores processed: {scores}")
        print(f"Total score: {sum(scores)}")
        print(f"Average score: {sum(scores)/len(scores):.1f}")
        print(f"High score: {max(scores)}")
        print(f"Low score: {min(scores)}")
        print(f"Score range: {max(scores) - min(scores)}\n")

if __name__ == "__main__":
    main()
