import sys
import os
import site


# detection for venv: we compare the sys.prefix (global python path)
# with the one the interpreter is currently using
def in_venv() -> bool:
    return sys.prefix != sys.base_prefix


def main() -> None:
    # 1st check: if we're in venv (using the in_venv func)
    if in_venv():
        print("\nMATRIX STATUS: Welcome to the construct\n")

        print(f"Current Python: {sys.executable}")
        print(f"Virtual Environment: {os.path.basename(sys.prefix)}")
        print(f"Environment Path: {sys.prefix}")

        print("\nSUCCESS: You're in an isolated environment!"
              "\nSafe to install packages without affecting"
              "\nthe global system.")

        print("\nPackage installation path:"
              f"\n{site.getusersitepackages()}")

    # 2nd check: if we're out of the venv
    else:
        print("\nMATRIX STATUS: You're still plugged in\n")

        print(f"Current Python: {sys.executable}")
        print("Virtual Environment: None detected")

        print("\nWARNING: You're in the global environment!"
              "\nThe machines can see everything you install.")

        print("\nTo enter the construct, run:")
        print("python -m venv matrix_env"
              "\nsource matrix_env/bin/activate # On Unix"
              "\nmatrix_env"
              "\nScripts"
              "\nactivate   # On Windows")

        print("\nThen run this program again.")


if __name__ == "__main__":
    main()
