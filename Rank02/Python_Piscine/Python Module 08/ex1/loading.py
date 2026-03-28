import sys
import importlib.metadata


def check_dep(module: str, desc: str) -> bool:
    try:
        version = importlib.metadata.version(module)
        print(f"[OK] {module} ({version}) - {desc}")
        return True
    except importlib.metadata.PackageNotFoundError:
        print(f"[ERROR] Missing dependency: {module}")
        return False


def main() -> None:
    print("\nLOADING STATUS: Loading programs...")

    print("\nChecking dependencies:")
    check = True
    if not check_dep("pandas", "Data manipulation ready"):
        check = False
    if not check_dep("requests", "Network access ready"):
        check = False
    if not check_dep("matplotlib", "Visualization ready"):
        check = False
        


if __name__ == "__main__":
    main()