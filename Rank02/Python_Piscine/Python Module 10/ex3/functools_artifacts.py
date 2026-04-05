from collections.abc import Callable
from typing import Any
import functools
from operator import add, mul


# ====== HELPER ======
def base_enchantment(power: int, element: str, target: str) -> str:
    return f"Enchanted {target} with {power} {element} power!"


# ====== MAIN FUNCS ======
def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops = {
        "add": add,
        "multiply": mul,
        "max": max,
        "min": min
    }
    if operation not in ops:
        raise ValueError(f"- [ERROR] Unknown operation: {operation}")
    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire_enchant": functools.partial(base_enchantment, 50, "fire"),
        "ice_enchant": functools.partial(base_enchantment, 50, "ice"),
        "light_enchant": functools.partial(base_enchantment, 50, "lightning")
    }


@functools.lru_cache
def memoized_fibonacci(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @functools.singledispatch
    def cast_spell(spell: Any) -> str:
        return "Unknown spell type"

    @cast_spell.register
    def _(spell: int) -> str:
        return f"{spell} damage"

    @cast_spell.register
    def _(spell: str) -> str:
        return spell.strip()

    @cast_spell.register
    def _(spell: list) -> str:
        return f"{len(spell)} spell(s)"

    return cast_spell


def main() -> None:
    # ====== SPELL REDUCER ======
    try:
        print("\nTesting spell reducer...")
        spell_list = [1, 2, 3]
        print(f"- Sum: {spell_reducer(spell_list, "add")}")
        print(f"- Product: {spell_reducer(spell_list, "multiply")}")
        print(f"- Max: {spell_reducer(spell_list, "max")}")
        print(f"- Min: {spell_reducer(spell_list, "min")}")
    except ValueError as e:
        print(e)

    # ====== PARTIAL ENHANCER ======
    try:
        print("\nTesting partial enhancer...")
        enchanter = partial_enchanter(base_enchantment)
        print(f"- {enchanter["fire_enchant"]("Sword")}")
        print(f"- {enchanter["ice_enchant"]("Shield")}")
        print(f"- {enchanter["light_enchant"]("Staff")}")
    except KeyError:
        print("- [ERROR] Enchantment not found!")

    # ====== MEMOIZED FIBONACCI ======
    print("\nTesting memoized fibonacci...")
    print(f"- Fib(0): {memoized_fibonacci(0)}")
    print(f"- Fib(1): {memoized_fibonacci(1)}")
    print(f"- Fib(10): {memoized_fibonacci(10)}")
    print(f"- Fib(15): {memoized_fibonacci(15)}")

    # ====== SPELL DISPATCHER ======
    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(f"- Damage spell: {dispatcher(42)}")
    print(f"- Enchantment: {dispatcher("Fireball")}")
    print(f"- Multi-cast: {dispatcher(["Fireball", "Lightning"])}")
    print(f"- {dispatcher({"test": 1337})}")


if __name__ == "__main__":
    main()
