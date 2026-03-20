#!/usr/bin/env python3


def main() -> None:
    print("=== CYBER ARCHIVES - VAULT SECURITY SYSTEM ===\n")

    print("Initiating secure vault access...")
    print("Vault connection established with failsafe protocols")

    try:
        with open("classified_data.txt", "r") as f:
            data = f.read()
            print("\nSECURE EXTRACTION:")
            print(data)
    except FileNotFoundError:
        print("\nEXTRACTION ERROR:")
        print("Secure vault not found.")

    print("\nSECURE PRESERVATION:")
    with open("security_protocols.txt", "w") as f:
        proto = "[CLASSIFIED] New security protocols archived"
        f.write(proto)
        print(proto)
        print("Vault automatically sealed upon completion")

    print("\nAll vault operations completed with maximum security.")


if __name__ == "__main__":
    main()
