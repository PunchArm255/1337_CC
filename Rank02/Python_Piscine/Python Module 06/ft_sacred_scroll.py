#!/usr/bin/env python3


import alchemy
import alchemy.elements


def main():
    print("\n=== Sacred Scroll Mastery ===")
    print("\nTesting direct module access:")

    print(f"alchemy.elements.create_fire(): "
          f"{alchemy.elements.create_fire():}")
    print(f"alchemy.elements.create_water(): "
          f"{alchemy.elements.create_water():}")
    print(f"alchemy.elements.create_earth(): "
          f"{alchemy.elements.create_earth():}")
    print(f"alchemy.elements.create_air(): "
          f"{alchemy.elements.create_air():}")

    print("\nTesting package-level access (controlled by __init__.py):")
    try:
        print(f"alchemy.create_fire(): {alchemy.create_fire():}")
        print(f"alchemy.create_water(): {alchemy.create_water():}")
        print(f"alchemy.create_earth(): {alchemy.create_earth():}")
        print(f"alchemy.create_air(): {alchemy.create_air():}")
    except AttributeError:
        print("alchemy.create_earth(): AttributeError - not exposed")
        print("alchemy.create_air(): AttributeError - not exposed")

    print("\nPackage metadata:")
    print(f"Version: {alchemy.__version__}")
    print(f"Author: {alchemy.__author__}")


if __name__ == "__main__":
    main()
