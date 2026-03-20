#!/usr/bin/env python3


def main() -> None:
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")

    f = open("new_discovery.txt", "w+")
    print(f"Initializing new storage unit: {f.name}")
    print("Storage unit created successfully...\n")
    print("Inscribing preservation data...")
    line1 = "[ENTRY 001] New quantum algorithm discovered"
    line2 = "\n[ENTRY 002] Efficiency increased by 347%"
    line3 = "\n[ENTRY 003] Archived by Data Archivist trainee"
    f.write(line1)
    f.write(line2)
    f.write(line3)
    f.close()
    print(f"{line1}{line2}{line3}")
    print("\nData inscription complete. Storage unit sealed.")
    print(f"Archive '{f.name}' ready for long-term preservation.")


if __name__ == "__main__":
    main()
