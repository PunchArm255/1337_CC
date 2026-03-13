#!/usr/bin/env python3


def main():
    print("=== CYBER ARCHIVES - PRESERVATION SYSTEM ===\n")

    file = open("new_discovery.txt", "w+")
    print(f"Initializing new storage unit: {file.name}")
    print("Storage unit created successfully...\n")

    print("Inscribing preservation data...")
    file.write("[ENTRY 001] New quantum algorithm discovered")
    file.write("\n[ENTRY 002] Efficiency increased by 347%")
    file.write("\n[ENTRY 003] Archived by Data Archivist trainee")
    file.seek(0)
    content = file.read()
    print(content)
    
    print("\nData inscription complete. Storage unit sealed.")
    print(f"Archive '{file.name}' ready for long-term preservation.")
    file.close()


if __name__ == "__main__":
    main()
