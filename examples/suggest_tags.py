#!/usr/bin/env python3
"""
Example: Tag Suggestions with Claude

Get intelligent tag suggestions for your notes.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration


def main():
    print("\n" + "="*80)
    print("Tag Suggestions with Claude")
    print("="*80)

    # Initialize
    integration = ClaudeObsidianIntegration()
    connector = integration.connector

    # Find notes with few or no tags
    print("\n🔍 Finding notes that need tags...")
    notes_needing_tags = []

    for path in connector.list_notes():
        note = connector.read_note(path)
        if len(note.tags) < 3:  # Notes with fewer than 3 tags
            notes_needing_tags.append((path, note))

    print(f"Found {len(notes_needing_tags)} notes with fewer than 3 tags")

    # Process first 5
    for i, (path, note) in enumerate(notes_needing_tags[:5], 1):
        print(f"\n{i}. {note.title}")
        print(f"   Current tags: {', '.join(note.tags) if note.tags else 'None'}")

        print(f"   🤖 Getting suggestions from Claude...")
        suggestions = integration.suggest_tags(path, max_tags=5)
        print(f"   💡 Suggested: {', '.join([f'#{tag}' for tag in suggestions])}")

        # Optionally update the note
        response = input("   Add these tags? (y/n): ").lower()
        if response == 'y':
            # Add tags to end of note
            new_content = note.content.rstrip() + '\n\n' + ' '.join([f'#{tag}' for tag in suggestions])
            connector.write_note(path, new_content)
            print("   ✓ Tags added!")

    print("\n" + "="*80)
    print("✓ Tag suggestions complete!")
    print("="*80)


if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    main()
