#!/usr/bin/env python3
"""
Simple Hello World example for iSH
"""

def main():
    print("=" * 50)
    print("  🐍 Python is running on iSH!")
    print("=" * 50)
    print()

    name = input("What's your name? ")
    print(f"\nHello, {name}! Welcome to Python on iSH! 🎉")

    # Show Python version
    import sys
    print(f"\nYou're running Python {sys.version}")

if __name__ == "__main__":
    main()
