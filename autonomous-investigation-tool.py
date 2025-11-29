#!/usr/bin/env python3
"""
Autonomous Investigation Tool v1.0
End-to-end investigation engine for Obsidian vault knowledge management.
Exhaustively traverses, analyzes, and cross-references all files.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set, Tuple
import hashlib

class InvestigationEngine:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.files_analyzed = 0
        self.entities = defaultdict(set)
        self.relationships = []
        self.cross_references = defaultdict(list)
        self.evidence_chain = []
        self.keywords_found = defaultdict(list)
        self.investigation_gaps = []
        self.file_metadata = {}

        # Investigation patterns and keywords
        self.entity_patterns = {
            'organization': r'\b(?:LLC|Inc|Corp|Institute|University|Agency|Department|Lab|Center)\b',
            'person': r'\b(?:Dr\.|Mr\.|Ms\.|Prof\.|Sir\s+)\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b',
            'technology': r'\b(?:DARPA|BRAIN|IoB|Z-File|AI|ML|Network|Protocol|Firmware|Exploit)\b',
            'evidence_marker': r'\b(?:proof|evidence|incident|case|document|patent|timeline|finding)\b',
            'connection_marker': r'\b(?:connected to|linked to|associated with|part of|involved in|relationship)\b'
        }

        # Critical investigation keywords
        self.critical_keywords = [
            'harassment', 'network', 'DARPA', 'BRAIN', 'technology transfer',
            'population control', 'Z-File', 'IoB', 'infrastructure', 'patent',
            'DARPA BRAIN', 'neural', 'monitoring', 'evidence', 'investigation',
            'cross-reference', 'connection', 'entity', 'relationship', 'timeline'
        ]

        # File relevance scoring
        self.file_scores = {}

    def run_complete_investigation(self):
        """Execute complete autonomous investigation."""
        print("=" * 80)
        print("AUTONOMOUS INVESTIGATION TOOL - STARTING COMPLETE ANALYSIS")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        # Phase 1: File Traversal
        print("\n[PHASE 1] FILE TRAVERSAL AND DISCOVERY...")
        self.traverse_all_files()

        # Phase 2: Content Analysis
        print("\n[PHASE 2] CONTENT ANALYSIS AND EXTRACTION...")
        self.analyze_all_content()

        # Phase 3: Entity Identification
        print("\n[PHASE 3] ENTITY IDENTIFICATION AND MAPPING...")
        self.identify_entities()

        # Phase 4: Relationship Discovery
        print("\n[PHASE 4] RELATIONSHIP DISCOVERY AND MAPPING...")
        self.discover_relationships()

        # Phase 5: Cross-Reference Building
        print("\n[PHASE 5] CROSS-REFERENCE BUILDING...")
        self.build_cross_references()

        # Phase 6: Connection Analysis
        print("\n[PHASE 6] DEEP CONNECTION ANALYSIS...")
        self.analyze_connections()

        # Phase 7: Gap Identification
        print("\n[PHASE 7] INVESTIGATION GAP IDENTIFICATION...")
        self.identify_investigation_gaps()

        # Phase 8: Report Generation
        print("\n[PHASE 8] COMPREHENSIVE REPORT GENERATION...")
        self.generate_investigation_report()

        print("\n" + "=" * 80)
        print("INVESTIGATION COMPLETE")
        print("=" * 80)

    def traverse_all_files(self):
        """Exhaustively traverse all files in vault."""
        print(f"\nScanning vault: {self.vault_path}")

        file_count = 0
        for root, dirs, files in os.walk(self.vault_path):
            # Skip git and obsidian directories
            dirs[:] = [d for d in dirs if d not in {'.git', '.obsidian', '__pycache__'}]

            for file in files:
                if file.endswith(('.md', '.json', '.txt', '.log')):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.vault_path)

                    file_count += 1
                    self.file_metadata[str(rel_path)] = {
                        'full_path': str(file_path),
                        'size': file_path.stat().st_size,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        'type': file.split('.')[-1]
                    }

        print(f"✓ Found {file_count} files for analysis")
        self.files_analyzed = file_count

    def analyze_all_content(self):
        """Analyze content from all files."""
        print(f"\nAnalyzing {self.files_analyzed} files...")

        for rel_path, metadata in self.file_metadata.items():
            full_path = metadata['full_path']
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extract keywords
                for keyword in self.critical_keywords:
                    if keyword.lower() in content.lower():
                        count = content.lower().count(keyword.lower())
                        self.keywords_found[keyword].append((rel_path, count))

                # Score file by relevance
                self.file_scores[rel_path] = self.score_file_relevance(content)

            except Exception as e:
                print(f"  ⚠ Error reading {rel_path}: {e}")

        print(f"✓ Content analysis complete")
        print(f"✓ Keywords extracted from {len(self.keywords_found)} categories")

    def score_file_relevance(self, content: str) -> float:
        """Score file relevance to investigation."""
        score = 0

        # Critical keywords worth more
        for keyword in self.critical_keywords:
            occurrences = content.lower().count(keyword.lower())
            if keyword in ['DARPA', 'BRAIN', 'harassment', 'network', 'evidence']:
                score += occurrences * 5
            else:
                score += occurrences * 1

        # Evidence markers
        evidence_count = len(re.findall(r'\b(?:proof|evidence|found|documented|confirmed)\b', content, re.I))
        score += evidence_count * 3

        return score

    def identify_entities(self):
        """Identify and catalog all entities."""
        print(f"\nIdentifying entities from {self.files_analyzed} files...")

        entity_count = 0
        for rel_path, metadata in self.file_metadata.items():
            if not rel_path.endswith('.md'):
                continue

            full_path = metadata['full_path']
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Extract titles and headers
                headers = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
                for header in headers:
                    self.entities['headers'].add(header)
                    entity_count += 1

                # Extract organization names
                orgs = re.findall(r'\b([A-Z][a-z]+ (?:LLC|Inc|Corp|Institute|University|Center|Agency|Department|Lab))\b', content)
                for org in set(orgs):
                    self.entities['organizations'].add(org)
                    entity_count += 1

                # Extract person names
                people = re.findall(r'\b(?:Dr\.|Prof\.|Mr\.|Ms\.|Mrs\.|Sir\s+)?([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', content)
                for person in set(people):
                    self.entities['people'].add(person)
                    entity_count += 1

                # Extract technologies/projects
                techs = re.findall(r'\b(?:DARPA|BRAIN|IoB|Z-File|AI|ML|Project [A-Z][a-z]+)\b', content)
                for tech in set(techs):
                    self.entities['technologies'].add(tech)
                    entity_count += 1

                # Extract URLs and domains
                urls = re.findall(r'https?://[^\s\)]+', content)
                for url in set(urls):
                    self.entities['urls'].add(url)
                    entity_count += 1

                # Extract email addresses
                emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
                for email in set(emails):
                    self.entities['emails'].add(email)
                    entity_count += 1

            except Exception as e:
                print(f"  ⚠ Entity extraction error in {rel_path}: {e}")

        print(f"✓ Identified {entity_count} entities across {len(self.entities)} categories")
        for category, entities in self.entities.items():
            print(f"  - {category}: {len(entities)} unique entities")

    def discover_relationships(self):
        """Discover relationships between entities."""
        print(f"\nDiscovering relationships in {self.files_analyzed} files...")

        relationship_count = 0
        for rel_path, metadata in self.file_metadata.items():
            if not rel_path.endswith('.md'):
                continue

            full_path = metadata['full_path']
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                # Find connection markers with surrounding context
                patterns = [
                    r'([A-Z][a-z][\w\s]+?)\s+(?:connected to|linked to|associated with|partner|collaborat|funded|employed)\s+([A-Z][a-z][\w\s]+?)(?:\.|,|;)',
                    r'([A-Z][a-z][\w\s]+?)\s+and\s+([A-Z][a-z][\w\s]+?)\s+(?:work|collaborate|partner)',
                    r'([A-Z\w\s]+?)\s+(?:uses|develops|creates|manages|operates)\s+([A-Z\w\s]+?)(?:\.|,|;)',
                ]

                for pattern in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        source = match.group(1).strip()
                        target = match.group(2).strip()

                        # Get surrounding context
                        start = max(0, match.start() - 100)
                        end = min(len(content), match.end() + 100)
                        context = content[start:end]

                        relationship = {
                            'source': source,
                            'target': target,
                            'file': str(rel_path),
                            'context': context,
                            'confidence': self.calculate_confidence(source, target, context)
                        }

                        self.relationships.append(relationship)
                        relationship_count += 1

            except Exception as e:
                print(f"  ⚠ Relationship discovery error in {rel_path}: {e}")

        print(f"✓ Discovered {relationship_count} relationships")

    def calculate_confidence(self, source: str, target: str, context: str) -> float:
        """Calculate confidence score for a relationship."""
        score = 0.5  # Base score

        # Strong evidence markers
        strong_markers = ['directly connected', 'confirmed', 'documented', 'evidence', 'proven']
        for marker in strong_markers:
            if marker in context.lower():
                score += 0.15

        # Entity validation
        if source in self.entities.get('organizations', set()) or source in self.entities.get('people', set()):
            score += 0.1
        if target in self.entities.get('organizations', set()) or target in self.entities.get('people', set()):
            score += 0.1

        return min(score, 1.0)

    def build_cross_references(self):
        """Build comprehensive cross-reference index."""
        print(f"\nBuilding cross-reference index...")

        xref_count = 0
        for rel_path, metadata in self.file_metadata.items():
            if not rel_path.endswith('.md'):
                continue

            full_path = metadata['full_path']
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                # Find all internal links and references
                internal_links = re.findall(r'\[\[([^\]]+)\]\]', content)
                external_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

                # Cross-reference entities
                for entity_type, entities in self.entities.items():
                    for entity in entities:
                        if entity in content:
                            self.cross_references[entity].append({
                                'file': str(rel_path),
                                'type': entity_type,
                                'occurrences': content.count(entity),
                                'internal_links': len(internal_links),
                                'external_links': len(external_links)
                            })
                            xref_count += 1

            except Exception as e:
                print(f"  ⚠ Cross-reference error in {rel_path}: {e}")

        print(f"✓ Built cross-reference index with {xref_count} entries")

    def analyze_connections(self):
        """Perform deep connection analysis."""
        print(f"\nPerforming deep connection analysis...")

        # Find connection chains
        connection_chains = 0

        # Build adjacency map
        adjacency = defaultdict(set)
        for rel in self.relationships:
            adjacency[rel['source']].add(rel['target'])
            adjacency[rel['target']].add(rel['source'])

        # Find high-connection entities
        high_connection_entities = sorted(
            [(entity, len(connections)) for entity, connections in adjacency.items()],
            key=lambda x: x[1],
            reverse=True
        )[:20]

        print(f"\n✓ Top connected entities:")
        for entity, conn_count in high_connection_entities:
            print(f"  - {entity}: {conn_count} connections")

        # Analyze evidence chains
        evidence_chain_count = 0
        for rel_path, metadata in self.file_metadata.items():
            if 'EVIDENCE' in rel_path.upper() or 'FRAMEWORK' in rel_path.upper():
                full_path = metadata['full_path']
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Extract numbered evidence items
                    evidence_items = re.findall(r'(?:^|\n)[\d\-\*]+\.\s+([^\n]+)', content)
                    self.evidence_chain.extend([(item, str(rel_path)) for item in evidence_items])
                    evidence_chain_count += len(evidence_items)

                except Exception as e:
                    print(f"  ⚠ Evidence chain error in {rel_path}: {e}")

        print(f"✓ Extracted {evidence_chain_count} evidence items from evidence documents")

    def identify_investigation_gaps(self):
        """Identify gaps and areas for further investigation."""
        print(f"\nIdentifying investigation gaps...")

        gaps = []

        # Gap 1: Entities without sufficient cross-references
        print("\n  Checking entity coverage...")
        for entity_type, entities in self.entities.items():
            for entity in entities:
                xref_count = len(self.cross_references.get(entity, []))
                if xref_count == 0 and entity_type in ['organizations', 'people']:
                    gaps.append({
                        'type': 'uncrossreferenced_entity',
                        'entity': entity,
                        'entity_type': entity_type,
                        'recommendation': f'Add cross-references for {entity} in more documents'
                    })

        # Gap 2: Relationships without context
        print("  Checking relationship documentation...")
        weak_relationships = [rel for rel in self.relationships if rel['confidence'] < 0.6]
        if weak_relationships:
            gaps.append({
                'type': 'weak_relationships',
                'count': len(weak_relationships),
                'recommendation': 'Strengthen evidence for weak relationships'
            })

        # Gap 3: Missing time periods
        print("  Checking timeline coverage...")
        year_pattern = r'\b(19|20)\d{2}\b'
        years_found = set()
        for rel_path, metadata in self.file_metadata.items():
            full_path = metadata['full_path']
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    years = re.findall(year_pattern, content)
                    years_found.update(years)
            except:
                pass

        all_years = set(str(y) for y in range(2010, 2026))
        missing_years = all_years - years_found
        if missing_years:
            gaps.append({
                'type': 'timeline_gaps',
                'missing_years': sorted(missing_years)[-5:],  # Last 5 missing years
                'recommendation': 'Research and document missing years'
            })

        # Gap 4: Document types analysis
        print("  Analyzing document coverage...")
        doc_types = defaultdict(int)
        for rel_path in self.file_metadata.keys():
            if 'Entities' in rel_path:
                doc_types['entity_profiles'] += 1
            elif 'Technical' in rel_path:
                doc_types['technical_analysis'] += 1
            elif 'Analysis' in rel_path:
                doc_types['analysis'] += 1
            elif 'Patents' in rel_path:
                doc_types['patent_research'] += 1

        if doc_types['patent_research'] < 10:
            gaps.append({
                'type': 'insufficient_patent_research',
                'current_count': doc_types.get('patent_research', 0),
                'recommendation': 'Expand patent research and analysis'
            })

        self.investigation_gaps = gaps
        print(f"✓ Identified {len(gaps)} investigation gaps")

    def generate_investigation_report(self):
        """Generate comprehensive investigation report."""
        report_path = self.vault_path / 'AUTONOMOUS_INVESTIGATION_REPORT.md'

        print(f"\nGenerating comprehensive report: {report_path.name}")

        report = []
        report.append("# AUTONOMOUS INVESTIGATION REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Files Analyzed:** {self.files_analyzed}")
        report.append(f"**Analysis Engine:** Autonomous Investigation Tool v1.0")

        # Executive Summary
        report.append("\n## EXECUTIVE SUMMARY\n")
        report.append(f"This report presents findings from autonomous analysis of {self.files_analyzed} files ")
        report.append(f"in the Obsidian investigation vault. The analysis has identified {len(self.entities)} ")
        report.append(f"entity categories, {len(self.relationships)} relationships, and {len(self.investigation_gaps)} ")
        report.append(f"areas requiring further investigation.\n")

        # Files Analyzed
        report.append("\n## FILES ANALYZED\n")
        report.append(f"**Total Files:** {self.files_analyzed}\n")
        for rel_path, metadata in sorted(self.file_metadata.items()):
            report.append(f"- `{rel_path}` ({metadata['size']} bytes, {metadata['type']})")

        # Key Findings - Critical Keywords
        report.append("\n## KEY FINDINGS - CRITICAL KEYWORDS\n")
        sorted_keywords = sorted(self.keywords_found.items(), key=lambda x: sum(c for _, c in x[1]), reverse=True)
        for keyword, occurrences in sorted_keywords[:15]:
            total_count = sum(count for _, count in occurrences)
            files_count = len(occurrences)
            report.append(f"- **{keyword}**: {total_count} mentions across {files_count} files")

        # Entities Identified
        report.append("\n## ENTITIES IDENTIFIED\n")
        for category in sorted(self.entities.keys()):
            entities = sorted(self.entities[category])
            report.append(f"\n### {category.upper()} ({len(entities)} unique)\n")
            for entity in entities[:20]:  # Top 20 per category
                xref_count = len(self.cross_references.get(entity, []))
                report.append(f"- {entity} (cross-referenced in {xref_count} locations)")
            if len(entities) > 20:
                report.append(f"- ... and {len(entities) - 20} more")

        # Relationships Discovered
        report.append("\n## RELATIONSHIPS DISCOVERED\n")
        report.append(f"\n**Total Relationships:** {len(self.relationships)}\n")

        # Top relationships by confidence
        sorted_rels = sorted(self.relationships, key=lambda x: x['confidence'], reverse=True)[:20]
        report.append("### Highest Confidence Relationships\n")
        for rel in sorted_rels:
            report.append(f"- **{rel['source']}** → **{rel['target']}** (Confidence: {rel['confidence']:.2f})")
            report.append(f"  - File: `{rel['file']}`")
            report.append(f"  - Context: {rel['context'][:100]}...")

        # Cross-Reference Index
        report.append("\n## CROSS-REFERENCE INDEX\n")
        sorted_xref = sorted(self.cross_references.items(), key=lambda x: len(x[1]), reverse=True)[:30]
        for entity, references in sorted_xref:
            report.append(f"- **{entity}**: {len(references)} cross-references")
            for ref in references[:3]:
                report.append(f"  - {ref['file']} ({ref['occurrences']} occurrences)")

        # File Relevance Ranking
        report.append("\n## FILE RELEVANCE RANKING\n")
        sorted_files = sorted(self.file_scores.items(), key=lambda x: x[1], reverse=True)[:30]
        report.append("\n### Top Files by Investigation Relevance\n")
        for file_path, score in sorted_files:
            report.append(f"- **{file_path}**: Relevance Score {score:.1f}")

        # Investigation Gaps
        report.append("\n## INVESTIGATION GAPS AND RECOMMENDATIONS\n")
        if self.investigation_gaps:
            for i, gap in enumerate(self.investigation_gaps, 1):
                report.append(f"\n### Gap {i}: {gap['type'].replace('_', ' ').upper()}\n")
                for key, value in gap.items():
                    if key != 'type':
                        report.append(f"- **{key.replace('_', ' ').title()}:** {value}")

        # Evidence Chain Summary
        report.append("\n## EVIDENCE CHAIN SUMMARY\n")
        if self.evidence_chain:
            report.append(f"\n**Total Evidence Items:** {len(self.evidence_chain)}\n")
            report.append("### Sample Evidence Items\n")
            for evidence, file_path in self.evidence_chain[:20]:
                report.append(f"- {evidence}")
                report.append(f"  (From: `{file_path}`)")

        # Connection Hubs
        report.append("\n## CONNECTION HUBS (HIGH-DEGREE NODES)\n")
        adjacency = defaultdict(set)
        for rel in self.relationships:
            adjacency[rel['source']].add(rel['target'])
            adjacency[rel['target']].add(rel['source'])

        high_connection = sorted(adjacency.items(), key=lambda x: len(x[1]), reverse=True)[:15]
        report.append("\n### Entities with Most Connections\n")
        for entity, connections in high_connection:
            report.append(f"- **{entity}**: {len(connections)} connections")
            for connected in list(connections)[:5]:
                report.append(f"  - {connected}")

        # Technology and Infrastructure
        report.append("\n## TECHNOLOGY AND INFRASTRUCTURE IDENTIFIED\n")
        techs = self.entities.get('technologies', set())
        if techs:
            for tech in sorted(techs):
                xref_count = len(self.cross_references.get(tech, []))
                report.append(f"- {tech} (referenced {xref_count} times)")

        # Next Steps
        report.append("\n## RECOMMENDED NEXT STEPS\n")
        report.append("""
