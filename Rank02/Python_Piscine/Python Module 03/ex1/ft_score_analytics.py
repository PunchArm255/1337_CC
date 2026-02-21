#!/usr/bin/env python3

import sys
import math


def main():
    print("=== Player Score Analytics ===")
    
    if len(sys.argv) < 2:
        print("No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...")
    else:
        try:
            scores = [int(sc) for sc in sys.argv[1:]]
            print(f"Scores processed: {scores}")
            print(f"Total players: {len(scores)}")
            print(f"Total score: {sum(scores)}")
            print(f"Average score: {sum(scores) / len(scores):.1f}")
            print(f"High score: {max(scores)}")
            print(f"Low score: {min(scores)}")
            print(f"Score range: {max(scores) - min(scores)}\n")
        except ValueError:
            print("Error: Invalid Score (Score values can only be numbers!)")


if __name__ == "__main__":
    main()
