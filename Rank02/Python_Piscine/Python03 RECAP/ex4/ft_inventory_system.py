#!/usr/bin/env python3

import sys

def main():
    print("=== Inventory System Analysis ===")
    inv = {}
    for a in sys.argv[1:]:
        name, qty = a.split(':')
        inv[name] = int(qty)
    print(f"Total items in inventory: {sum(inv.values())}")
    print(f"Unique item types: {len(inv.items())}")

    print("\n=== Current Inventory ===")
    item_list = []
    for k, v in inv.items():
        item_list.append([v, k])
    item_list.sort(reverse=True)
    for qty, name in item_list:
        print(f"{name}: {qty} units ({qty / sum(inv.values()) * 100:.1f}%)")

    print("\n=== Inventory Statistics ===")
    print(f"Most abundant: {item_list[0][1]} - {item_list[0][0]} unit(s)")
    print(f"Least abundant: {item_list[-1][1]} - {item_list[-1][0]} unit(s)")
    
    print("\n=== Item Categories ===")
    moderate = {k: v for k, v in inv.items() if v >= 4}
    scarce = {k: v for k, v in inv.items() if v < 4}
    print(f"Moderate: {moderate}")
    print(f"Scarce: {scarce}")

    print("\n=== Management Suggestions ===")
    restock = [k for k, v in inv.items() if v < 2]
    print(f"Restock needed: {', '.join(restock)}")

    print("\n=== Dictionary Properties Demo ===")
    dict_vals = [str(v) for v in inv.values()]
    print(f"Dictionary keys: {', '.join(inv.keys())}")
    print(f"Dictionary values: {', '.join(dict_vals)}")
    print(f"Sample lookup - 'sword' in inventory: {'sword' in inv}")


if __name__ == "__main__":
    main()
