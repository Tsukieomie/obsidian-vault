#!/usr/bin/env python3
"""
File operations example for iSH
Demonstrates reading, writing, and manipulating files
"""

import os
from pathlib import Path

def create_sample_file():
    """Create a sample text file"""
    content = """This is a sample file created by Python on iSH!
You can read, write, and manipulate files easily.
Line 3
Line 4
Line 5"""

    with open("sample.txt", "w") as f:
        f.write(content)
    print("✅ Created sample.txt")

def read_file():
    """Read and display the file"""
    if not Path("sample.txt").exists():
        print("❌ sample.txt not found! Creating it first...")
        create_sample_file()

    print("\n📄 File contents:")
    print("-" * 40)
    with open("sample.txt", "r") as f:
        print(f.read())
    print("-" * 40)

def append_to_file():
    """Append text to the file"""
    with open("sample.txt", "a") as f:
        f.write("\n\nThis line was appended! ✨")
    print("✅ Appended to sample.txt")

def count_lines():
    """Count lines in the file"""
    with open("sample.txt", "r") as f:
        lines = f.readlines()
    print(f"\n📊 File has {len(lines)} lines")

def list_files():
    """List files in current directory"""
    print("\n📁 Files in current directory:")
    for item in sorted(Path.cwd().iterdir()):
        if item.is_file():
            size = item.stat().st_size
            print(f"  {item.name} ({size} bytes)")

def main():
    print("=" * 50)
    print("  📁 File Operations Demo")
    print("=" * 50)

    while True:
        print("\nChoose an option:")
        print("  1. Create sample file")
        print("  2. Read file")
        print("  3. Append to file")
        print("  4. Count lines")
        print("  5. List files in directory")
        print("  6. Exit")

        choice = input("\nYour choice (1-6): ").strip()

        if choice == "1":
            create_sample_file()
        elif choice == "2":
            read_file()
        elif choice == "3":
            append_to_file()
        elif choice == "4":
            count_lines()
        elif choice == "5":
            list_files()
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
