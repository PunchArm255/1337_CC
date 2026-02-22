#!/usr/bin/env python3
"""Inventory Master: manage game inventory using dictionaries."""

import sys


def main() -> None:
    """Parse item:quantity args and display inventory analytics."""
    print("=== Inventory System Analysis ===\n")

    if len(sys.argv) > 1:
        inv = {}
        try:
            for a in sys.argv[1:]:
                item_name, item_qty = a.split(":")
                inv[item_name] = int(item_qty)
        except ValueError as e:
            print(
                f"Error: Invalid Item Syntax.\nDetails: {e}\nCorrect Usage"
                ": ./ft_inventory_system.py <item1:value1> <item2:value2> ..."
            )
            return

        print(f"Total items in inventory: {sum(inv.values())}")
        print(f"Unique item types: {len(inv)}\n")

        item_list = []
        for k, v in inv.items():
            item_list.append([v, k])
        item_list.sort(reverse=True)

        print("=== Current Inventory ===")
        for qty, name in item_list:
            print(
                f"{name}: {qty} units ({(qty / sum(inv.values())) * 100:.1f}%)"
            )

        print("\n=== Inventory Statistics ===")
        most_unit = "unit" if item_list[0][0] == 1 else "units"
        print(f"Most abundant: {item_list[0][1]} ({item_list[0][0]} "
              f"{most_unit})")
        least_unit = "unit" if item_list[-1][0] == 1 else "units"
        print(
            f"Least abundant: {item_list[-1][1]} ({item_list[-1][0]} "
            f"{least_unit})"
        )

        print("\n=== Item Categories ===")
        moderate = {k: v for k, v in inv.items() if v > 3}
        scarce = {k: v for k, v in inv.items() if v <= 3}
        print(f"Moderate: {moderate}")
        print(f"Scarce: {scarce}")

        print("\n=== Management Suggestions ===")
        restock = []
        for k, v in inv.items():
            if v < 2:
                restock.append(k)
        print(f"Restock needed: {", ".join(restock)}")

        print("\n=== Dictionary Properties Demo ===")
        print(f"Dictionary keys: {', '.join(inv.keys())}")
        dict_vals = [str(v) for v in inv.values()]
        print(f"Dictionary values: {', '.join(dict_vals)}")
        print(f"Sample lookup - 'sword' in inventory: {'sword' in inv}")

    else:
        print(
            "Error: No items detected.\nUsage: ./ft_inventory_system.py"
            " <item1:value1> <item2:value2> ..."
        )


if __name__ == "__main__":
    main()
