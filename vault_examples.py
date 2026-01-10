#!/usr/bin/env python3
"""
Vault API Usage Examples
Demonstrates how to use the Obsidian vault API programmatically
"""

from vault_api import ObsidianVault


def example_basic_usage():
    """Example 1: Basic vault usage"""
    print("="*70)
    print("EXAMPLE 1: Basic Usage")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Get vault statistics
    stats = vault.get_statistics()
    print(f"\nVault contains {stats['total_files']} files and {stats['total_entities']} entities")

    # List some files
    print("\nSample files:")
    files = vault.list_files()[:5]
    for file_path in files:
        file = vault.get_file(file_path)
        print(f"  - {file.title}")

    print()


def example_search():
    """Example 2: Search functionality"""
    print("="*70)
    print("EXAMPLE 2: Search Functionality")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Search for something
    query = "investigation"
    print(f"\nSearching for '{query}'...\n")
    results = vault.search(query, limit=5)

    for i, result in enumerate(results, 1):
        print(f"{i}. {result.title}")
        print(f"   Match type: {result.match_type}")
        print(f"   Relevance: {result.relevance:.2f}")

    print()


def example_entity_analysis():
    """Example 3: Entity analysis"""
    print("="*70)
    print("EXAMPLE 3: Entity Analysis")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Pick an entity
    entity_name = "Junyuan Wang"
    print(f"\nAnalyzing entity: {entity_name}\n")

    # Get entity info
    info = vault.get_entity_info(entity_name)
    if info:
        print(f"Name: {info['name']}")
        print(f"Type: {info['type']}")
        print(f"Mentioned in {info['mentions_count']} documents")
        print(f"Tags: {', '.join(info['tags'][:5])}")

        # Show connected entities
        print(f"\nConnected to:")
        for entity in info['network']['nodes']:
            if entity != entity_name:
                print(f"  - {entity}")

    print()


def example_relationship_analysis():
    """Example 4: Relationship analysis"""
    print("="*70)
    print("EXAMPLE 4: Relationship Analysis")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    entity1 = "Junyuan Wang"
    entity2 = "Asymptote Network LLC"

    print(f"\nFinding relationships between '{entity1}' and '{entity2}'...\n")

    # Find common connections
    common = vault.find_common_connections(entity1, entity2)
    if common:
        print(f"Common connections:")
        for entity in common:
            print(f"  - {entity}")
    else:
        print("No common connections found")

    # Find path
    path = vault.find_path(entity1, entity2)
    if path:
        print(f"\nConnection path:")
        print(" → ".join(path))
    else:
        print("\nNo direct connection path found")

    print()


def example_category_browsing():
    """Example 5: Browse by category"""
    print("="*70)
    print("EXAMPLE 5: Browse by Category")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Get files in Analysis category
    category = "Analysis"
    print(f"\nFiles in '{category}' category:\n")

    files = vault.list_files(category=category)
    for file_path in files:
        file = vault.get_file(file_path)
        print(f"  - {file.title}")
        if file.tags:
            print(f"    Tags: {', '.join(sorted(list(file.tags))[:3])}")

    print()


def example_tag_analysis():
    """Example 6: Tag analysis"""
    print("="*70)
    print("EXAMPLE 6: Tag Analysis")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    tags = vault.list_tags()
    print(f"\nTop 10 tags by frequency:\n")

    for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  #{tag}: {count} files")

    # Get files by tag
    tag = "investigation"
    print(f"\n\nFiles tagged with '#{tag}':\n")
    files = vault.get_files_by_tag(tag)
    for file_path in files[:5]:
        file = vault.get_file(file_path)
        print(f"  - {file.title}")

    if len(files) > 5:
        print(f"  ... and {len(files)-5} more")

    print()


def example_related_files():
    """Example 7: Find related files"""
    print("="*70)
    print("EXAMPLE 7: Find Related Files")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Find file
    file_title = "Junyuan Wang"
    file = vault.get_file_by_title(file_title)

    if file:
        print(f"\nFiles related to '{file.title}':\n")

        related = vault.find_related_files(file.relative_path, limit=5)
        for i, (file_path, score) in enumerate(related, 1):
            related_file = vault.get_file(file_path)
            if related_file:
                print(f"{i}. {related_file.title}")
                print(f"   Similarity score: {score:.2f}")

    print()


def example_data_export():
    """Example 8: Export data"""
    print("="*70)
    print("EXAMPLE 8: Export Data")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Export as JSON
    data = vault.export_as_json()
    print(f"\nExported vault data contains:")
    print(f"  - Metadata")
    print(f"  - File count: {data['metadata']['file_count']}")
    print(f"  - Entity count: {data['metadata']['entity_count']}")
    print(f"  - Summary information")

    print()


def example_programmatic_queries():
    """Example 9: Programmatic queries"""
    print("="*70)
    print("EXAMPLE 9: Programmatic Queries")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Find all entities of a specific type
    print("\nAll people entities:\n")
    for entity_name in vault.list_entities():
        entity = vault.get_entity(entity_name)
        if entity and entity.entity_type == "Person":
            print(f"  - {entity.name}")

    # Find frequently mentioned entities
    print("\n\nMost frequently mentioned entities:\n")
    entity_mentions = vault.get_statistics()['index_stats']['entity_mentions']
    for entity, count in sorted(entity_mentions.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  {entity}: {count} mentions")

    print()


def example_advanced_analysis():
    """Example 10: Advanced analysis"""
    print("="*70)
    print("EXAMPLE 10: Advanced Analysis")
    print("="*70)

    vault = ObsidianVault()
    vault.load()

    # Get network around multiple entities
    entities = ["Junyuan Wang", "Brandon Han", "Chris Wang Oklahoma"]
    print(f"\nNetwork analysis of {len(entities)} people:\n")

    all_connections = set()
    for entity_name in entities:
        info = vault.get_entity_info(entity_name)
        if info:
            all_connections.update(info['network']['nodes'])

    print(f"Total entities in network: {len(all_connections)}")
    print("\nAll connected entities:")
    for entity in sorted(all_connections):
        if entity not in entities:
            print(f"  - {entity}")

    print()


if __name__ == '__main__':
    # Run all examples
    examples = [
        example_basic_usage,
        example_search,
        example_entity_analysis,
        example_relationship_analysis,
        example_category_browsing,
        example_tag_analysis,
        example_related_files,
        example_data_export,
        example_programmatic_queries,
        example_advanced_analysis,
    ]

    for example_func in examples:
        example_func()
        input("Press Enter to continue to next example...")

    print("\n✓ All examples completed!")
