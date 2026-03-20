#!/usr/bin/env python3


def crisis_response(file: str) -> None:
    prefix = "ROUTINE ACCESS" if "standard" in file else "CRISIS ALERT"
    print(f"{prefix}: Attempting access to '{file}'...")

    try:
        with open(file, "r") as f:
            data = f.read()
            print(f"SUCCESS: Archive recovered - \"{data}\"")
            print("STATUS: Normal operations resumed\n")
    except FileNotFoundError:
        print("RESPONSE: Archive not found in storage matrix")
        print("STATUS: Crisis handled, system stable\n")
    except PermissionError:
        print("RESPONSE: Security protocols deny access")
        print("STATUS: Crisis handled, security maintained\n")
    except Exception:
        print("RESPONSE: Unidentified error detected")
        print("STATUS: Crisis handled, system stable\n")


def main() -> None:
    print("=== CYBER ARCHIVES - CRISIS RESPONSE SYSTEM ===\n")

    crisis_response("lost_archive.txt")
    crisis_response("classified_vault.txt")
    crisis_response("standard_archive.txt")

    print("All crisis scenarios handled successfully. Archives secure.")


if __name__ == "__main__":
    main()
