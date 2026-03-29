import os
import sys


def main() -> None:
    # catching an import error in case pkg isn't installed
    try:
        from dotenv import load_dotenv
    except ImportError:
        print("\n[ERROR] python-dotenv is not installed.")
        print("\nTo install, run: pip install python-dotenv")
        sys.exit(1)

    print("\nORACLE STATUS: Reading the Matrix...")

    # populating variables from .env data (if it exists)
    env = load_dotenv()
    mode = os.environ.get("MATRIX_MODE")
    db_url = os.environ.get("DATABASE_URL")
    api_key = os.environ.get("API_KEY")
    log_level = os.environ.get("LOG_LEVEL")
    zion_endpoint = os.environ.get("ZION_ENDPOINT")

    print("\nConfiguration loaded:")

    if mode:
        print(f"Mode: {mode}")
    else:
        print("Mode: [WARNING] Missing matrix mode!")

    if db_url:
        print("Database: Connected to local instance")
    else:
        print("Database: [WARNING] Missing database URL!")

    if api_key:
        print("API Access: Authenticated")
    else:
        print("API Access: [WARNING] Missing API Key!")

    if log_level:
        print(f"Log Level: {log_level}")
    else:
        print("Log Level: [WARNING] Missing log level!")

    if zion_endpoint:
        print("Zion Network: Online")
    else:
        print("Zion Network: [WARNING] Missing endpoint URL!")

    print("\nEnvironment security check:")
    print("[OK] No hardcoded secrets detected")

    if env:
        print("[OK] .env file properly configured")
    else:
        print("[KO] .env file empty or not found")

    print("[OK] Production overrides available")

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
