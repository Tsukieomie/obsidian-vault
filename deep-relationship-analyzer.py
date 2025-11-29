#!/usr/bin/env python3
"""
Deep Relationship Analyzer
Discovers hidden connections, multi-hop relationships, and complex entity interactions.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple

class DeepRelationshipAnalyzer:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.hidden_connections = []
        self.multi_hop_paths = []
        self.entity_interactions = defaultdict(list)
        self.co_occurrence_graph = defaultdict(set)
        self.influence_scores = {}

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run deep relationship analysis."""
        print("=" * 80)
        print("DEEP RELATIONSHIP ANALYZER - HIDDEN CONNECTIONS AND INTERACTIONS")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] BUILDING CO-OCCURRENCE NETWORK...")
        self.build_co_occurrence_network()

        print("\n[PHASE 2] DISCOVERING HIDDEN CONNECTIONS...")
        self.discover_hidden_connections()

        print("\n[PHASE 3] FINDING MULTI-HOP RELATIONSHIPS...")
        self.find_multi_hop_paths()

        print("\n[PHASE 4] ANALYZING ENTITY INTERACTIONS...")
        self.analyze_entity_interactions()

        print("\n[PHASE 5] CALCULATING INFLUENCE SCORES...")
        self.calculate_influence_scores()

        print("\n[PHASE 6] GENERATING DEEP RELATIONSHIP REPORT...")
        self.generate_deep_report()

        print("\n" + "=" * 80)
        print("DEEP RELATIONSHIP ANALYSIS COMPLETE")
        print("=" * 80)

    def build_co_occurrence_network(self):
        """Build network based on entity co-occurrence in documents."""
        print(f"\nAnalyzing entity co-occurrence patterns...")

        entities_list = []
        for category, ents in self.investigation_data.get('entities', {}).items():
            entities_list.extend(ents)

        co_occurrence_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                # Find co-occurring entities in same document
                found_entities = []
                for entity in entities_list:
                    if entity.lower() in content:
                        found_entities.append(entity)

                # Build co-occurrence graph
                for i, entity1 in enumerate(found_entities):
                    for entity2 in found_entities[i+1:]:
                        self.co_occurrence_graph[entity1].add(entity2)
                        self.co_occurrence_graph[entity2].add(entity1)
                        co_occurrence_count += 1

            except Exception as e:
                pass

        print(f"✓ Found {co_occurrence_count} co-occurrence relationships")

    def discover_hidden_connections(self):
        """Discover hidden connections not explicitly documented."""
        print(f"\nDiscovering hidden connections...")

        hidden_count = 0

        # Look for entities that share many connections but aren't directly related
        for entity1 in list(self.co_occurrence_graph.keys())[:50]:
            connections1 = self.co_occurrence_graph[entity1]

            for entity2 in list(self.co_occurrence_graph.keys())[50:100]:
                if entity1 != entity2:
                    connections2 = self.co_occurrence_graph[entity2]

                    # Calculate Jaccard similarity of connections
                    common = len(connections1 & connections2)
                    total = len(connections1 | connections2)

                    if common > 0 and total > 0:
                        similarity = common / total

                        if similarity > 0.3:  # High connection similarity
                            # Check if directly related
                            relationships = self.investigation_data.get('relationships', [])
                            is_direct = any(
                                (r.get('source') == entity1 and r.get('target') == entity2) or
                                (r.get('source') == entity2 and r.get('target') == entity1)
                                for r in relationships
                            )

                            if not is_direct:
                                self.hidden_connections.append({
                                    'entity1': entity1,
                                    'entity2': entity2,
                                    'similarity': similarity,
                                    'shared_connections': common,
                                    'type': 'indirect_relationship'
                                })
                                hidden_count += 1

        print(f"✓ Discovered {hidden_count} hidden connections")

    def find_multi_hop_paths(self):
        """Find multi-hop relationship paths between entities."""
        print(f"\nFinding multi-hop relationship paths...")

        path_count = 0
        relationships = self.investigation_data.get('relationships', [])

        # Build adjacency for explicit relationships
        adj = defaultdict(set)
        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')
            if source and target:
                adj[source].add(target)
                adj[target].add(source)

        # Find 2-hop and 3-hop paths
        for start_entity in list(adj.keys())[:20]:
            # 2-hop paths
            for intermediate in adj[start_entity]:
                for end in adj[intermediate]:
                    if end != start_entity:
                        # Check if direct connection doesn't exist
                        if end not in adj[start_entity]:
                            self.multi_hop_paths.append({
                                'start': start_entity,
                                'intermediate': intermediate,
                                'end': end,
                                'hops': 2,
                                'path': f"{start_entity} → {intermediate} → {end}"
                            })
                            path_count += 1

        print(f"✓ Found {path_count} multi-hop relationship paths")

    def analyze_entity_interactions(self):
        """Analyze how entities interact with each other."""
        print(f"\nAnalyzing entity interactions...")

        interaction_count = 0
        cross_refs = self.investigation_data.get('cross_references', {})

        for entity, references in cross_refs.items():
            files = [ref['file'] for ref in references]
            co_entities = set()

            # Find other entities in same files
            for file in files:
                for other_entity, other_refs in cross_refs.items():
                    if entity != other_entity:
                        for ref in other_refs:
                            if ref['file'] == file:
                                co_entities.add(other_entity)

            if co_entities:
                self.entity_interactions[entity] = {
                    'count': len(co_entities),
                    'entities': list(co_entities)[:10],
                    'files': len(set(files))
                }
                interaction_count += 1

        print(f"✓ Analyzed {interaction_count} entity interactions")

    def calculate_influence_scores(self):
        """Calculate influence/importance scores for entities."""
        print(f"\nCalculating entity influence scores...")

        score_count = 0

        for entity in self.co_occurrence_graph:
            # Factors in influence:
            # 1. Number of connections
            connections = len(self.co_occurrence_graph[entity])

            # 2. Keyword mentions
            keywords = self.investigation_data.get('keywords', {})
            keyword_score = sum(1 for k, occs in keywords.items()
                               if entity.lower() in k.lower() or
                               any(entity.lower() in str(occ[0]).lower() for occ in occs))

            # 3. Cross-reference count
            cross_refs = self.investigation_data.get('cross_references', {})
            xref_count = len(cross_refs.get(entity, []))

            # Calculate composite score
            influence = (connections * 0.3) + (keyword_score * 0.4) + (xref_count * 0.3)

            self.influence_scores[entity] = {
                'score': influence,
                'connections': connections,
                'keyword_mentions': keyword_score,
                'cross_references': xref_count
            }
            score_count += 1

        print(f"✓ Calculated influence scores for {score_count} entities")

    def generate_deep_report(self):
        """Generate deep relationship analysis report."""
        report_path = self.vault_path / 'DEEP_RELATIONSHIP_ANALYSIS.md'

        report = []
        report.append("# DEEP RELATIONSHIP ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Hidden Connections
        report.append("## HIDDEN CONNECTIONS\n")
        report.append(f"**Total Hidden Connections:** {len(self.hidden_connections)}\n")
        report.append("### High-Similarity Indirect Relationships\n")

        sorted_hidden = sorted(self.hidden_connections, key=lambda x: x['similarity'], reverse=True)
        for conn in sorted_hidden[:30]:
            report.append(f"\n- **{conn['entity1']}** ↔ **{conn['entity2']}**")
            report.append(f"  - Similarity Score: {conn['similarity']:.3f}")
            report.append(f"  - Shared Connections: {conn['shared_connections']}")
            report.append(f"  - Type: {conn['type']}")

        # Multi-Hop Paths
        report.append(f"\n## MULTI-HOP RELATIONSHIP PATHS\n")
        report.append(f"**Total Paths Found:** {len(self.multi_hop_paths)}\n")
        report.append("### 2-Hop and 3-Hop Connections\n")

        for path in self.multi_hop_paths[:30]:
            report.append(f"\n- {path['path']}")
            report.append(f"  Hops: {path['hops']}")

        # Entity Interactions
        report.append(f"\n## ENTITY INTERACTION ANALYSIS\n")
        report.append(f"**Entities with Significant Interactions:** {len(self.entity_interactions)}\n")

        sorted_interactions = sorted(self.entity_interactions.items(),
                                     key=lambda x: x[1]['count'], reverse=True)
        for entity, interaction in sorted_interactions[:30]:
            report.append(f"\n### {entity}\n")
            report.append(f"- Co-occurring Entities: {interaction['count']}")
            report.append(f"- Files Present: {interaction['files']}")
            report.append("- Connected to:")
            for co_entity in interaction['entities'][:5]:
                report.append(f"  - {co_entity}")

        # Influence Scores
        report.append(f"\n## ENTITY INFLUENCE RANKINGS\n")
        report.append("**Top Influential Entities:**\n")

        sorted_influence = sorted(self.influence_scores.items(),
                                  key=lambda x: x[1]['score'], reverse=True)
        for entity, scores in sorted_influence[:30]:
            report.append(f"\n### {entity}\n")
            report.append(f"- Influence Score: {scores['score']:.2f}")
            report.append(f"- Connections: {scores['connections']}")
            report.append(f"- Keyword Mentions: {scores['keyword_mentions']}")
            report.append(f"- Cross-References: {scores['cross_references']}")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Deep relationship report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    analyzer = DeepRelationshipAnalyzer(vault_path, data_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
