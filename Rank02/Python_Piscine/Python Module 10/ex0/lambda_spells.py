def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(artifacts, key=lambda x: x["power"], reverse=True)


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(filter(lambda x: x["power"] >= min_power, mages))


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda x: f"* {x} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    powers = [((lambda x: x["power"])(element)) for element in mages]
    max_pwr = (lambda x: max(x))(powers)
    min_pwr = (lambda x: min(x))(powers)
    avg = (lambda x: round(sum(x) / len(x), 2))(powers)
    return {"max_power": max_pwr, "min_power": min_pwr, "avg_power": avg}


def main() -> None:

    artifacts = [
        {'name': 'Crystal Orb', 'power': 85, 'type': 'focus'},
        {'name': 'Fire Staff', 'power': 92, 'type': 'weapon'}
    ]

    mages = [
        {'name': 'Alice', 'power': 100, 'element': 'fire'},
        {'name': 'Bob', 'power': 45, 'element': 'water'},
        {'name': 'Charlie', 'power': 85, 'element': 'earth'}
    ]

    spells = ['fireball', 'lightning']

    # ====== ARTIFACT SORTER ======
    print("\nTesting artifact sorter...")
    sorted_arts = artifact_sorter(artifacts)
    for i in range(len(sorted_arts) - 1):
        print(f"- {sorted_arts[i]["name"]} ({sorted_arts[i]["power"]} power) "
              f"comes before {sorted_arts[i+1]["name"]} "
              f"({sorted_arts[i+1]["power"]} power)")

    # ====== POWER FILTER (BY MIN) ======
    print("\nTesting power filter...")
    pwr_filter = power_filter(mages, 0)
    for i in range(len(pwr_filter)):
        print(f"- {pwr_filter[i]["name"]} ({pwr_filter[i]["power"]} power)")

    # ====== SPELL TRANSFORMER ======
    print("\nTesting spell transformer...")
    print(' '.join(spell_transformer(spells)))

    # ====== MAGE STATS ======
    print("\nTesting mage stats...")
    stats = mage_stats(mages)
    print(f"- Max Power: {stats["max_power"]}")
    print(f"- Min Power: {stats["min_power"]}")
    print(f"- Avg Power: {stats["avg_power"]}")


if __name__ == "__main__":
    main()