1. **Strengthen Weak Relationships:** Add supporting evidence to relationships with confidence < 0.6
2. **Fill Timeline Gaps:** Research and document missing years and periods
3. **Expand Entity Coverage:** Add profiles for unlinked entities
4. **Deep Dives:** Conduct detailed analysis on high-connection entities
5. **Cross-Validation:** Verify findings across multiple independent sources
6. **Continuous Monitoring:** Re-run analysis quarterly to track changes
7. **Pattern Recognition:** Use findings for predictive analysis
8. **Documentation:** Ensure all findings are properly documented with sources
""")

        # Technical Details
        report.append("\n## TECHNICAL ANALYSIS DETAILS\n")
        report.append(f"- Entity Categories: {len(self.entities)}")
        report.append(f"- Total Unique Entities: {sum(len(e) for e in self.entities.values())}")
        report.append(f"- Relationship Chains: {len(self.relationships)}")
        report.append(f"- Cross-Reference Points: {len(self.cross_references)}")
        report.append(f"- Investigation Gaps Identified: {len(self.investigation_gaps)}")
        report.append(f"- Evidence Items Extracted: {len(self.evidence_chain)}")

        # Metadata Summary
        report.append("\n## FILE METADATA SUMMARY\n")
        total_size = sum(m['size'] for m in self.file_metadata.values())
        report.append(f"- Total Storage: {total_size / 1024 / 1024:.2f} MB")

        file_types = defaultdict(int)
        for m in self.file_metadata.values():
            file_types[m['type']] += 1

        report.append("- File Type Distribution:")
        for ftype, count in sorted(file_types.items()):
            report.append(f"  - {ftype}: {count} files")

        report.append(f"\n---\n**Report Generated:** {datetime.now().isoformat()}\n")
        report.append("**End of Report**\n")

        # Write report
        report_content = '\n'.join(report)
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✓ Report generated: {report_path}")
        print(f"  - Analyzed {self.files_analyzed} files")
        print(f"  - {len(self.entities)} entity categories")
        print(f"  - {len(self.relationships)} relationships")
        print(f"  - {len(self.investigation_gaps)} investigation gaps")
        print(f"  - {len(self.evidence_chain)} evidence items")

        # Also generate a detailed JSON output
        self.generate_json_export(report_path.parent)

    def generate_json_export(self, output_dir: Path):
        """Generate detailed JSON export for programmatic access."""
        json_path = output_dir / 'investigation_data.json'

        data = {
            'metadata': {
                'generated': datetime.now().isoformat(),
                'files_analyzed': self.files_analyzed,
                'tool_version': '1.0'
            },
            'entities': {k: list(v) for k, v in self.entities.items()},
            'relationships': self.relationships,
            'cross_references': {k: v for k, v in self.cross_references.items()},
            'file_scores': self.file_scores,
            'investigation_gaps': self.investigation_gaps,
            'keywords': {k: [(f, c) for f, c in v] for k, v in self.keywords_found.items()},
            'evidence_count': len(self.evidence_chain)
        }

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)

        print(f"✓ JSON data export: {json_path}")


def main():
    """Main entry point."""
    vault_path = '/home/user/obsidian-vault'

    engine = InvestigationEngine(vault_path)
    engine.run_complete_investigation()

    print("\n" + "=" * 80)
    print("ALL INVESTIGATION PHASES COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == '__main__':
    main()
