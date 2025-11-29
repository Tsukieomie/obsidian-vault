#!/usr/bin/env python3
"""
Python Launcher for iSH
Interactive menu to run example scripts and custom Python code
"""

import os
import sys
import subprocess
from pathlib import Path

def clear_screen():
    """Clear the terminal screen"""
    os.system('clear' if os.name == 'posix' else 'cls')

def run_script(script_path):
    """Run a Python script"""
    try:
        print(f"\n🚀 Running {script_path}...")
        print("=" * 60)
        subprocess.run([sys.executable, script_path], check=True)
        print("=" * 60)
        input("\n✅ Script finished. Press Enter to continue...")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Script failed with error code {e.returncode}")
        input("Press Enter to continue...")
    except KeyboardInterrupt:
        print("\n\n⚠️  Script interrupted!")
        input("Press Enter to continue...")

def list_examples():
    """List all example scripts"""
    examples_dir = Path(__file__).parent / "examples"
    if not examples_dir.exists():
        return []

    scripts = sorted(examples_dir.glob("*.py"))
    return scripts

def run_custom_code():
    """Run custom Python code"""
    print("\n💻 Enter Python code (type 'END' on a new line to execute):")
    print("-" * 60)

    lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        except EOFError:
            break

    code = "\n".join(lines)

    if code.strip():
        print("\n🚀 Executing...")
        print("=" * 60)
        try:
            exec(code)
        except Exception as e:
            print(f"\n❌ Error: {e}")
        print("=" * 60)
        input("\n✅ Done. Press Enter to continue...")
    else:
        print("❌ No code entered!")
        input("Press Enter to continue...")

def show_python_info():
    """Show Python and system information"""
    import platform

    print("\n🐍 Python Information:")
    print("=" * 60)
    print(f"  Python Version: {sys.version}")
    print(f"  Python Executable: {sys.executable}")
    print(f"  Platform: {platform.platform()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Working Directory: {Path.cwd()}")
    print("=" * 60)

    # List installed packages
    print("\n📦 Installed Packages:")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
    except subprocess.CalledProcessError:
        print("  ❌ Could not list packages")

    input("\nPress Enter to continue...")

def main():
    """Main menu loop"""
    while True:
        clear_screen()
        print("=" * 60)
        print("  🐍 Python Launcher for iSH")
        print("=" * 60)

        # Show examples
        examples = list_examples()
        print("\n📚 Example Scripts:")
        for i, script in enumerate(examples, 1):
            print(f"  {i}. {script.stem.replace('_', ' ').title()}")

        print(f"\n  {len(examples) + 1}. Run custom Python code")
        print(f"  {len(examples) + 2}. Show Python info")
        print(f"  {len(examples) + 3}. Open Python REPL")
        print(f"  {len(examples) + 4}. Exit")

        print("\n" + "=" * 60)
        choice = input(f"Choose an option (1-{len(examples) + 4}): ").strip()

        try:
            choice_num = int(choice)

            if 1 <= choice_num <= len(examples):
                # Run example script
                script = examples[choice_num - 1]
                run_script(script)

            elif choice_num == len(examples) + 1:
                # Run custom code
                run_custom_code()

            elif choice_num == len(examples) + 2:
                # Show Python info
                show_python_info()

            elif choice_num == len(examples) + 3:
                # Open REPL
                print("\n🐍 Opening Python REPL...")
                print("   (Type 'exit()' or press Ctrl+D to return)")
                print("=" * 60)
                subprocess.run([sys.executable])

            elif choice_num == len(examples) + 4:
                # Exit
                print("\n👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice!")
                input("Press Enter to continue...")

        except ValueError:
            print("❌ Please enter a number!")
            input("Press Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
