#!/usr/bin/env python3
"""
Automated Investigation Engine
Systematically analyzes vault data, discovers connections, and generates investigation reports
"""

import json
from typing import Dict, List, Set, Tuple
from datetime import datetime
from vault_api import ObsidianVault
from vault_insights import VaultInsights


class AutomatedInvestigation:
    """Automated investigation system for vault analysis"""

    def __init__(self):
        self.vault = ObsidianVault()
        self.vault.load()
        self.insights = VaultInsights()
        self.report_timestamp = datetime.now()

    def discover_hidden_connections(self) -> Dict:
        """Discover connections that aren't directly documented"""
        connections = {}

        # For each entity, find shared mentions
        for entity1 in self.vault.list_entities():
            connections[entity1] = {}

            for entity2 in self.vault.list_entities():
                if entity1 == entity2:
                    continue

                # Find files that mention both entities
                files_entity1 = set()
                files_entity2 = set()

                for file_path, file in self.vault.loader.files.items():
                    if self._entity_mentioned(entity1, file):
                        files_entity1.add(file_path)
                    if self._entity_mentioned(entity2, file):
                        files_entity2.add(file_path)

                # Shared mentions = indirect connection
                shared_files = files_entity1 & files_entity2
                if shared_files:
                    connections[entity1][entity2] = {
                        'shared_documents': len(shared_files),
                        'files': sorted(list(shared_files)),
                        'strength': len(shared_files) / max(len(files_entity1), len(files_entity2))
                    }

        return connections

    def _entity_mentioned(self, entity_name: str, file) -> bool:
        """Check if entity is mentioned in file"""
        entity_lower = entity_name.lower()
        content_lower = file.content.lower()
        title_lower = file.title.lower()
        return (entity_lower in content_lower or
                entity_lower in title_lower or
                entity_name in file.internal_links)

    def identify_investigation_hotspots(self) -> Dict:
        """Identify key investigation areas and patterns"""
        hotspots = {}

        # Category hotspots
        categories = self.vault.get_statistics()['index_stats']['categories']
        hotspots['categories'] = categories

        # Entity hotspots (most connected)
        connection_strength = self.insights.get_connection_strength()
        hotspots['entity_hubs'] = dict(list(connection_strength.items())[:5])

        # Timeline hotspots
        timeline_mentions = {}
        for file_path in self.vault.list_files():
            if 'timeline' in file_path.lower() or 'timeline' in self.vault.get_file(file_path).title.lower():
                timeline_mentions[file_path] = True

        hotspots['timeline_documents'] = len(timeline_mentions)

        # Evidence hotspots
        evidence_mentions = {}
        for file_path in self.vault.list_files():
            if 'evidence' in file_path.lower():
                evidence_mentions[file_path] = True

        hotspots['evidence_documents'] = len(evidence_mentions)

        # Technology/infrastructure mentions
        tech_keywords = ['network', 'infrastructure', 'domain', 'ip', 'server', 'technology', 'as53616']
        tech_files = {}
        for file_path in self.vault.list_files():
            file = self.vault.get_file(file_path)
            if any(keyword in file.content.lower() for keyword in tech_keywords):
                tech_files[file_path] = sum(1 for keyword in tech_keywords if keyword in file.content.lower())

        hotspots['technology_focus'] = len(tech_files)

        return hotspots

    def analyze_investigation_scope(self) -> Dict:
        """Analyze the overall scope of the investigation"""
        stats = self.vault.get_statistics()

        scope = {
            'total_documents': stats['total_files'],
            'documented_entities': stats['total_entities'],
            'known_relationships': stats['total_relationships'],
            'investigation_areas': stats['index_stats']['categories'],
            'keyword_index': stats['index_stats']['entity_mentions'],
        }

        # Determine investigation phases
        phases = self._determine_investigation_phases()
        scope['investigation_phases'] = phases

        # Scope expansion potential
        scope['scope_expansion_potential'] = self._assess_scope_expansion()

        return scope

    def _determine_investigation_phases(self) -> List[str]:
        """Determine investigation phases based on content"""
        phases = []

        # Check for timeline breadth
        timeline_files = [f for f in self.vault.list_files() if 'timeline' in f.lower()]
        if timeline_files:
            phases.append("Historical Analysis (Timeline tracked)")

        # Check for technical analysis
        tech_files = [f for f in self.vault.list_files() if 'technical' in f.lower()]
        if tech_files:
            phases.append("Technical Infrastructure Analysis")

        # Check for entity analysis
        entity_files = [f for f in self.vault.list_files() if 'entities' in f.lower()]
        if entity_files:
            phases.append("Entity Profiling and Analysis")

        # Check for legal/evidence analysis
        legal_files = [f for f in self.vault.list_files() if 'legal' in f.lower() or 'evidence' in f.lower()]
        if legal_files:
            phases.append("Legal and Evidence Framework")

        # Check for cross-reference analysis
        if 'cross' in ' '.join(self.vault.list_files()).lower():
            phases.append("Cross-Reference Analysis")

        return phases

    def _assess_scope_expansion(self) -> Dict:
        """Assess potential for scope expansion"""
        # Entities with few connections might indicate underdeveloped areas
        connection_strength = self.insights.get_connection_strength()
        isolated = [e for e, c in connection_strength.items() if c <= 2]

        # Unknown connections might indicate expansion areas
        hidden_connections = self.discover_hidden_connections()
        expansion_opportunities = sum(1 for entity_data in hidden_connections.values() if entity_data)

        return {
            'isolated_entities': len(isolated),
            'potential_hidden_connections': expansion_opportunities,
            'underdeveloped_areas': isolated[:5],
            'expansion_score': (len(isolated) + expansion_opportunities) / len(self.vault.list_entities())
        }

    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive automated investigation report"""
        lines = []
        lines.append("="*80)
        lines.append("AUTOMATED INVESTIGATION ANALYSIS REPORT")
        lines.append("="*80)
        lines.append(f"Generated: {self.report_timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        # 1. Executive Summary
        lines.append("1. EXECUTIVE SUMMARY")
        lines.append("-"*80)
        stats = self.vault.get_statistics()
        lines.append(f"Total Investigation Documents: {stats['total_files']}")
        lines.append(f"Documented Entities: {stats['total_entities']}")
        lines.append(f"Known Relationships: {stats['total_relationships']}")
        lines.append("")

        # 2. Investigation Scope
        lines.append("2. INVESTIGATION SCOPE")
        lines.append("-"*80)
        scope = self.analyze_investigation_scope()
        for phase in scope['investigation_phases']:
            lines.append(f"  • {phase}")
        lines.append("")

        # 3. Key Investigation Hotspots
        lines.append("3. INVESTIGATION HOTSPOTS")
        lines.append("-"*80)
        hotspots = self.identify_investigation_hotspots()
        lines.append(f"Primary Categories: {', '.join(hotspots['categories'].keys())}")
        lines.append(f"Top Entity Hubs: {', '.join(list(hotspots['entity_hubs'].keys())[:3])}")
        lines.append(f"Timeline Documents: {hotspots['timeline_documents']}")
        lines.append(f"Evidence Documents: {hotspots['evidence_documents']}")
        lines.append(f"Technology Focus Areas: {hotspots['technology_focus']}")
        lines.append("")

        # 4. Hidden Connection Analysis
        lines.append("4. HIDDEN CONNECTION ANALYSIS")
        lines.append("-"*80)
        hidden = self.discover_hidden_connections()
        major_connection_hubs = {}
        for entity, connections in hidden.items():
            if connections:
                major_connection_hubs[entity] = len(connections)

        top_hubs = sorted(major_connection_hubs.items(), key=lambda x: x[1], reverse=True)[:5]
        for entity, count in top_hubs:
            lines.append(f"  {entity}: {count} indirect connections discovered")
        lines.append("")

        # 5. Scope Expansion Assessment
        lines.append("5. SCOPE EXPANSION POTENTIAL")
        lines.append("-"*80)
        expansion = scope['scope_expansion_potential']
        lines.append(f"Isolated Entities (limited connections): {expansion['isolated_entities']}")
        lines.append(f"Potential Hidden Connections: {expansion['potential_hidden_connections']}")
        lines.append(f"Expansion Score: {expansion['expansion_score']:.2%}")
        lines.append(f"Underdeveloped Areas: {', '.join(expansion['underdeveloped_areas'][:3])}")
        lines.append("")

        # 6. Emerging Investigation Leads
        lines.append("6. EMERGING INVESTIGATION LEADS")
        lines.append("-"*80)
        emerging = self._identify_emerging_leads()
        for i, lead in enumerate(emerging[:5], 1):
            lines.append(f"  {i}. {lead['name']}")
            lines.append(f"     Priority: {lead['priority']}")
            lines.append(f"     Reason: {lead['reason']}")
        lines.append("")

        # 7. Connection Network Analysis
        lines.append("7. KEY CONNECTION NETWORKS")
        lines.append("-"*80)
        networks = self._analyze_connection_networks()
        for network_name, network_data in networks.items():
            lines.append(f"  {network_name}:")
            lines.append(f"    Nodes: {network_data['node_count']}")
            lines.append(f"    Edges: {network_data['edge_count']}")
            lines.append(f"    Density: {network_data['density']:.2f}")
        lines.append("")

        # 8. Investigation Recommendations
        lines.append("8. INVESTIGATION RECOMMENDATIONS")
        lines.append("-"*80)
        recommendations = self._generate_recommendations()
        for i, rec in enumerate(recommendations[:10], 1):
            lines.append(f"  {i}. {rec['action']}")
            lines.append(f"     Priority: {rec['priority']}")
            lines.append(f"     Expected Outcome: {rec['outcome']}")
        lines.append("")

        lines.append("="*80)

        return "\n".join(lines)

    def _identify_emerging_leads(self) -> List[Dict]:
        """Identify emerging investigation leads"""
        leads = []

        # New entities with evidence documents
        for entity in self.vault.list_entities():
            entity_obj = self.vault.get_entity(entity)
            if entity_obj:
                mentions = self.vault.loader.tag_index.get(entity, set())
                if len(mentions) >= 5:
                    leads.append({
                        'name': entity,
                        'priority': 'HIGH' if len(mentions) > 15 else 'MEDIUM',
                        'reason': f'Mentioned in {len(mentions)} documents'
                    })

        # Sort by priority
        return sorted(leads, key=lambda x: {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}[x['priority']])

    def _analyze_connection_networks(self) -> Dict:
        """Analyze the structure of connection networks"""
        networks = {}

        # Get all relationships
        relationships = self.vault.loader.graph.relationships if hasattr(self.vault.loader, 'graph') else []

        # Identify network clusters
        if relationships:
            # Simple clustering based on shared entities
            entity_pairs = {}
            for rel in relationships:
                pair = tuple(sorted([rel.source, rel.target]))
                entity_pairs[pair] = entity_pairs.get(pair, 0) + 1

            networks['primary_network'] = {
                'node_count': len(self.vault.list_entities()),
                'edge_count': len(relationships),
                'density': len(relationships) / (len(self.vault.list_entities()) * (len(self.vault.list_entities()) - 1) / 2) if self.vault.list_entities() else 0
            }

        return networks

    def _generate_recommendations(self) -> List[Dict]:
        """Generate actionable investigation recommendations"""
        recommendations = []

        # Recommendation 1: Focus on high-connection entities
        hubs = self.insights.find_hubs(threshold=3)
        if hubs:
            recommendations.append({
                'action': f'Deep analysis of entity hubs: {", ".join(hubs[:3])}',
                'priority': 'CRITICAL',
                'outcome': 'Identify central figures and decision makers'
            })

        # Recommendation 2: Fill information gaps
        isolated = self.insights.find_isolated_entities()
        if isolated:
            recommendations.append({
                'action': f'Research isolated entities: {", ".join(isolated[:3])}',
                'priority': 'HIGH',
                'outcome': 'Discover missing connections and expand network'
            })

        # Recommendation 3: Timeline reconstruction
        recommendations.append({
            'action': 'Reconstruct complete investigation timeline',
            'priority': 'HIGH',
            'outcome': 'Identify chronological patterns and causality'
        })

        # Recommendation 4: Evidence cross-reference
        recommendations.append({
            'action': 'Systematic cross-reference all evidence documents',
            'priority': 'CRITICAL',
            'outcome': 'Identify corroborating evidence and contradictions'
        })

        # Recommendation 5: Co-mention analysis
        co_mentions = self.insights.find_co_mentioned_entities(limit=20)
        if co_mentions:
            recommendations.append({
                'action': f'Analyze frequently co-mentioned entity pairs',
                'priority': 'MEDIUM',
                'outcome': 'Identify strong associations and working relationships'
            })

        return recommendations

    def run_full_investigation(self) -> Dict:
        """Run complete automated investigation"""
        print("Starting automated investigation...")

        result = {
            'timestamp': self.report_timestamp.isoformat(),
            'scope': self.analyze_investigation_scope(),
            'hotspots': self.identify_investigation_hotspots(),
            'hidden_connections': self.discover_hidden_connections(),
            'emerging_leads': self._identify_emerging_leads(),
            'networks': self._analyze_connection_networks(),
            'recommendations': self._generate_recommendations(),
            'report': self.generate_comprehensive_report()
        }

        return result


if __name__ == '__main__':
    import sys

    print("Automated Investigation Engine v1.0")
    print("="*80)

    investigation = AutomatedInvestigation()
    results = investigation.run_full_investigation()

    # Print report
    print(results['report'])

    # Optionally save results
    if len(sys.argv) > 1 and sys.argv[1] == '--save':
        output_file = sys.argv[2] if len(sys.argv) > 2 else 'investigation_results.json'

        # Don't save the report string to avoid duplication
        save_results = {k: v for k, v in results.items() if k != 'report'}

        with open(output_file, 'w') as f:
            json.dump(save_results, f, indent=2, default=str)

        print(f"\nResults saved to {output_file}")
