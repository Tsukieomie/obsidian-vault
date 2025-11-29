#!/usr/bin/env python3
"""
Keyword Co-occurrence Analyzer
Analyzes keyword patterns and co-occurrence relationships to identify thematic clusters.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple

class KeywordCooccurrenceAnalyzer:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.keyword_pairs = defaultdict(int)
        self.keyword_networks = defaultdict(set)
        self.thematic_clusters = []
        self.keyword_strength = {}
        self.document_themes = {}

        # Critical keywords organized by theme
        self.themes = {
            'surveillance': ['surveil', 'monitor', 'track', 'spy', 'observe'],
            'neural': ['neural', 'brain', 'cognitive', 'neuron', 'synapse'],
            'control': ['control', 'manipulat', 'influence', 'coerce', 'command'],
            'military': ['military', 'weapon', 'combat', 'defense', 'warfare'],
            'technology': ['technology', 'infrastructure', 'network', 'system', 'protocol'],
            'evidence': ['evidence', 'proof', 'documented', 'confirmed', 'verified'],
            'darpa': ['DARPA', 'BRAIN', 'Initiative', 'program', 'project'],
            'population': ['population', 'control', 'health', 'pandemic', 'crisis']
        }

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run keyword co-occurrence analysis."""
        print("=" * 80)
        print("KEYWORD CO-OCCURRENCE ANALYZER - THEMATIC CLUSTERING")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] ANALYZING KEYWORD PAIRS...")
        self.analyze_keyword_pairs()

        print("\n[PHASE 2] BUILDING KEYWORD NETWORKS...")
        self.build_keyword_networks()

        print("\n[PHASE 3] IDENTIFYING THEMATIC CLUSTERS...")
        self.identify_thematic_clusters()

        print("\n[PHASE 4] ANALYZING DOCUMENT THEMES...")
        self.analyze_document_themes()

        print("\n[PHASE 5] CALCULATING KEYWORD STRENGTH...")
        self.calculate_keyword_strength()

        print("\n[PHASE 6] GENERATING KEYWORD CO-OCCURRENCE REPORT...")
        self.generate_cooccurrence_report()

        print("\n" + "=" * 80)
        print("KEYWORD CO-OCCURRENCE ANALYSIS COMPLETE")
        print("=" * 80)

    def analyze_keyword_pairs(self):
        """Analyze co-occurrence of keyword pairs."""
        print(f"\nAnalyzing keyword pair co-occurrence...")

        pair_count = 0
        all_keywords = []

        for theme, keywords in self.themes.items():
            all_keywords.extend(keywords)

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                # Find co-occurring keyword pairs
                found_keywords = []
                for keyword in all_keywords:
                    if keyword.lower() in content:
                        found_keywords.append(keyword)

                # Count pairs
                for i, kw1 in enumerate(found_keywords):
                    for kw2 in found_keywords[i+1:]:
                        pair = tuple(sorted([kw1, kw2]))
                        self.keyword_pairs[pair] += 1
                        pair_count += 1

            except Exception as e:
                pass

        print(f"✓ Analyzed {pair_count} keyword pair co-occurrences")

    def build_keyword_networks(self):
        """Build networks of related keywords."""
        print(f"\nBuilding keyword networks...")

        network_count = 0

        for (kw1, kw2), count in self.keyword_pairs.items():
            if count > 1:  # At least 2 co-occurrences
                self.keyword_networks[kw1].add(kw2)
                self.keyword_networks[kw2].add(kw1)
                network_count += 1

        print(f"✓ Built keyword networks with {network_count} connections")

    def identify_thematic_clusters(self):
        """Identify thematic clusters based on keyword co-occurrence."""
        print(f"\nIdentifying thematic clusters...")

        cluster_count = 0

        for theme, keywords in self.themes.items():
            theme_keywords = set(keywords)
            connected = set()

            # Find all keywords connected to theme keywords
            for kw in keywords:
                connected.add(kw)
                connected.update(self.keyword_networks.get(kw, set()))

            if len(connected) > len(theme_keywords):
                self.thematic_clusters.append({
                    'theme': theme,
                    'core_keywords': keywords,
                    'extended_keywords': list(connected),
                    'size': len(connected)
                })
                cluster_count += 1

        print(f"✓ Identified {cluster_count} thematic clusters")

    def analyze_document_themes(self):
        """Analyze which documents belong to which themes."""
        print(f"\nAnalyzing document themes...")

        doc_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()

                # Calculate theme scores
                theme_scores = {}
                for theme, keywords in self.themes.items():
                    score = sum(content.count(kw.lower()) for kw in keywords)
                    if score > 0:
                        theme_scores[theme] = score

                if theme_scores:
                    rel_path = str(file_path.relative_to(self.vault_path))
                    primary_theme = max(theme_scores, key=theme_scores.get)
                    self.document_themes[rel_path] = {
                        'primary_theme': primary_theme,
                        'theme_scores': theme_scores
                    }
                    doc_count += 1

            except Exception as e:
                pass

        print(f"✓ Analyzed themes for {doc_count} documents")

    def calculate_keyword_strength(self):
        """Calculate strength and importance of keywords."""
        print(f"\nCalculating keyword strength...")

        strength_count = 0

        for theme, keywords in self.themes.items():
            for keyword in keywords:
                # Factors in strength:
                # 1. Network size (how many other keywords it connects to)
                network_size = len(self.keyword_networks.get(keyword, set()))

                # 2. Co-occurrence frequency
                total_cooccurrences = sum(count for (kw1, kw2), count in self.keyword_pairs.items()
                                         if kw1 == keyword or kw2 == keyword)

                # 3. Mention frequency across vault
                keywords_data = self.investigation_data.get('keywords', {})
                mention_count = sum(count for k, occs in keywords_data.items()
                                  if keyword.lower() in k.lower())

                # Composite strength
                strength = (network_size * 0.3) + (total_cooccurrences * 0.4) + (mention_count * 0.3)

                self.keyword_strength[keyword] = {
                    'theme': theme,
                    'strength': strength,
                    'network_size': network_size,
                    'cooccurrence_count': total_cooccurrences,
                    'mentions': mention_count
                }
                strength_count += 1

        print(f"✓ Calculated strength for {strength_count} keywords")

    def generate_cooccurrence_report(self):
        """Generate keyword co-occurrence report."""
        report_path = self.vault_path / 'KEYWORD_COOCCURRENCE_REPORT.md'

        report = []
        report.append("# KEYWORD CO-OCCURRENCE ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Thematic Clusters
        report.append("## THEMATIC CLUSTERS\n")
        for cluster in sorted(self.thematic_clusters, key=lambda x: x['size'], reverse=True):
            report.append(f"\n### {cluster['theme'].upper()}\n")
            report.append(f"**Core Keywords:** {', '.join(cluster['core_keywords'])}\n")
            report.append(f"**Extended Network:** {len(cluster['extended_keywords'])} keywords")
            report.append(f"\nExtended Keywords:")
            for kw in cluster['extended_keywords'][:15]:
                strength = self.keyword_strength.get(kw, {})
                if strength:
                    report.append(f"- {kw} (strength: {strength.get('strength', 0):.2f})")

        # Keyword Strength Ranking
        report.append(f"\n## KEYWORD STRENGTH RANKING\n")
        sorted_keywords = sorted(self.keyword_strength.items(),
                                key=lambda x: x[1]['strength'], reverse=True)

        for keyword, strength_info in sorted_keywords[:40]:
            report.append(f"\n### {keyword}\n")
            report.append(f"- **Theme:** {strength_info['theme']}")
            report.append(f"- **Strength:** {strength_info['strength']:.2f}")
            report.append(f"- **Network Connections:** {strength_info['network_size']}")
            report.append(f"- **Co-occurrence Count:** {strength_info['cooccurrence_count']}")
            report.append(f"- **Total Mentions:** {strength_info['mentions']}")

        # Top Co-occurring Pairs
        report.append(f"\n## TOP CO-OCCURRING KEYWORD PAIRS\n")
        sorted_pairs = sorted(self.keyword_pairs.items(), key=lambda x: x[1], reverse=True)

        for (kw1, kw2), count in sorted_pairs[:30]:
            report.append(f"- **{kw1}** + **{kw2}**: {count} co-occurrences")

        # Document Themes
        report.append(f"\n## DOCUMENTS BY PRIMARY THEME\n")
        themes_docs = defaultdict(list)
        for doc, theme_info in self.document_themes.items():
            themes_docs[theme_info['primary_theme']].append(doc)

        for theme in sorted(themes_docs.keys()):
            report.append(f"\n### {theme.upper()}\n")
            for doc in themes_docs[theme][:10]:
                report.append(f"- {doc}")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Keyword co-occurrence report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    analyzer = KeywordCooccurrenceAnalyzer(vault_path, data_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
