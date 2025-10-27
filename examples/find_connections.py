#!/usr/bin/env python3
"""
Example: Find Connections with Claude

Discover connections between notes that aren't currently linked.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python find_connections.py <note_path>")
        print("\nExample:")
        print("  python find_connections.py 'Entities/People/Brandon Han.md'")
        sys.exit(1)

    note_path = sys.argv[1]

    print("\n" + "="*80)
    print(f"Finding Connections")
    print("="*80)

    # Initialize
    integration = ClaudeObsidianIntegration()

    # Read the note
    note = integration.connector.read_note(note_path)
    print(f"\nAnalyzing: {note.title}")
    print(f"Current links: {len(note.links)}")
    print(f"Current tags: {', '.join(note.tags) if note.tags else 'None'}")

    # Find connections
    print("\n🤖 Asking Claude to find connections...")
    connections = integration.find_connections(note_path)

    if connections:
        print(f"\n💡 Suggested connections:")
        for i, conn in enumerate(connections, 1):
            print(f"\n{i}. {conn.get('title', 'Unknown')}")
            print(f"   Reason: {conn.get('reason', 'No reason provided')}")

        # Offer to add links
        print("\n" + "-"*80)
        response = input("Add these as links to the note? (y/n): ").lower()
        if response == 'y':
            links_to_add = [f"[[{conn.get('title')}]]" for conn in connections]
            new_content = note.content.rstrip() + '\n\n## Suggested Connections\n' + '\n'.join([f"- {link}" for link in links_to_add])
            integration.connector.write_note(note_path, new_content)
            print("✓ Connections added!")
    else:
        print("\n❌ No connections found")

    print("\n" + "="*80)
    print("✓ Connection analysis complete!")
    print("="*80)


if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    main()
