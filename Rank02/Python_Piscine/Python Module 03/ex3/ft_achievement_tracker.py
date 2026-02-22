#!/usr/bin/env python3
"""Achievement Hunter: track unique achievements using sets."""


def main() -> None:
    """Demonstrate set operations on player achievement data."""
    print("=== Achievement Tracker System ===\n")

    alice = {"first_kill", "level_10", "treasure_hunter", "speed_demon"}
    bob = {"first_kill", "level_10", "boss_slayer", "collector"}
    charlie = {
        "level_10",
        "treasure_hunter",
        "boss_slayer",
        "speed_demon",
        "perfectionist",
    }

    all_union = alice.union(bob).union(charlie)
    all_inter = alice.intersection(bob).intersection(charlie)
    all_rare = (
        (alice - bob - charlie)
        | (bob - charlie - alice)
        | (charlie - bob - alice)
    )

    alice_bob = alice & bob
    alice_unique = alice - bob
    bob_unique = bob - alice

    print(f"Player alice achievements: {alice}")
    print(f"Player bob achievements: {bob}")
    print(f"Player charlie achievements: {charlie}\n")

    print("=== Achievement Analytics ===")
    print(f"All unique achievements: {all_union}")
    print(f"Total unique achievements: {len(all_union)}\n")

    print(f"Common to all players: {all_inter}")
    print(f"Rare achievements (1 player): {all_rare}\n")

    print(f"Alice vs Bob common: {alice_bob}")
    print(f"Alice unique: {alice_unique}")
    print(f"Bob unique: {bob_unique}")


if __name__ == "__main__":
    main()
