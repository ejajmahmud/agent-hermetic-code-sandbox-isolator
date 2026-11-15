"""CLI for Hermetic Code Sandbox."""
import argparse
from .core import HermeticSandbox

def main():
    parser = argparse.ArgumentParser(description="Hermetic Code Sandbox CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate isolated script execution")
    args = parser.parse_args()

    sandbox = HermeticSandbox(timeout_seconds=3.0)
    script = "print('Hello from inside the hermetic sandbox! Current working dir has only run.py')"
    res = sandbox.execute_code(script)

    print(f"Execution Exit Code: {res.exit_code}")
    print(f"Stdout Output: {res.stdout.strip()}")

if __name__ == "__main__":
    main()
