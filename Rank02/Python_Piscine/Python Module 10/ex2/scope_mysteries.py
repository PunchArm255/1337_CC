from collections.abc import Callable


def mage_counter() -> Callable:
    count = 0

    def count_tracker() -> int:
        nonlocal count
        count += 1
        return count
    return count_tracker


def spell_accumulator(initial_power: int) -> Callable:
    base_power = initial_power

    def power_tracker(amount: int):
        nonlocal base_power
        base_power += amount
        return base_power
    return power_tracker


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchanter(item_name: str) -> str:
        return f"{enchantment_type.strip()} {item_name.strip()}"
    return enchanter


def memory_vault() -> dict[str, Callable]:
    memory = {}

    def store(key: str, value: int) -> None:
        memory[key] = value

    def recall(key: int) -> int | str:
        return memory.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    # ====== MAGE COUNTER ======
    print("\nTesting mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"- Counter A: {counter_a()}")
    print(f"- Counter A: {counter_a()}")
    print(f"- Counter B: {counter_b()}")

    # ====== SPELL ACCUMULATOR ======
    print("\nTesting spell accumulator...")
    base = 100
    accumulator = spell_accumulator(base)
    print(f"- Base: {base}, add: 20 ==> {accumulator(20)}")
    print(f"- Base: {base}, add: 30 ==> {accumulator(30)}")

    # ====== ENCHANTMENT FACTORY ======
    print("\nTesting enchantment factory...")
    flame_enchatement = enchantment_factory("Flaming")
    freeze_enchatement = enchantment_factory("Frozen")
    print(f"- {flame_enchatement("Sword")}")
    print(f"- {freeze_enchatement("Sheild")}")

    # ====== MEMORY VAULT ======
    print("\nTesting memory vault...")
    vault = memory_vault()
    vault["store"]("secret", 42)
    print("- Store 'secret' = 42")
    val1 = vault["recall"]("secret")
    print(f"- Recall 'secret': {val1}")
    val2 = vault["recall"]("unknown")
    print(f"- Recall 'unknown': {val2}")


if __name__ == "__main__":
    main()
