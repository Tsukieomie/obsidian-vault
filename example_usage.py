#!/usr/bin/env python3
"""
Example Usage of Obsidian-Claude Connector

This script demonstrates common use cases for the connector.
Run this to test your setup and see what's possible.
"""

from obsidian_connector import ObsidianConnector
import json


def example_1_basic_stats():
    """Example 1: Get basic vault statistics"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Vault Statistics")
    print("="*80)

    connector = ObsidianConnector()
    stats = connector.get_vault_stats()

    print(f"\nYour vault contains:")
    print(f"  📝 {stats['total_notes']} notes")
    print(f"  📊 {stats['total_words']:,} words")
    print(f"  🏷️  {stats['unique_tags']} unique tags")
    print(f"  🔗 {stats['unique_links']} unique links")
    print(f"  📁 Located at: {stats['vault_path']}")


def example_2_search():
    """Example 2: Search for content"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Search for Content")
    print("="*80)

    connector = ObsidianConnector()
    query = "investigation"

    results = connector.search_notes(query)
    print(f"\nFound {len(results)} notes containing '{query}':")

    for result in results[:5]:  # Show first 5
        print(f"\n📄 {result['title']}")
        print(f"   Path: {result['path']}")
        print(f"   Matches: {result['match_count']}")
        if result['matches']:
            print(f"   Preview: {result['matches'][0]['line'][:80]}...")


def example_3_tags():
    """Example 3: Work with tags"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Tag Analysis")
    print("="*80)

    connector = ObsidianConnector()

    # Get all tags
    all_tags = connector.get_all_tags()
    print(f"\nTop 10 most used tags:")
    for tag, count in list(all_tags.items())[:10]:
        print(f"  #{tag:25} → {count:2} notes")

    # Find notes with specific tag
    if all_tags:
        top_tag = list(all_tags.keys())[0]
        tagged_notes = connector.search_by_tag(top_tag)
        print(f"\nNotes tagged with #{top_tag}:")
        for note in tagged_notes[:3]:
            print(f"  • {note.title} ({note.word_count} words)")


def example_4_links():
    """Example 4: Analyze links and backlinks"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Link Analysis")
    print("="*80)

    connector = ObsidianConnector()

    # Find most linked notes
    link_counts = {}
    for path in connector.list_notes():
        note = connector.read_note(path)
        backlinks = connector.get_backlinks(note.title)
        link_counts[note.title] = len(backlinks)

    print("\nTop 10 most linked-to notes:")
    for title, count in sorted(link_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
        if count > 0:
            print(f"  {title:40} ← {count} backlinks")


def example_5_read_note():
    """Example 5: Read a specific note"""
    print("\n" + "="*80)
    print("EXAMPLE 5: Read a Note")
    print("="*80)

    connector = ObsidianConnector()

    # Get first note
    notes = connector.list_notes()
    if notes:
        note_path = notes[0]
        note = connector.read_note(note_path)

        print(f"\nNote: {note.title}")
        print(f"Path: {note.path}")
        print(f"Words: {note.word_count}")
        print(f"Tags: {', '.join(note.tags) if note.tags else 'None'}")
        print(f"Links: {', '.join(note.links[:5]) if note.links else 'None'}")
        if len(note.links) > 5:
            print(f"       ... and {len(note.links) - 5} more")
        print(f"\nContent preview (first 300 chars):")
        print("-" * 80)
        print(note.content[:300])
        if len(note.content) > 300:
            print("...")
        print("-" * 80)


def example_6_create_note():
    """Example 6: Create a new note"""
    print("\n" + "="*80)
    print("EXAMPLE 6: Create a New Note")
    print("="*80)

    connector = ObsidianConnector()

    # Create a test note
    test_content = """# Connector Test Note

This note was created by the Obsidian-Claude connector!

## Features Demonstrated
- ✅ Note creation
- ✅ Markdown formatting
- ✅ Tag assignment

## Test Data
This is a test note created to demonstrate the connector's capabilities.

#test #connector #demo
"""

    try:
        path = connector.write_note('Test/Connector Test.md', test_content)
        print(f"\n✅ Successfully created test note!")
        print(f"   Path: Test/Connector Test.md")
        print(f"   Full path: {path}")

        # Read it back
        note = connector.read_note('Test/Connector Test.md')
        print(f"\n📄 Note verification:")
        print(f"   Title: {note.title}")
        print(f"   Tags: {', '.join(note.tags)}")
        print(f"   Words: {note.word_count}")

    except Exception as e:
        print(f"❌ Error creating note: {e}")


def example_7_knowledge_graph():
    """Example 7: Build a simple knowledge graph"""
    print("\n" + "="*80)
    print("EXAMPLE 7: Knowledge Graph")
    print("="*80)

    connector = ObsidianConnector()

    # Build graph data
    graph = {}
    print("\nBuilding knowledge graph...")

    for path in connector.list_notes()[:10]:  # Sample 10 notes
        note = connector.read_note(path)
        backlinks = connector.get_backlinks(note.title)

        graph[note.title] = {
            'words': note.word_count,
            'tags': len(note.tags),
            'outbound': len(note.links),
            'inbound': len(backlinks)
        }

    # Show graph
    print(f"\nSample knowledge graph (10 notes):")
    print(f"{'Note':<40} {'Words':<8} {'Tags':<6} {'Out':<5} {'In':<5}")
    print("-" * 70)

    for title, data in graph.items():
        print(f"{title[:38]:<40} {data['words']:<8} {data['tags']:<6} {data['outbound']:<5} {data['inbound']:<5}")


def main():
    """Run all examples"""
    print("\n" + "="*80)
    print(" "*25 + "OBSIDIAN-CLAUDE CONNECTOR")
    print(" "*30 + "Example Usage")
    print("="*80)

    try:
        example_1_basic_stats()
        example_2_search()
        example_3_tags()
        example_4_links()
        example_5_read_note()
        example_6_create_note()
        example_7_knowledge_graph()

        print("\n" + "="*80)
        print("✅ All examples completed successfully!")
        print("="*80)
        print("\nNext steps:")
        print("  • Read CONNECTOR_GUIDE.md for full API documentation")
        print("  • Try the CLI: python vault_cli.py --help")
        print("  • Import the connector in your own scripts")
        print("  • Integrate with Claude API for AI-powered analysis")
        print("\n")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
