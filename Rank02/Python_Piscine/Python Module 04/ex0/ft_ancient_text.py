#!/usr/bin/env python3


def main():
    print("=== CYBER ARCHIVES - DATA RECOVERY SYSTEM ===\n")
    try:
        file = open("ancient_fragment.txt", "r")
        print(f"Accessing Storage Vault: {file.name}")
        print("Connection established...\n")
        print("RECOVERED DATA:")
        content = file.read()
        print(content)
        print("\nData recovery complete. Storage unit disconnected.")
    except FileNotFoundError:
        print("ERROR: Storage vault not found. Run data generator first.")
    finally:
        file.close()


if __name__ == "__main__":
    main()
