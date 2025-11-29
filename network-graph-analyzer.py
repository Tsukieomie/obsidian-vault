#!/usr/bin/env python3
"""
Network Graph Analysis Tool
Builds and analyzes network graphs of entities and relationships.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set

class NetworkGraphAnalyzer:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.graph = defaultdict(set)
        self.edge_weights = defaultdict(int)
        self.node_properties = {}
        self.centrality_scores = {}
        self.shortest_paths = {}

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run complete network analysis."""
        print("=" * 80)
        print("NETWORK GRAPH ANALYSIS ENGINE")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] BUILDING NETWORK GRAPH...")
        self.build_graph()

        print("\n[PHASE 2] CALCULATING CENTRALITY MEASURES...")
        self.calculate_centrality()

        print("\n[PHASE 3] IDENTIFYING BRIDGES AND HUBS...")
        self.identify_bridges_and_hubs()

        print("\n[PHASE 4] ANALYZING NETWORK PROPERTIES...")
        self.analyze_network_properties()

        print("\n[PHASE 5] GENERATING NETWORK REPORT...")
        self.generate_network_report()

        print("\n" + "=" * 80)
        print("NETWORK ANALYSIS COMPLETE")
        print("=" * 80)

    def build_graph(self):
        """Build network graph from relationships."""
        print(f"\nBuilding network graph...")

        relationships = self.investigation_data.get('relationships', [])

        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')
            confidence = rel.get('confidence', 0.5)

            if source and target:
                self.graph[source].add(target)
                self.graph[target].add(source)

                # Weight edges by confidence
                edge_key = tuple(sorted([source, target]))
                self.edge_weights[edge_key] += max(1, int(confidence * 10))

        # Add entity-based connections
        entities = self.investigation_data.get('entities', {})
        cross_refs = self.investigation_data.get('cross_references', {})

        for entity, references in cross_refs.items():
            if len(references) > 5:  # Significant presence
                # Connect to entities in same files
                for ref in references[:5]:
                    file_path = ref.get('file', '')
                    # This is a simple co-occurrence
                    self.node_properties[entity] = {
                        'occurrences': ref.get('occurrences', 0),
                        'files': len(references)
                    }

        print(f"✓ Built graph with {len(self.graph)} nodes and {len(self.edge_weights)} edges")

    def calculate_centrality(self):
        """Calculate various centrality measures."""
        print(f"\nCalculating centrality measures...")

        # Degree centrality
        for node in self.graph:
            self.centrality_scores[node] = {
                'degree': len(self.graph[node]),
                'degree_centrality': len(self.graph[node]) / (len(self.graph) - 1) if len(self.graph) > 1 else 0
            }

        # Identify hubs (high degree nodes)
        hubs = sorted(self.centrality_scores.items(), key=lambda x: x[1]['degree'], reverse=True)[:20]

        print(f"✓ Calculated centrality for {len(self.centrality_scores)} nodes")
        print(f"\n  Top 10 Hubs (by degree):")
        for node, scores in hubs[:10]:
            print(f"    - {node}: {scores['degree']} connections")

    def identify_bridges_and_hubs(self):
        """Identify bridge nodes and network hubs."""
        print(f"\nIdentifying critical network nodes...")

        bridges = []
        hubs = []

        # Find nodes that connect different clusters
        node_degrees = {node: len(connections) for node, connections in self.graph.items()}

        # High-degree nodes are hubs
        avg_degree = sum(node_degrees.values()) / len(node_degrees) if node_degrees else 0
        for node, degree in node_degrees.items():
            if degree > avg_degree * 2:
                hubs.append((node, degree))

        # Simple bridge detection (nodes with balanced connections to different groups)
        for node in self.graph:
            if node_degrees[node] >= 3:
                # Check if connections reach different parts of graph
                neighbors = list(self.graph[node])
                if len(set(neighbors)) > 1:
                    bridges.append((node, node_degrees[node]))

        print(f"✓ Identified {len(hubs)} hubs and {len(bridges)} potential bridges")

    def analyze_network_properties(self):
        """Analyze overall network properties."""
        print(f"\nAnalyzing network properties...")

        # Network density
        if len(self.graph) > 1:
            actual_edges = len(self.edge_weights)
            possible_edges = len(self.graph) * (len(self.graph) - 1) / 2
            density = actual_edges / possible_edges if possible_edges > 0 else 0
        else:
            density = 0

        # Clustering coefficient (simplified)
        clustering_coeffs = []
        for node in list(self.graph.keys())[:50]:  # Sample
            neighbors = self.graph[node]
            if len(neighbors) > 1:
                edges_in_neighborhood = 0
                for n1 in neighbors:
                    for n2 in neighbors:
                        if n2 in self.graph.get(n1, set()):
                            edges_in_neighborhood += 1
                coeff = edges_in_neighborhood / (len(neighbors) * (len(neighbors) - 1)) if len(neighbors) > 1 else 0
                clustering_coeffs.append(coeff)

        avg_clustering = sum(clustering_coeffs) / len(clustering_coeffs) if clustering_coeffs else 0

        print(f"  Network Density: {density:.3f}")
        print(f"  Avg Clustering Coefficient: {avg_clustering:.3f}")
        print(f"  Avg Connections per Node: {sum(node_degrees.values()) / len(node_degrees) if (node_degrees := dict(zip(range(len(self.graph)), [len(c) for c in self.graph.values()]))) else 0:.1f}")

    def generate_network_report(self):
        """Generate network analysis report."""
        report_path = self.vault_path / 'NETWORK_ANALYSIS_REPORT.md'

        report = []
        report.append("# NETWORK GRAPH ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Network Overview
        report.append("## NETWORK OVERVIEW\n")
        report.append(f"- **Total Nodes:** {len(self.graph)}")
        report.append(f"- **Total Edges:** {len(self.edge_weights)}")
        report.append(f"- **Unique Relationships:** {len(set(self.edge_weights.keys()))}")

        # Central Nodes
        report.append("\n## CENTRAL NODES (HUBS)\n")
        report.append("\nMost connected entities in the network:\n")

        sorted_centrality = sorted(self.centrality_scores.items(), key=lambda x: x[1]['degree'], reverse=True)
        for node, scores in sorted_centrality[:30]:
            report.append(f"- **{node}**: {scores['degree']} connections (Centrality: {scores['degree_centrality']:.3f})")

        # Periphery Nodes
        report.append("\n## PERIPHERAL NODES\n")
        report.append("\nLow-connectivity entities:\n")

        low_degree = sorted(self.centrality_scores.items(), key=lambda x: x[1]['degree'])[:20]
        for node, scores in low_degree:
            if scores['degree'] > 0:
                report.append(f"- **{node}**: {scores['degree']} connection(s)")

        # Isolated Nodes
        isolated = [node for node in self.graph if len(self.graph[node]) == 0]
        if isolated:
            report.append(f"\n## ISOLATED NODES ({len(isolated)})\n")
            report.append("Entities with no documented connections:\n")
            for node in isolated[:20]:
                report.append(f"- {node}")

        # Heaviest Weighted Edges
        report.append("\n## STRONGEST RELATIONSHIPS\n")
        report.append("\nHighest-confidence connections:\n")

        sorted_edges = sorted(self.edge_weights.items(), key=lambda x: x[1], reverse=True)[:20]
        for (node1, node2), weight in sorted_edges:
            report.append(f"- **{node1}** ↔ **{node2}** (Weight: {weight})")

        # Network Statistics
        report.append("\n## NETWORK STATISTICS\n")
        node_degrees = {node: len(connections) for node, connections in self.graph.items()}
        if node_degrees:
            report.append(f"- **Avg Degree:** {sum(node_degrees.values()) / len(node_degrees):.2f}")
            report.append(f"- **Max Degree:** {max(node_degrees.values())}")
            report.append(f"- **Min Degree:** {min(node_degrees.values())}")

        # Recommendations
        report.append("\n## INVESTIGATION RECOMMENDATIONS\n")
        report.append("""
1. **Focus on Hubs:** High-degree nodes are critical to the investigation network
2. **Bridge Analysis:** Nodes connecting different clusters may reveal cross-domain connections
3. **Isolated Entities:** Investigate why certain entities lack connections
4. **Strong Relationships:** Verify the strongest connections with primary evidence
5. **Network Gaps:** Look for missing connections that would explain investigative questions
6. **Temporal Analysis:** Map network changes over time
""")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Network report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    analyzer = NetworkGraphAnalyzer(vault_path, data_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
