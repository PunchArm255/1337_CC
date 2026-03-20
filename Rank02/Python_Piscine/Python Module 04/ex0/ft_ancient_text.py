#!/usr/bin/env python3


def main() -> None:
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")

    try:
        f = open("ancient_fragment.txt", "r")
        data = f.read()
        f.close()
        print(f"Accessing Storage Vault: {f.name}")
        print("Connection established...\n")
        print("RECOVERED DATA:")
        print(data)
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found.")


if __name__ == "__main__":
    main()
