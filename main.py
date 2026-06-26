"""
main.py

Entry point. Run this file to use the system:  python main.py
"""

import sys

import orchestrator


def main():
    """
    Implement:
      1. Get a request. While you're testing, start with a hard-coded string, e.g.
           request = "Write a function that checks if a number is prime"
         Once it works end-to-end, switch to input() to type your own.
      2. Pass it to orchestrator.run(request) and store the result.
      3. Print the result so you can see the final code.
    """
    request = input("Enter your coding request: ")
    try:
        result = orchestrator.run(request)
        print("\n--- Final Code ---\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
