#!/usr/bin/env python3
"""
Obsidian Vault CLI Tool

Command-line interface for interacting with your Obsidian vault using the connector.

Usage:
    python vault_cli.py stats                    # Show vault statistics
    python vault_cli.py list [pattern]           # List notes (optional pattern)
    python vault_cli.py read <path>              # Read a specific note
    python vault_cli.py search <query>           # Search for text
    python vault_cli.py tags <tag>               # Find notes by tag
    python vault_cli.py alltags                  # Show all tags
    python vault_cli.py backlinks <title>        # Find backlinks to a note
    python vault_cli.py create <path> <content>  # Create a new note
"""

import sys
import json
from obsidian_connector import ObsidianConnector


def print_note_info(note):
    """Print formatted note information"""
    print(f"\nTitle: {note.title}")
    print(f"Path: {note.path}")
    print(f"Words: {note.word_count}")
    print(f"Tags: {', '.join(note.tags) if note.tags else 'None'}")
    print(f"Links: {', '.join(note.links) if note.links else 'None'}")
    print(f"Created: {note.created}")
    print(f"Modified: {note.modified}")
    print(f"\nContent Preview:")
    print("-" * 80)
    print(note.content[:500])
    if len(note.content) > 500:
        print(f"\n... ({len(note.content) - 500} more characters)")
    print("-" * 80)


def cmd_stats(connector):
    """Show vault statistics"""
    stats = connector.get_vault_stats()
    print("\n=== Vault Statistics ===")
    print(f"Total Notes: {stats['total_notes']}")
    print(f"Total Words: {stats['total_words']:,}")
    print(f"Unique Tags: {stats['unique_tags']}")
    print(f"Unique Links: {stats['unique_links']}")
    print(f"Vault Path: {stats['vault_path']}")


def cmd_list(connector, pattern="**/*.md"):
    """List all notes"""
    notes = connector.list_notes(pattern)
    print(f"\n=== Found {len(notes)} notes ===")
    for note in notes:
        print(f"  {note}")


def cmd_read(connector, note_path):
    """Read a specific note"""
    try:
        note = connector.read_note(note_path)
        print_note_info(note)
    except FileNotFoundError:
        print(f"Error: Note not found: {note_path}")
        sys.exit(1)


def cmd_search(connector, query):
    """Search for text in notes"""
    results = connector.search_notes(query)
    print(f"\n=== Found {len(results)} notes matching '{query}' ===")

    for result in results:
        print(f"\n{result['path']} ({result['match_count']} matches)")
        for match in result['matches'][:3]:  # Show first 3 matches
            print(f"  Line {match['line_number']}: {match['line'][:100]}")
        if result['match_count'] > 3:
            print(f"  ... and {result['match_count'] - 3} more matches")


def cmd_tags(connector, tag):
    """Find notes by tag"""
    notes = connector.search_by_tag(tag)
    print(f"\n=== Found {len(notes)} notes with #{tag} ===")

    for note in notes:
        print(f"\n{note.path}")
        print(f"  Title: {note.title}")
        print(f"  Words: {note.word_count}")
        print(f"  Tags: {', '.join(note.tags)}")


def cmd_alltags(connector):
    """Show all tags with counts"""
    tags = connector.get_all_tags()
    print(f"\n=== All Tags ({len(tags)} unique) ===")

    for tag, count in tags.items():
        print(f"  #{tag:30} {count:3} notes")


def cmd_backlinks(connector, title):
    """Find backlinks to a note"""
    backlinks = connector.get_backlinks(title)
    print(f"\n=== Found {len(backlinks)} notes linking to '{title}' ===")

    for note in backlinks:
        print(f"\n{note.path}")
        print(f"  Title: {note.title}")
        print(f"  Tags: {', '.join(note.tags) if note.tags else 'None'}")


def cmd_create(connector, note_path, content):
    """Create a new note"""
    try:
        full_path = connector.write_note(note_path, content)
        print(f"\nNote created successfully:")
        print(f"  Path: {note_path}")
        print(f"  Full path: {full_path}")
    except Exception as e:
        print(f"Error creating note: {e}")
        sys.exit(1)


def show_usage():
    """Show usage information"""
    print(__doc__)
    sys.exit(1)


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 2:
        show_usage()

    # Initialize connector
    connector = ObsidianConnector()

    # Parse command
    command = sys.argv[1].lower()

    try:
        if command == "stats":
            cmd_stats(connector)

        elif command == "list":
            pattern = sys.argv[2] if len(sys.argv) > 2 else "**/*.md"
            cmd_list(connector, pattern)

        elif command == "read":
            if len(sys.argv) < 3:
                print("Error: Missing note path")
                print("Usage: vault_cli.py read <path>")
                sys.exit(1)
            cmd_read(connector, sys.argv[2])

        elif command == "search":
            if len(sys.argv) < 3:
                print("Error: Missing search query")
                print("Usage: vault_cli.py search <query>")
                sys.exit(1)
            cmd_search(connector, sys.argv[2])

        elif command == "tags":
            if len(sys.argv) < 3:
                print("Error: Missing tag name")
                print("Usage: vault_cli.py tags <tag>")
                sys.exit(1)
            cmd_tags(connector, sys.argv[2])

        elif command == "alltags":
            cmd_alltags(connector)

        elif command == "backlinks":
            if len(sys.argv) < 3:
                print("Error: Missing note title")
                print("Usage: vault_cli.py backlinks <title>")
                sys.exit(1)
            cmd_backlinks(connector, sys.argv[2])

        elif command == "create":
            if len(sys.argv) < 4:
                print("Error: Missing note path or content")
                print("Usage: vault_cli.py create <path> <content>")
                sys.exit(1)
            cmd_create(connector, sys.argv[2], sys.argv[3])

        else:
            print(f"Error: Unknown command '{command}'")
            show_usage()

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
