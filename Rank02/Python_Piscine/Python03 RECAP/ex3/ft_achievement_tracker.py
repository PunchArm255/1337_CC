#!/usr/bin/env python3

def main():
    alice = {'first_kill', 'level_10', 'treasure_hunter', 'speed_demon'}
    bob = {'first_kill', 'level_10', 'boss_slayer', 'collector'}
    charlie = {'level_10', 'treasure_hunter', 'boss_slayer', 'speed_demon', 'perfectionist'}

    print("=== Achievement Tracker System ===\n")
    print(f"Player Alice achievements: {alice}")
    print(f"Player Bob achievements: {bob}")
    print(f"Player Charlie achievements: {charlie}")

    print("\n=== Achievement Analytics ===")
    all_unique = alice | bob | charlie
    all_common = alice & bob & charlie
    all_rare = (
                alice - bob - charlie |
                bob - alice - charlie |
                charlie - alice - bob
                )
    alice_vs_bob = alice & bob
    alice_unique = alice - bob
    bob_unique = bob - alice

    print(f"All unique achievements: {all_unique}")
    print(f"Total unique achievements: {len(all_unique)}")
    print(f"\nCommon to all players: {all_common}")
    print(f"Rare achievements (1 player): {all_rare}")
    print(f"\nAlice vs Bob common: {alice_vs_bob}")
    print(f"Alice unique: {alice_unique}")
    print(f"Bob unique: {bob_unique}")


if __name__ == "__main__":
    main()
