#!/usr/bin/env python3
"""
Example: Smart Search with Claude

Search your vault and have Claude provide intelligent summaries
of the results.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration


def main():
    if len(sys.argv) < 2:
        print("Usage: python smart_search.py <search query>")
        print("\nExample:")
        print("  python smart_search.py 'DARPA BRAIN'")
        sys.exit(1)

    query = sys.argv[1]

    print("\n" + "="*80)
    print(f"Smart Search: {query}")
    print("="*80)

    # Initialize
    integration = ClaudeObsidianIntegration()

    # Perform traditional search first
    print("\n🔍 Searching vault...")
    results = integration.connector.search_notes(query)
    print(f"Found {len(results)} matching notes")

    # Get Claude's intelligent analysis
    print("\n🤖 Asking Claude to analyze results...")
    analysis = integration.smart_search(query, max_results=5)

    print("\n" + "-"*80)
    print("Claude's Analysis:")
    print("-"*80)
    print(f"\n{analysis}\n")

    print("="*80)
    print("✓ Search complete!")
    print("="*80)


if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    main()
