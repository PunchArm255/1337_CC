from collections.abc import Callable


# ====== HELPER FUNCTIONS ======
def spell(target: str, power: int) -> str:
    return f"Spell hits {target} with {power} power"


def heal(target: str, power: int) -> str:
    return f"Heal restores {power} HP for {target}"


def cond(target: str, power: int) -> bool:
    if power > 70:
        return True
    return False


# ====== HIGHER ORDER FUNCS ======
def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    def result(target, power) -> tuple[Callable, Callable]:
        return (spell1(target, power), spell2(target, power))
    return result


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    def result(target, power) -> Callable:
        amp_power = power * multiplier
        return base_spell(target, amp_power)
    return result


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    def result(target, power) -> Callable | str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"
    return result


def spell_sequence(spells: list[Callable]) -> Callable:
    def result(target, power) -> None:
        for spell in spells:
            print(f"- {spell(target, power)}")
    return result


def main() -> None:
    # ====== SPELL COMBINER ======
    print("\nTesting spell combiner...")
    combined = spell_combiner(spell, heal)
    print(f"- Combined spell result: {', '.join(combined("Dragon", 67))}")

    # ====== POWER AMPLIFIER ======
    print("\nTesting power amplifier...")
    amped = power_amplifier(spell, 10)
    print(f"- Original: {spell("Dragon", 67)}"
          f"\n- Amplified: {amped("Dragon", 67)}")

    # ====== CONDITIONAL CASTER ======
    print("\nTesting conditional caster...")
    conditional = conditional_caster(cond, spell)
    print(f"- Casting spell: {conditional("Dragon", 67)}")

    # ====== SPELL SEQUENCE =======
    print("\nTesting spell sequence...")
    spell_list = [spell, heal]
    sequence = spell_sequence(spell_list)
    sequence("Dragon", 69)


if __name__ == "__main__":
    main()
