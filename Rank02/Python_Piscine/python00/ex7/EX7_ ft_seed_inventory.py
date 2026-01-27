#!/usr/bin/env python3

def ft_seed_inventory(seed_type: str, quantity: int, unit: str) -> None:
    if unit.casefold() == "packets":
        print(f"{seed_type.capitalize()} seeds: {quantity} packets available")
    elif unit.casefold() == "grams":
        print(f"{seed_type.capitalize()} seeds: {quantity} grams total")
    elif unit.casefold() == "area":
        print(f"{seed_type.capitalize()} seeds: covers {quantity} square meters")
    else:
        print("Unknown unit type")

ft_seed_inventory("Tomato", 10, "Packets")
ft_seed_inventory("Banana", 10, "gRAMS")
ft_seed_inventory("adnan", 8, "area")
ft_seed_inventory("tomato", 10, "tests")