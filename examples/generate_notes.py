#!/usr/bin/env python3
"""
Example: Generate Notes with Claude

Generate new notes on any topic using Claude AI.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_notes.py <topic>")
        print("\nExample:")
        print("  python generate_notes.py 'Neural interface technology overview'")
        sys.exit(1)

    topic = sys.argv[1]

    print("\n" + "="*80)
    print(f"Generating Note: {topic}")
    print("="*80)

    # Initialize
    integration = ClaudeObsidianIntegration()

    # Generate note
    print("\n🤖 Asking Claude to generate note...")
    content = integration.generate_note(
        topic=topic,
        include_tags=['ai-generated', 'research'],
        save=True
    )

    print("\n" + "-"*80)
    print("Generated Content Preview:")
    print("-"*80)
    print(f"\n{content[:500]}...\n")

    print("="*80)
    print("✓ Note generated and saved!")
    print("="*80)


if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    main()
