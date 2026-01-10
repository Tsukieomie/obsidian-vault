#!/usr/bin/env python3
"""
Vault Insights Generator
Generates analytical insights and patterns from vault data
"""

import json
from typing import Dict, List, Tuple
from vault_api import ObsidianVault


class VaultInsights:
    """Generate analytical insights from vault data"""

    def __init__(self):
        self.vault = ObsidianVault()
        self.vault.load()

    def get_connection_strength(self) -> Dict[str, int]:
        """Get connection strength between entities"""
        connections = {}
        for entity_name in self.vault.list_entities():
            network = self.vault.get_entity_relationships(entity_name)
            if network:
                connections[entity_name] = len(network['nodes']) - 1  # Exclude self

        return dict(sorted(
            connections.items(),
            key=lambda x: x[1],
            reverse=True
        ))

    def find_hubs(self, threshold: int = 5) -> List[str]:
        """Find highly connected entities (hubs)"""
        connections = self.get_connection_strength()
        return [entity for entity, count in connections.items() if count >= threshold]

    def find_isolated_entities(self) -> List[str]:
        """Find entities with few connections"""
        connections = self.get_connection_strength()
        return [entity for entity, count in connections.items() if count <= 2]

    def get_entity_mention_patterns(self) -> Dict[str, int]:
        """Get entity mention frequency"""
        stats = self.vault.get_statistics()
        return stats['index_stats']['entity_mentions']

    def find_co_mentioned_entities(self, limit: int = 10) -> List[Tuple[str, str, int]]:
        """Find entities frequently mentioned together"""
        co_mentions = {}

        for file_path in self.vault.list_files():
            file = self.vault.get_file(file_path)
            if file:
                # Get all internal links that are entities
                entity_links = []
                for link in file.internal_links:
                    # Try to find entity with this name
                    if any(link.lower() in entity.lower() or entity.lower() in link.lower()
                           for entity in self.vault.list_entities()):
                        entity_links.append(link)

                # Count co-mentions
                for i, entity1 in enumerate(entity_links):
                    for entity2 in entity_links[i+1:]:
                        key = tuple(sorted([entity1, entity2]))
                        co_mentions[key] = co_mentions.get(key, 0) + 1

        # Sort by frequency
        return sorted(co_mentions.items(), key=lambda x: x[1], reverse=True)[:limit]

    def get_category_distribution(self) -> Dict[str, int]:
        """Get file distribution by category"""
        stats = self.vault.get_statistics()
        return stats['index_stats']['categories']

    def get_tag_cloud(self, limit: int = 30) -> Dict[str, int]:
        """Get most frequent tags"""
        tags = self.vault.list_tags()
        return dict(sorted(
            tags.items(),
            key=lambda x: x[1],
            reverse=True
        )[:limit])

    def find_information_density(self) -> Dict[str, float]:
        """Measure information density (links and tags per file)"""
        density = {}

        for file_path in self.vault.list_files():
            file = self.vault.get_file(file_path)
            if file:
                # Count total references
                total_refs = len(file.tags) + len(file.internal_links)
                # Calculate density relative to content length
                content_length = len(file.content)
                if content_length > 0:
                    density_score = total_refs / (content_length / 1000)  # Per 1000 chars
                    density[file.title] = round(density_score, 2)

        return dict(sorted(
            density.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10])

    def get_investigation_metrics(self) -> Dict:
        """Get metrics relevant to investigation documents"""
        metrics = {
            'total_documents': len(self.vault.list_files()),
            'documented_entities': len(self.vault.list_entities()),
            'total_connections': sum(1 for _ in self.vault.loader.graph.relationships) if hasattr(self.vault.loader, 'graph') else 0,
            'average_mentions_per_entity': 0,
        }

        # Calculate average mentions
        mentions = self.get_entity_mention_patterns()
        if mentions:
            metrics['average_mentions_per_entity'] = round(
                sum(mentions.values()) / len(mentions),
                2
            )

        # Find critical entities (most connected + most mentioned)
        connections = self.get_connection_strength()
        entity_mentions = mentions
        critical_score = {}

        for entity in self.vault.list_entities():
            conn_score = connections.get(entity, 0)
            mention_score = entity_mentions.get(entity, 0)
            critical_score[entity] = conn_score * 0.5 + mention_score * 0.5

        metrics['critical_entities'] = [
            entity for entity, score in sorted(
                critical_score.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        ]

        return metrics

    def generate_summary_report(self) -> str:
        """Generate a text summary report"""
        lines = []
        lines.append("="*70)
        lines.append("VAULT INSIGHTS AND ANALYSIS REPORT")
        lines.append("="*70)

        # Overview
        lines.append("\n1. VAULT OVERVIEW")
        lines.append("-" * 70)
        stats = self.vault.get_statistics()
        lines.append(f"Total Files: {stats['total_files']}")
        lines.append(f"Total Entities: {stats['total_entities']}")
        lines.append(f"Total Tags: {stats['total_tags']}")
        lines.append(f"Total Relationships: {stats['total_relationships']}")

        # Categories
        lines.append("\n2. DOCUMENT DISTRIBUTION")
        lines.append("-" * 70)
        categories = self.get_category_distribution()
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  {cat}: {count} files")

        # Hubs
        lines.append("\n3. HIGHLY CONNECTED ENTITIES (HUBS)")
        lines.append("-" * 70)
        hubs = self.find_hubs(threshold=3)
        connections = self.get_connection_strength()
        for entity in hubs[:10]:
            lines.append(f"  {entity}: {connections[entity]} connections")

        # Isolated
        lines.append("\n4. LESS CONNECTED ENTITIES")
        lines.append("-" * 70)
        isolated = self.find_isolated_entities()
        for entity in isolated[:10]:
            conn_count = connections.get(entity, 0)
            lines.append(f"  {entity}: {conn_count} connection(s)")

        # Mention patterns
        lines.append("\n5. TOP MENTIONED ENTITIES")
        lines.append("-" * 70)
        mentions = self.get_entity_mention_patterns()
        for entity, count in sorted(mentions.items(), key=lambda x: x[1], reverse=True)[:10]:
            lines.append(f"  {entity}: {count} mentions")

        # Co-mentions
        lines.append("\n6. FREQUENTLY CO-MENTIONED ENTITY PAIRS")
        lines.append("-" * 70)
        co_mentions = self.find_co_mentioned_entities(limit=5)
        for (entity1, entity2), count in co_mentions:
            lines.append(f"  {entity1} ↔ {entity2}: {count} times")

        # Tag cloud
        lines.append("\n7. TOP TAGS")
        lines.append("-" * 70)
        tags = self.get_tag_cloud(limit=15)
        for tag, count in tags.items():
            lines.append(f"  #{tag}: {count} files")

        # Information density
        lines.append("\n8. HIGH INFORMATION DENSITY FILES")
        lines.append("-" * 70)
        density = self.find_information_density()
        for file_title, score in list(density.items())[:10]:
            lines.append(f"  {file_title}: {score} refs/1K chars")

        # Investigation metrics
        lines.append("\n9. INVESTIGATION METRICS")
        lines.append("-" * 70)
        inv_metrics = self.get_investigation_metrics()
        lines.append(f"Total Documents: {inv_metrics['total_documents']}")
        lines.append(f"Documented Entities: {inv_metrics['documented_entities']}")
        lines.append(f"Avg Mentions per Entity: {inv_metrics['average_mentions_per_entity']}")
        lines.append(f"\nCritical Entities:")
        for entity in inv_metrics['critical_entities']:
            lines.append(f"  - {entity}")

        lines.append("\n" + "="*70)

        return "\n".join(lines)

    def export_as_json(self) -> Dict:
        """Export insights as JSON"""
        return {
            'overview': {
                'file_count': len(self.vault.list_files()),
                'entity_count': len(self.vault.list_entities()),
            },
            'connection_strength': self.get_connection_strength(),
            'hubs': self.find_hubs(),
            'isolated_entities': self.find_isolated_entities(),
            'entity_mentions': self.get_entity_mention_patterns(),
            'category_distribution': self.get_category_distribution(),
            'top_tags': self.get_tag_cloud(limit=50),
            'information_density': self.find_information_density(),
            'investigation_metrics': self.get_investigation_metrics(),
        }


if __name__ == '__main__':
    import sys

    insights = VaultInsights()

    # Generate and print report
    report = insights.generate_summary_report()
    print(report)

    # Optionally save to file
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'vault_insights.json'
        with open(output_file, 'w') as f:
            json.dump(insights.export_as_json(), f, indent=2)
        print(f"\nInsights saved to {output_file}")
