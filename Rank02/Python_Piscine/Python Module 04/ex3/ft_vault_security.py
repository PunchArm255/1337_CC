#!/usr/bin/env python3


def main():
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")

    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols\n")

    with open("classified_data.txt", "r") as file1:
        content = file1.read()
        print("SECURE EXTRACTION:")
        print(content)

    with open("security_protocols.txt", "w+") as file2:
        print("\nSECURE PRESERVATION:")
        file2.write("[CLASSIFIED] Brand New security protocols archived")
        file2.seek(0)
        content = file2.read()
        print(content)
        print("Vault automatically sealed upon completion")

    print("\nAll vault operations completed with maximum security.")


if __name__ == "__main__":
    main()
