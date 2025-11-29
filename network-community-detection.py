#!/usr/bin/env python3
"""
Network Community Detection
Identifies communities and clusters within the entity network.
"""

import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set

class NetworkCommunityDetection:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.graph = defaultdict(set)
        self.communities = []
        self.community_membership = {}
        self.community_strength = {}
        self.inter_community_links = []

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run network community detection."""
        print("=" * 80)
        print("NETWORK COMMUNITY DETECTION - ENTITY CLUSTERING")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] BUILDING ENTITY NETWORK...")
        self.build_network()

        print("\n[PHASE 2] DETECTING COMMUNITIES...")
        self.detect_communities()

        print("\n[PHASE 3] ANALYZING COMMUNITY STRENGTH...")
        self.analyze_community_strength()

        print("\n[PHASE 4] MAPPING INTER-COMMUNITY LINKS...")
        self.map_inter_community_links()

        print("\n[PHASE 5] GENERATING COMMUNITY REPORT...")
        self.generate_community_report()

        print("\n" + "=" * 80)
        print("NETWORK COMMUNITY DETECTION COMPLETE")
        print("=" * 80)

    def build_network(self):
        """Build entity network from relationships."""
        print(f"\nBuilding entity network...")

        edge_count = 0

        # Add edges from explicit relationships
        relationships = self.investigation_data.get('relationships', [])
        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')
            if source and target:
                self.graph[source].add(target)
                self.graph[target].add(source)
                edge_count += 1

        # Add edges from co-occurrence
        cross_refs = self.investigation_data.get('cross_references', {})
        cooccurrence_edges = 0

        for entity1, refs1 in list(cross_refs.items())[:100]:
            files1 = set(ref['file'] for ref in refs1)

            for entity2, refs2 in list(cross_refs.items())[100:]:
                if entity1 != entity2:
                    files2 = set(ref['file'] for ref in refs2)
                    common_files = len(files1 & files2)

                    if common_files >= 2:
                        self.graph[entity1].add(entity2)
                        self.graph[entity2].add(entity1)
                        cooccurrence_edges += 1

        print(f"✓ Built network with {len(self.graph)} nodes and {edge_count + cooccurrence_edges} edges")

    def detect_communities(self):
        """Detect communities using greedy modularity optimization."""
        print(f"\nDetecting communities...")

        visited = set()
        community_id = 0

        # Simple community detection using BFS
        for node in self.graph:
            if node not in visited:
                community = set()
                queue = [node]

                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue

                    visited.add(current)
                    community.add(current)

                    # Add connected nodes with high connection density
                    for neighbor in self.graph[current]:
                        if neighbor not in visited:
                            # Check if neighbor is well-connected to community
                            connections_in_community = len(self.graph[neighbor] & community)
                            if connections_in_community > 0 or len(community) < 3:
                                queue.append(neighbor)

                if len(community) >= 2:
                    self.communities.append({
                        'id': community_id,
                        'members': list(community),
                        'size': len(community)
                    })

                    for member in community:
                        self.community_membership[member] = community_id

                    community_id += 1

        print(f"✓ Detected {len(self.communities)} communities")

    def analyze_community_strength(self):
        """Analyze strength and cohesion of communities."""
        print(f"\nAnalyzing community strength...")

        for community in self.communities:
            members = community['members']

            # Calculate internal edges
            internal_edges = 0
            for member in members:
                internal_edges += len(self.graph[member] & set(members))

            internal_edges //= 2  # Undirected graph

            # Possible edges
            possible_edges = len(members) * (len(members) - 1) / 2

            # Calculate density
            density = internal_edges / possible_edges if possible_edges > 0 else 0

            # Average degree within community
            avg_degree = 2 * internal_edges / len(members) if members else 0

            self.community_strength[community['id']] = {
                'internal_edges': internal_edges,
                'density': density,
                'avg_degree': avg_degree,
                'size': len(members)
            }

        print(f"✓ Analyzed strength for {len(self.communities)} communities")

    def map_inter_community_links(self):
        """Map links between communities."""
        print(f"\nMapping inter-community links...")

        link_count = 0

        for community in self.communities:
            members = set(community['members'])

            for member in members:
                for neighbor in self.graph[member]:
                    if neighbor not in members:
                        # Link to different community
                        neighbor_community = self.community_membership.get(neighbor)

                        if neighbor_community is not None:
                            self.inter_community_links.append({
                                'from_community': community['id'],
                                'to_community': neighbor_community,
                                'from_entity': member,
                                'to_entity': neighbor
                            })
                            link_count += 1

        print(f"✓ Mapped {link_count} inter-community links")

    def generate_community_report(self):
        """Generate network community report."""
        report_path = self.vault_path / 'NETWORK_COMMUNITY_REPORT.md'

        report = []
        report.append("# NETWORK COMMUNITY DETECTION REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Community Overview
        report.append("## COMMUNITY OVERVIEW\n")
        report.append(f"**Total Communities:** {len(self.communities)}\n")
        report.append(f"**Total Entities:** {len(self.graph)}\n")
        report.append(f"**Inter-Community Links:** {len(self.inter_community_links)}\n")

        # Communities by Size
        report.append("\n## COMMUNITIES BY SIZE\n")
        sorted_communities = sorted(self.communities, key=lambda x: x['size'], reverse=True)

        for community in sorted_communities[:20]:
            cid = community['id']
            strength = self.community_strength.get(cid, {})

            report.append(f"\n### Community {cid}\n")
            report.append(f"- **Size:** {community['size']} entities")
            report.append(f"- **Density:** {strength.get('density', 0):.3f}")
            report.append(f"- **Internal Edges:** {strength.get('internal_edges', 0)}")
            report.append(f"- **Members:**")

            for member in community['members'][:15]:
                report.append(f"  - {member}")

            if len(community['members']) > 15:
                report.append(f"  - ... and {len(community['members']) - 15} more")

        # Community Strength Ranking
        report.append(f"\n## COMMUNITIES BY STRENGTH (DENSITY)\n")
        sorted_by_strength = sorted(self.community_strength.items(),
                                   key=lambda x: x[1]['density'], reverse=True)

        for cid, strength_info in sorted_by_strength[:15]:
            report.append(f"\n- **Community {cid}**")
            report.append(f"  Density: {strength_info['density']:.3f}")
            report.append(f"  Size: {strength_info['size']}")
            report.append(f"  Avg Degree: {strength_info['avg_degree']:.2f}")

        # Inter-Community Bridges
        report.append(f"\n## BRIDGE ENTITIES (INTER-COMMUNITY CONNECTORS)\n")
        bridge_score = defaultdict(int)

        for link in self.inter_community_links:
            bridge_score[link['from_entity']] += 1
            bridge_score[link['to_entity']] += 1

        sorted_bridges = sorted(bridge_score.items(), key=lambda x: x[1], reverse=True)
        for entity, score in sorted_bridges[:30]:
            report.append(f"- **{entity}**: {score} inter-community connections")

        # Community Interactions
        report.append(f"\n## COMMUNITY INTERACTIONS\n")
        community_links = defaultdict(int)

        for link in self.inter_community_links:
            pair = tuple(sorted([link['from_community'], link['to_community']]))
            community_links[pair] += 1

        sorted_links = sorted(community_links.items(), key=lambda x: x[1], reverse=True)
        for (c1, c2), count in sorted_links[:20]:
            report.append(f"- **Community {c1}** ↔ **Community {c2}**: {count} links")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Network community report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    detector = NetworkCommunityDetection(vault_path, data_path)
    detector.run_analysis()


if __name__ == '__main__':
    main()
