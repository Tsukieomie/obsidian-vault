#!/usr/bin/env python3
"""
Example: Analyze Your Vault with Claude

This script demonstrates how to use Claude to analyze your entire vault
and generate insights.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from claude_integration import ClaudeObsidianIntegration


def main():
    print("\n" + "="*80)
    print("Vault Analysis with Claude")
    print("="*80)

    # Initialize
    integration = ClaudeObsidianIntegration()
    connector = integration.connector

    # Get vault stats
    stats = connector.get_vault_stats()
    print(f"\nAnalyzing vault:")
    print(f"  📝 {stats['total_notes']} notes")
    print(f"  📊 {stats['total_words']:,} words")
    print(f"  🏷️  {stats['unique_tags']} tags")

    # Analyze by top tags
    print("\n" + "-"*80)
    print("Analyzing notes by popular tags...")
    print("-"*80)

    all_tags = connector.get_all_tags()
    top_tags = list(all_tags.keys())[:3]  # Top 3 tags

    for tag in top_tags:
        print(f"\n📌 Analyzing tag: #{tag}")
        notes = connector.search_by_tag(tag)
        print(f"   Found {len(notes)} notes")

        if len(notes) > 0:
            print(f"   Generating analysis...")
            report = integration.batch_analyze_by_tag(tag, save_report=True)
            print(f"   ✓ Analysis complete!")

    print("\n" + "="*80)
    print("✓ Vault analysis complete!")
    print("="*80)
    print("\nCheck the Analysis/ folder for generated reports.")


if __name__ == '__main__':
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)

    main()
