#!/usr/bin/env python3
"""
Advanced Pattern Analysis Engine
Identifies suspicious patterns, anomalies, and complex relationships.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple

class PatternAnalyzer:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_investigation_data(investigation_data_path)
        self.patterns_found = []
        self.anomalies = []
        self.suspicious_clusters = []
        self.temporal_patterns = defaultdict(list)

        # Pattern definitions
        self.suspicious_patterns = [
            r'(?:anonymous|hidden|encrypted|offshore|shell|dummy|front)',
            r'(?:monitor|surveil|track|spy|infiltrat|penetrat)',
            r'(?:weapon|military|classified|classified.*project)',
            r'(?:silence|disappear|missing|eliminate|remove|terminate)',
            r'(?:network.*infrastructure|command.*control|C2)',
            r'(?:backdoor|trojan|malware|exploit|vulnerability)',
            r'(?:population.*control|mind.*control|neural.*interfer)',
            r'(?:directed.*energy|microwave|rf|electromagnetic)',
        ]

        # Connection pattern types
        self.connection_patterns = {
            'direct_collaboration': r'(?:collaborate|partner|work\s+together|joint)',
            'funding_relationship': r'(?:fund|sponsor|finance|grant|support)',
            'employment': r'(?:employ|hire|staff|personnel|team)',
            'technology_transfer': r'(?:transfer|share|license|proprietary)',
            'investigation_target': r'(?:investigate|prosecute|charge|suspect|target)',
            'evidence_linkage': r'(?:evidence|proof|document|confirm|verify)',
        }

    def load_investigation_data(self, data_path: str) -> Dict:
        """Load investigation data from JSON export."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load investigation data: {e}")
            return {}

    def run_analysis(self):
        """Run complete pattern analysis."""
        print("=" * 80)
        print("ADVANCED PATTERN ANALYSIS ENGINE")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] IDENTIFYING SUSPICIOUS PATTERNS...")
        self.find_suspicious_patterns()

        print("\n[PHASE 2] DETECTING ANOMALIES...")
        self.detect_anomalies()

        print("\n[PHASE 3] CLUSTERING ANALYSIS...")
        self.perform_clustering_analysis()

        print("\n[PHASE 4] TEMPORAL PATTERN ANALYSIS...")
        self.analyze_temporal_patterns()

        print("\n[PHASE 5] GENERATING PATTERN REPORT...")
        self.generate_pattern_report()

        print("\n" + "=" * 80)
        print("PATTERN ANALYSIS COMPLETE")
        print("=" * 80)

    def find_suspicious_patterns(self):
        """Find suspicious patterns in documents."""
        print(f"\nScanning {len(self.investigation_data.get('keywords', {}))} keyword categories...")

        suspicious_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Check each suspicious pattern
                for pattern in self.suspicious_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Get context
                        start = max(0, match.start() - 80)
                        end = min(len(content), match.end() + 80)
                        context = content[start:end]

                        self.patterns_found.append({
                            'pattern': pattern,
                            'match': match.group(),
                            'file': str(file_path.relative_to(self.vault_path)),
                            'context': context,
                            'severity': self.assess_severity(match.group(), context),
                            'timestamp': datetime.now().isoformat()
                        })
                        suspicious_count += 1

            except Exception as e:
                pass

        print(f"✓ Found {suspicious_count} suspicious pattern occurrences")

    def assess_severity(self, match: str, context: str) -> str:
        """Assess severity of suspicious pattern."""
        high_severity_keywords = [
            'weapon', 'eliminate', 'kill', 'terminate', 'classified',
            'neural', 'mind control', 'population control'
        ]

        for keyword in high_severity_keywords:
            if keyword.lower() in match.lower() or keyword.lower() in context.lower():
                return 'high'

        medium_severity_keywords = ['monitor', 'track', 'surveil', 'network', 'infrastructure']
        for keyword in medium_severity_keywords:
            if keyword.lower() in match.lower() or keyword.lower() in context.lower():
                return 'medium'

        return 'low'

    def detect_anomalies(self):
        """Detect anomalies in data."""
        print(f"\nAnalyzing {len(self.investigation_data.get('entities', {}))} entity categories...")

        # Anomaly 1: Entities with no connections
        entities = {}
        for category, ents in self.investigation_data.get('entities', {}).items():
            entities.update({e: category for e in ents})

        relationships = self.investigation_data.get('relationships', [])
        connected_entities = set()
        for rel in relationships:
            connected_entities.add(rel.get('source', ''))
            connected_entities.add(rel.get('target', ''))

        isolated_entities = set(entities.keys()) - connected_entities
        for entity in list(isolated_entities)[:30]:  # Top 30
            self.anomalies.append({
                'type': 'isolated_entity',
                'entity': entity,
                'entity_type': entities.get(entity, 'unknown'),
                'description': f'{entity} appears in vault but has no documented connections'
            })

        # Anomaly 2: Files with unusual metadata
        print("  Checking file metadata anomalies...")
        for file_path, metadata in self.investigation_data.get('file_metadata', {}).items():
            if metadata['size'] > 1000000:  # > 1MB
                self.anomalies.append({
                    'type': 'unusually_large_file',
                    'file': file_path,
                    'size': metadata['size'],
                    'description': f'File {file_path} is unusually large'
                })

        # Anomaly 3: Keywords appearing in unexpected frequencies
        print("  Checking keyword frequency anomalies...")
        keywords = self.investigation_data.get('keywords', {})
        for keyword, occurrences in keywords.items():
            total_count = sum(c for _, c in occurrences)
            if total_count > 100:  # Unusually high frequency
                self.anomalies.append({
                    'type': 'high_frequency_keyword',
                    'keyword': keyword,
                    'frequency': total_count,
                    'description': f'Keyword "{keyword}" appears {total_count} times (unusually high)'
                })

        print(f"✓ Detected {len(self.anomalies)} anomalies")

    def perform_clustering_analysis(self):
        """Perform clustering analysis on entities."""
        print(f"\nAnalyzing entity clusters...")

        relationships = self.investigation_data.get('relationships', [])

        # Build adjacency
        adjacency = defaultdict(set)
        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')
            if source and target:
                adjacency[source].add(target)
                adjacency[target].add(source)

        # Simple clustering - find groups of interconnected entities
        visited = set()
        cluster_id = 0

        for entity in adjacency:
            if entity not in visited:
                cluster = set()
                queue = [entity]

                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue

                    visited.add(current)
                    cluster.add(current)

                    for neighbor in adjacency.get(current, []):
                        if neighbor not in visited:
                            queue.append(neighbor)

                if len(cluster) > 2:  # Only report clusters with 3+ entities
                    self.suspicious_clusters.append({
                        'cluster_id': cluster_id,
                        'size': len(cluster),
                        'entities': list(cluster),
                        'density': self.calculate_cluster_density(cluster, adjacency)
                    })
                    cluster_id += 1

        print(f"✓ Identified {len(self.suspicious_clusters)} entity clusters")

    def calculate_cluster_density(self, cluster: Set[str], adjacency: Dict) -> float:
        """Calculate density of a cluster."""
        if len(cluster) <= 1:
            return 0

        edges = 0
        for entity in cluster:
            for neighbor in adjacency.get(entity, []):
                if neighbor in cluster:
                    edges += 1

        # Undirected graph
        max_edges = len(cluster) * (len(cluster) - 1) / 2
        return edges / 2 / max_edges if max_edges > 0 else 0

    def analyze_temporal_patterns(self):
        """Analyze temporal patterns in investigation."""
        print(f"\nAnalyzing temporal patterns...")

        # Extract dates from files
        date_pattern = r'(\d{4})-(\d{2})-(\d{2})'
        years = defaultdict(int)
        months = defaultdict(int)

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                matches = re.finditer(date_pattern, content)
                for match in matches:
                    year = int(match.group(1))
                    month = int(match.group(2))

                    years[year] += 1
                    months[f"{year}-{month:02d}"] += 1

            except Exception as e:
                pass

        # Identify temporal gaps
        if years:
            min_year = min(years.keys())
            max_year = max(years.keys())

            for year in range(min_year, max_year + 1):
                if year not in years or years[year] == 0:
                    self.temporal_patterns['gap'].append({
                        'year': year,
                        'description': f'No documentation for year {year}'
                    })

        print(f"✓ Identified temporal patterns across {len(years)} years")

    def generate_pattern_report(self):
        """Generate detailed pattern analysis report."""
        report_path = self.vault_path / 'PATTERN_ANALYSIS_REPORT.md'

        report = []
        report.append("# PATTERN ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Suspicious Patterns
        report.append("\n## SUSPICIOUS PATTERNS DETECTED\n")
        report.append(f"**Total Occurrences:** {len(self.patterns_found)}\n")

        # Group by severity
        high_severity = [p for p in self.patterns_found if p['severity'] == 'high']
        medium_severity = [p for p in self.patterns_found if p['severity'] == 'medium']
        low_severity = [p for p in self.patterns_found if p['severity'] == 'low']

        report.append(f"\n### High Severity ({len(high_severity)})\n")
        for pattern in high_severity[:20]:
            report.append(f"- **{pattern['match']}** (File: {pattern['file']})")
            report.append(f"  Context: {pattern['context'][:100]}...")

        report.append(f"\n### Medium Severity ({len(medium_severity)})\n")
        for pattern in medium_severity[:20]:
            report.append(f"- **{pattern['match']}** (File: {pattern['file']})")

        # Anomalies
        report.append(f"\n## ANOMALIES DETECTED\n")
        report.append(f"**Total Anomalies:** {len(self.anomalies)}\n")

        # Group by type
        anomaly_types = defaultdict(list)
        for anomaly in self.anomalies:
            anomaly_types[anomaly['type']].append(anomaly)

        for atype, anomalies in anomaly_types.items():
            report.append(f"\n### {atype.replace('_', ' ').upper()} ({len(anomalies)})\n")
            for anomaly in anomalies[:10]:
                report.append(f"- {anomaly.get('description', 'N/A')}")

        # Entity Clusters
        report.append(f"\n## ENTITY CLUSTERS\n")
        report.append(f"**Total Clusters:** {len(self.suspicious_clusters)}\n")

        sorted_clusters = sorted(self.suspicious_clusters, key=lambda x: x['density'], reverse=True)
        for cluster in sorted_clusters[:15]:
            report.append(f"\n### Cluster {cluster['cluster_id']} (Density: {cluster['density']:.2f})\n")
            report.append(f"**Size:** {cluster['size']} entities\n")
            report.append("**Members:**\n")
            for entity in cluster['entities'][:10]:
                report.append(f"- {entity}")

        # Temporal Analysis
        report.append(f"\n## TEMPORAL ANALYSIS\n")
        if self.temporal_patterns.get('gap'):
            report.append("\n### Documentation Gaps by Year\n")
            for gap in sorted(self.temporal_patterns['gap'], key=lambda x: x['year'])[:20]:
                report.append(f"- {gap['description']}")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Pattern report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    analyzer = PatternAnalyzer(vault_path, data_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
