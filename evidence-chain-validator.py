#!/usr/bin/env python3
"""
Evidence Chain Validator
Validates evidence chains, checks logical consistency, and identifies evidence gaps.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

class EvidenceChainValidator:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.evidence_chains = defaultdict(list)
        self.chain_validity = {}
        self.missing_links = []
        self.circular_references = []
        self.evidence_strength = {}

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_validation(self):
        """Run evidence chain validation."""
        print("=" * 80)
        print("EVIDENCE CHAIN VALIDATOR - CHAIN INTEGRITY AND CONSISTENCY CHECK")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] EXTRACTING EVIDENCE CHAINS...")
        self.extract_evidence_chains()

        print("\n[PHASE 2] VALIDATING CHAIN LOGIC...")
        self.validate_chain_logic()

        print("\n[PHASE 3] CHECKING FOR CIRCULAR REFERENCES...")
        self.check_circular_references()

        print("\n[PHASE 4] IDENTIFYING MISSING LINKS...")
        self.identify_missing_links()

        print("\n[PHASE 5] CALCULATING EVIDENCE STRENGTH...")
        self.calculate_evidence_strength()

        print("\n[PHASE 6] GENERATING EVIDENCE CHAIN REPORT...")
        self.generate_chain_report()

        print("\n" + "=" * 80)
        print("EVIDENCE CHAIN VALIDATION COMPLETE")
        print("=" * 80)

    def extract_evidence_chains(self):
        """Extract evidence chains from investigation."""
        print(f"\nExtracting evidence chains from investigation data...")

        chain_count = 0
        relationships = self.investigation_data.get('relationships', [])

        # For each relationship, trace back to evidence
        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')
            file_source = rel.get('file', '')

            if source and target:
                chain_id = f"{source}-{target}"
                self.evidence_chains[chain_id] = {
                    'source': source,
                    'target': target,
                    'source_file': file_source,
                    'confidence': rel.get('confidence', 0.5),
                    'context': rel.get('context', '')[:100],
                    'strength': 'weak'
                }
                chain_count += 1

        # Cross-reference with direct evidence
        cross_refs = self.investigation_data.get('cross_references', {})
        for entity, references in cross_refs.items():
            files_mentioned = [ref['file'] for ref in references]

            for file in files_mentioned:
                chain_id = f"entity-{entity}-{file}"
                self.evidence_chains[chain_id] = {
                    'entity': entity,
                    'file': file,
                    'occurrences': sum(ref['occurrences'] for ref in references if ref['file'] == file),
                    'type': 'entity_reference'
                }
                chain_count += 1

        print(f"✓ Extracted {chain_count} evidence chains")

    def validate_chain_logic(self):
        """Validate logical consistency of evidence chains."""
        print(f"\nValidating evidence chain logic...")

        valid_count = 0
        invalid_count = 0

        for chain_id, chain in self.evidence_chains.items():
            if 'source' in chain and 'target' in chain:
                # Check if chain has supporting evidence
                source = chain['source']
                target = chain['target']

                cross_refs = self.investigation_data.get('cross_references', {})
                source_refs = len(cross_refs.get(source, []))
                target_refs = len(cross_refs.get(target, []))

                confidence = chain.get('confidence', 0.5)

                # Validation rules
                if source_refs > 2 and target_refs > 2 and confidence > 0.6:
                    validity = 'valid'
                    valid_count += 1
                elif source_refs > 0 and target_refs > 0 and confidence > 0.4:
                    validity = 'partially_valid'
                    valid_count += 1
                else:
                    validity = 'invalid'
                    invalid_count += 1

                self.chain_validity[chain_id] = {
                    'validity': validity,
                    'source_refs': source_refs,
                    'target_refs': target_refs,
                    'confidence': confidence
                }

        print(f"✓ Valid chains: {valid_count}, Invalid: {invalid_count}")

    def check_circular_references(self):
        """Check for circular reference patterns."""
        print(f"\nChecking for circular references...")

        circular_count = 0

        # Build directed graph
        graph = defaultdict(set)
        for chain_id, chain in self.evidence_chains.items():
            if 'source' in chain and 'target' in chain:
                graph[chain['source']].add(chain['target'])

        # Look for cycles using DFS
        def has_cycle(node, visited, rec_stack):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor, visited, rec_stack):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        visited = set()
        for node in graph:
            if node not in visited:
                if has_cycle(node, visited, set()):
                    self.circular_references.append(node)
                    circular_count += 1

        print(f"✓ Found {circular_count} circular reference patterns")

    def identify_missing_links(self):
        """Identify missing links in evidence chains."""
        print(f"\nIdentifying missing links...")

        missing_count = 0

        for chain_id, chain in self.evidence_chains.items():
            if 'source' in chain and 'target' in chain:
                source = chain['source']
                target = chain['target']
                confidence = chain.get('confidence', 0.5)

                # If confidence is low, likely missing links
                if confidence < 0.5:
                    self.missing_links.append({
                        'chain': chain_id,
                        'source': source,
                        'target': target,
                        'gap': f"Low confidence connection ({confidence:.2f})"
                    })
                    missing_count += 1

                # Check for intermediate entities
                cross_refs = self.investigation_data.get('cross_references', {})
                for intermediate, refs in cross_refs.items():
                    if intermediate != source and intermediate != target:
                        source_same_file = any(
                            ref['file'] == chain.get('source_file', '')
                            for ref in refs
                        )
                        if source_same_file:
                            # Potential missing intermediate link
                            pass

        print(f"✓ Identified {len(self.missing_links)} missing links")

    def calculate_evidence_strength(self):
        """Calculate strength of evidence for each chain."""
        print(f"\nCalculating evidence strength for chains...")

        for chain_id, chain in self.evidence_chains.items():
            if 'source' in chain and 'target' in chain:
                source = chain['source']
                target = chain['target']

                # Factors in strength:
                cross_refs = self.investigation_data.get('cross_references', {})
                source_refs = len(cross_refs.get(source, []))
                target_refs = len(cross_refs.get(target, []))
                confidence = chain.get('confidence', 0.5)

                # Weighted calculation
                strength = (source_refs * 0.2) + (target_refs * 0.2) + (confidence * 10)

                self.evidence_strength[chain_id] = {
                    'strength': strength,
                    'factors': {
                        'source_documentation': source_refs,
                        'target_documentation': target_refs,
                        'confidence': confidence
                    }
                }

    def generate_chain_report(self):
        """Generate evidence chain validation report."""
        report_path = self.vault_path / 'EVIDENCE_CHAIN_REPORT.md'

        report = []
        report.append("# EVIDENCE CHAIN VALIDATION REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Chain Validity Summary
        report.append("## CHAIN VALIDITY SUMMARY\n")
        valid = sum(1 for v in self.chain_validity.values() if v['validity'] == 'valid')
        partial = sum(1 for v in self.chain_validity.values() if v['validity'] == 'partially_valid')
        invalid = sum(1 for v in self.chain_validity.values() if v['validity'] == 'invalid')

        report.append(f"- **Valid Chains:** {valid}")
        report.append(f"- **Partially Valid:** {partial}")
        report.append(f"- **Invalid Chains:** {invalid}")

        # Valid Chains
        report.append(f"\n## VALID EVIDENCE CHAINS\n")
        valid_chains = [k for k, v in self.chain_validity.items() if v['validity'] == 'valid']

        for chain_id in valid_chains[:20]:
            chain = self.evidence_chains[chain_id]
            report.append(f"\n- **{chain.get('source', '')}** → **{chain.get('target', '')}**")
            report.append(f"  Confidence: {chain.get('confidence', 0):.2f}")

        # Weak/Invalid Chains
        report.append(f"\n## WEAK OR INVALID CHAINS\n")
        weak_chains = [k for k, v in self.chain_validity.items()
                       if v['validity'] in ['invalid', 'partially_valid']]

        for chain_id in weak_chains[:20]:
            chain = self.evidence_chains[chain_id]
            validity = self.chain_validity[chain_id]['validity']
            report.append(f"\n- **{chain.get('source', '')}** → **{chain.get('target', '')}** [{validity.upper()}]")
            report.append(f"  Confidence: {chain.get('confidence', 0):.2f}")

        # Missing Links
        report.append(f"\n## MISSING LINKS IN EVIDENCE CHAINS\n")
        report.append(f"**Total Missing Links:** {len(self.missing_links)}\n")

        for link in self.missing_links[:20]:
            report.append(f"\n- {link['gap']}")
            report.append(f"  From: **{link['source']}** To: **{link['target']}**")

        # Circular References
        if self.circular_references:
            report.append(f"\n## CIRCULAR REFERENCES\n")
            report.append(f"**Found:** {len(self.circular_references)}\n")
            for ref in self.circular_references[:10]:
                report.append(f"- {ref}")

        # Evidence Strength Ranking
        report.append(f"\n## EVIDENCE STRENGTH RANKING\n")
        sorted_strength = sorted(self.evidence_strength.items(),
                                key=lambda x: x[1]['strength'], reverse=True)

        for chain_id, strength_info in sorted_strength[:30]:
            chain = self.evidence_chains[chain_id]
            report.append(f"\n- **{chain.get('source', '')}** → **{chain.get('target', '')}**")
            report.append(f"  Strength: {strength_info['strength']:.2f}")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Evidence chain report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    validator = EvidenceChainValidator(vault_path, data_path)
    validator.run_validation()


if __name__ == '__main__':
    main()
