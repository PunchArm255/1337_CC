from collections.abc import Callable
from typing import Any
import functools
import operator

# ====== HELPER ======
def base_ench(power: int, element: str, target:str) -> str:
    pass


# ====== HIGHER ORDER FUNCS ======
def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0
    ops = {
        "add": operator.add,
        "multiply": operator.mul,
        "max": max,
        "min": min
    }
    if operation not in ops:
        raise ValueError(f"- [ERROR] Unknown operation: {operation}")
    return functools.reduce(ops[operation], spells)


def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    pass


def memoized_fibonacci(n: int) -> int:
    pass


def spell_dispatcher() -> Callable[[Any], str]:
    pass


def main() -> None:
    # ====== SPELL REDUCER ======
    print("\nTesting spell reducer...")
    spell_list = [1, 2, 3]
    try:
        print(f"- Sum: {spell_reducer(spell_list, "add")}")
        print(f"- Product: {spell_reducer(spell_list, "multiply")}")
        print(f"- Max: {spell_reducer(spell_list, "max")}")
        print(f"- Min: {spell_reducer(spell_list, "min")}")
    except ValueError as e:
        print(e)

    # ====== PARTIAL ENHANCER ======
    print("\nTesting partial enhancer...")


if __name__ == "__main__":
    main()
