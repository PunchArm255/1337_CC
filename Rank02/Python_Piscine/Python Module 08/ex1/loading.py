import importlib.metadata
import sys


# we check if the modules are correctly installed before importing
# in case of an error, we catch it
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

    # adding a boolean check to use for report
    print("\nChecking dependencies:")
    check = True
    if not check_dep("pandas", "Data manipulation ready"):
        check = False
    if not check_dep("requests", "Network access ready"):
        check = False
    if not check_dep("matplotlib", "Visualization ready"):
        check = False

    # this report will be printed in case of a PackageNotFoundError
    if not check:
        print("\n[ABORT] Missing required programs.")
        print("\nPlease install dependencies using:"
              "\npip install -r requirements.txt"
              "\nOR"
              "\npoetry install")
        sys.exit(1)

    # utilizing late import after we ensured everything is installed
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as mp

    print("\nAnalyzing Matrix data..."
          "\nProcessing 1000 data points..."
          "\nGenerating visualization...")

    # utilizing numpy to generate 2 lists of random integers
    x_data = np.random.randint(0, 100, 1000)
    y_data = np.random.randint(0, 100, 1000)

    # utilizing pandas to organize the previous lists into a dataframe
    df = pd.DataFrame({'x_axis': x_data, 'y_axis': y_data})

    # utilizing matplotlib to generate a graph from the processed data
    mp.bar(df['x_axis'], df['y_axis'])
    mp.title("Data Points Analysis")

    # catching a KeyboardIntrrupt error in case we ctrl+c during display
    try:
        mp.savefig("matrix_analysis.png")
        mp.show()
    except KeyboardInterrupt:
        print("\n[ABORT] Analysis interrupted.")

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
