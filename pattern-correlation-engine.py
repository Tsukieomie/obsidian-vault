#!/usr/bin/env python3
"""
Pattern Correlation Engine
Correlates suspicious patterns across documents and identifies pattern clusters.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set

class PatternCorrelationEngine:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.pattern_correlations = []
        self.pattern_clusters = defaultdict(list)
        self.file_pattern_vectors = {}
        self.pattern_strength_matrix = defaultdict(dict)

        self.suspicious_patterns = [
            'surveil', 'monitor', 'track', 'spy', 'infiltrat',
            'weapon', 'military', 'classified', 'eliminate', 'terminate',
            'neural', 'brain', 'control', 'population',
            'network', 'infrastructure', 'backdoor', 'malware',
            'evidence', 'proof', 'documented', 'confirmed'
        ]

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run pattern correlation analysis."""
        print("=" * 80)
        print("PATTERN CORRELATION ENGINE - DEEP PATTERN ANALYSIS")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] BUILDING PATTERN VECTORS...")
        self.build_pattern_vectors()

        print("\n[PHASE 2] CORRELATING PATTERNS ACROSS DOCUMENTS...")
        self.correlate_patterns()

        print("\n[PHASE 3] CLUSTERING SIMILAR PATTERNS...")
        self.cluster_patterns()

        print("\n[PHASE 4] ANALYZING PATTERN STRENGTH...")
        self.analyze_pattern_strength()

        print("\n[PHASE 5] IDENTIFYING PATTERN HOTSPOTS...")
        self.identify_pattern_hotspots()

        print("\n[PHASE 6] GENERATING PATTERN CORRELATION REPORT...")
        self.generate_correlation_report()

        print("\n" + "=" * 80)
        print("PATTERN CORRELATION ANALYSIS COMPLETE")
        print("=" * 80)

    def build_pattern_vectors(self):
        """Build pattern vectors for each document."""
        print(f"\nBuilding pattern vectors for documents...")

        vector_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                # Create pattern vector
                pattern_vector = {}
                for pattern in self.suspicious_patterns:
                    count = content.count(pattern)
                    if count > 0:
                        pattern_vector[pattern] = count

                if pattern_vector:
                    rel_path = str(file_path.relative_to(self.vault_path))
                    self.file_pattern_vectors[rel_path] = pattern_vector
                    vector_count += 1

            except Exception as e:
                pass

        print(f"✓ Built pattern vectors for {vector_count} documents")

    def correlate_patterns(self):
        """Correlate patterns across documents."""
        print(f"\nCorrelating patterns across {len(self.file_pattern_vectors)} documents...")

        correlation_count = 0

        files = list(self.file_pattern_vectors.keys())
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                vector1 = self.file_pattern_vectors[file1]
                vector2 = self.file_pattern_vectors[file2]

                # Calculate pattern overlap
                common_patterns = set(vector1.keys()) & set(vector2.keys())

                if len(common_patterns) > 0:
                    # Calculate correlation strength
                    strength = len(common_patterns) / len(set(vector1.keys()) | set(vector2.keys()))

                    if strength > 0.3:
                        self.pattern_correlations.append({
                            'file1': file1,
                            'file2': file2,
                            'common_patterns': list(common_patterns),
                            'strength': strength,
                            'pattern_count': len(common_patterns)
                        })
                        correlation_count += 1

        print(f"✓ Found {correlation_count} correlated pattern groups")

    def cluster_patterns(self):
        """Cluster similar patterns together."""
        print(f"\nClustering similar patterns...")

        cluster_count = 0

        for pattern in self.suspicious_patterns:
            files_with_pattern = []

            for file_path, vector in self.file_pattern_vectors.items():
                if pattern in vector:
                    files_with_pattern.append({
                        'file': file_path,
                        'count': vector[pattern]
                    })

            if len(files_with_pattern) > 2:
                sorted_files = sorted(files_with_pattern, key=lambda x: x['count'], reverse=True)
                self.pattern_clusters[pattern] = sorted_files
                cluster_count += 1

        print(f"✓ Created {cluster_count} pattern clusters")

    def analyze_pattern_strength(self):
        """Analyze strength of pattern associations."""
        print(f"\nAnalyzing pattern strength associations...")

        for file_path, vector in self.file_pattern_vectors.items():
            patterns = list(vector.keys())

            for i, pattern1 in enumerate(patterns):
                for pattern2 in patterns[i+1:]:
                    key = tuple(sorted([pattern1, pattern2]))
                    count1 = vector[pattern1]
                    count2 = vector[pattern2]

                    # Co-occurrence strength
                    strength = min(count1, count2) / max(count1, count2)

                    if key not in self.pattern_strength_matrix[pattern1]:
                        self.pattern_strength_matrix[pattern1][pattern2] = []

                    self.pattern_strength_matrix[pattern1][pattern2].append({
                        'file': file_path,
                        'strength': strength
                    })

    def identify_pattern_hotspots(self):
        """Identify files with high concentration of suspicious patterns."""
        print(f"\nIdentifying pattern hotspots...")

        hotspot_count = 0

        for file_path, vector in self.file_pattern_vectors.items():
            total_pattern_count = sum(vector.values())

            if total_pattern_count > 20:  # High threshold
                hotspot_count += 1

    def generate_correlation_report(self):
        """Generate pattern correlation report."""
        report_path = self.vault_path / 'PATTERN_CORRELATION_REPORT.md'

        report = []
        report.append("# PATTERN CORRELATION REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Pattern Correlations
        report.append("## CORRELATED PATTERN GROUPS\n")
        report.append(f"**Total Correlations:** {len(self.pattern_correlations)}\n")

        sorted_correlations = sorted(self.pattern_correlations,
                                     key=lambda x: x['strength'], reverse=True)
        for corr in sorted_correlations[:30]:
            report.append(f"\n### Correlation Strength: {corr['strength']:.3f}\n")
            report.append(f"- **File 1:** {corr['file1']}")
            report.append(f"- **File 2:** {corr['file2']}")
            report.append(f"- **Common Patterns:** {', '.join(corr['common_patterns'])}")
            report.append(f"- **Pattern Count:** {corr['pattern_count']}")

        # Pattern Clusters
        report.append(f"\n## PATTERN CLUSTERS\n")
        report.append(f"**Total Clusters:** {len(self.pattern_clusters)}\n")

        for pattern, files in sorted(self.pattern_clusters.items(),
                                     key=lambda x: len(x[1]), reverse=True):
            report.append(f"\n### Pattern: {pattern}\n")
            report.append(f"**Files with Pattern:** {len(files)}\n")

            for file_info in files[:10]:
                report.append(f"- {file_info['file']} ({file_info['count']} occurrences)")

        # Pattern Associations
        report.append(f"\n## PATTERN ASSOCIATIONS\n")
        report.append("Patterns that frequently co-occur:\n")

        for pattern1, associations in sorted(self.pattern_strength_matrix.items())[:10]:
            report.append(f"\n### {pattern1}\n")
            for pattern2, occurrences in associations.items():
                if occurrences:
                    avg_strength = sum(o['strength'] for o in occurrences) / len(occurrences)
                    report.append(f"- Co-occurs with **{pattern2}** (strength: {avg_strength:.3f})")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Pattern correlation report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    engine = PatternCorrelationEngine(vault_path, data_path)
    engine.run_analysis()


if __name__ == '__main__':
    main()
