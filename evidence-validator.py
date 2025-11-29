#!/usr/bin/env python3
"""
Evidence Validator and Cross-Reference Checker
Validates evidence quality, checks cross-references, and identifies gaps.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

class EvidenceValidator:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.evidence_quality = defaultdict(dict)
        self.validation_results = []
        self.cross_reference_issues = []
        self.completeness_scores = {}

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_validation(self):
        """Run complete evidence validation."""
        print("=" * 80)
        print("EVIDENCE VALIDATOR AND CROSS-REFERENCE CHECKER")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] VALIDATING EVIDENCE QUALITY...")
        self.validate_evidence_quality()

        print("\n[PHASE 2] CHECKING CROSS-REFERENCES...")
        self.check_cross_references()

        print("\n[PHASE 3] ASSESSING COMPLETENESS...")
        self.assess_completeness()

        print("\n[PHASE 4] IDENTIFYING EVIDENCE GAPS...")
        self.identify_evidence_gaps()

        print("\n[PHASE 5] GENERATING VALIDATION REPORT...")
        self.generate_validation_report()

        print("\n" + "=" * 80)
        print("EVIDENCE VALIDATION COMPLETE")
        print("=" * 80)

    def validate_evidence_quality(self):
        """Validate quality of evidence."""
        print(f"\nValidating evidence quality...")

        evidence_patterns = {
            'documented': r'\b(?:documented|documented in|found in|stated in|written in)\b',
            'sourced': r'\b(?:source|sourced|cited|reference|from|per|according to)\b',
            'verified': r'\b(?:verified|confirmed|proven|validated|established)\b',
            'dated': r'\b(?:\d{4}-\d{2}-\d{2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}(?:,|\s)\d{4})\b',
        }

        evidence_files = []
        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            if any(keyword in file_path.name for keyword in ['EVIDENCE', 'FRAMEWORK', 'FINDING']):
                evidence_files.append(file_path)

        print(f"Found {len(evidence_files)} evidence documents")

        for file_path in evidence_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                quality_score = 0
                max_score = 100

                # Check for evidence indicators
                for indicator, pattern in evidence_patterns.items():
                    matches = len(re.findall(pattern, content, re.IGNORECASE))
                    if matches > 0:
                        quality_score += 20
                    self.evidence_quality[str(file_path.relative_to(self.vault_path))][indicator] = matches

                # Check for numbered lists (evidence structure)
                list_items = len(re.findall(r'^[\d\-\*]+\.?\s+', content, re.MULTILINE))
                if list_items > 5:
                    quality_score += 10

                # Check document length
                if len(content) > 1000:
                    quality_score += 5

                file_rel_path = str(file_path.relative_to(self.vault_path))
                self.validation_results.append({
                    'file': file_rel_path,
                    'quality_score': min(quality_score, max_score),
                    'max_score': max_score,
                    'indicators': self.evidence_quality[file_rel_path]
                })

            except Exception as e:
                pass

        print(f"✓ Validated {len(self.validation_results)} evidence documents")

    def check_cross_references(self):
        """Check cross-references in documents."""
        print(f"\nChecking cross-references...")

        cross_refs = self.investigation_data.get('cross_references', {})
        total_refs = len(cross_refs)

        # Check for entities with too few cross-references
        low_ref_count = 0
        for entity, references in cross_refs.items():
            if len(references) < 2:
                low_ref_count += 1
                self.cross_reference_issues.append({
                    'entity': entity,
                    'issue': 'insufficient_cross_references',
                    'ref_count': len(references),
                    'recommendation': f'Add more cross-references for {entity}'
                })

        print(f"✓ Checked {total_refs} cross-reference entries")
        print(f"✓ Found {low_ref_count} entities with insufficient cross-references")

    def assess_completeness(self):
        """Assess investigation completeness."""
        print(f"\nAssessing investigation completeness...")

        # Completeness factors
        factors = {
            'entity_coverage': len(self.investigation_data.get('entities', {})) > 0,
            'relationships': len(self.investigation_data.get('relationships', [])) > 0,
            'cross_references': len(self.investigation_data.get('cross_references', {})) > 0,
            'evidence': len(self.investigation_data.get('keywords', {})) > 10,
            'multiple_sources': len(self.investigation_data.get('file_metadata', {})) > 10
        }

        # Calculate score
        completeness_score = sum(factors.values()) / len(factors) * 100

        # Category-specific completeness
        for category in ['organizations', 'people', 'technologies']:
            entities = self.investigation_data.get('entities', {}).get(category, [])
            refs = sum(len(self.investigation_data.get('cross_references', {}).get(e, []))
                      for e in entities)
            avg_refs = refs / len(entities) if entities else 0
            self.completeness_scores[category] = {
                'count': len(entities),
                'avg_references': avg_refs
            }

        print(f"✓ Investigation Completeness Score: {completeness_score:.1f}%")

    def identify_evidence_gaps(self):
        """Identify gaps in evidence."""
        print(f"\nIdentifying evidence gaps...")

        gaps = []

        # Gap 1: Entities without evidence files
        entities = self.investigation_data.get('entities', {})
        all_entity_names = set()
        for entity_type, ents in entities.items():
            all_entity_names.update(ents)

        # Check if each entity has a corresponding file
        entity_files = set()
        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue
            for entity in all_entity_names:
                if entity in file_path.name:
                    entity_files.add(entity)

        missing_files = all_entity_names - entity_files
        for entity in list(missing_files)[:20]:  # Top 20
            gaps.append({
                'type': 'missing_entity_file',
                'entity': entity,
                'recommendation': f'Create dedicated file for {entity}'
            })

        # Gap 2: Relationships without supporting evidence
        relationships = self.investigation_data.get('relationships', [])
        weak_rels = [r for r in relationships if r.get('confidence', 0) < 0.6]
        for rel in weak_rels[:10]:
            gaps.append({
                'type': 'weak_relationship',
                'source': rel.get('source', ''),
                'target': rel.get('target', ''),
                'confidence': rel.get('confidence', 0),
                'recommendation': 'Find additional evidence to strengthen connection'
            })

        print(f"✓ Identified {len(gaps)} evidence gaps")

    def generate_validation_report(self):
        """Generate validation report."""
        report_path = self.vault_path / 'EVIDENCE_VALIDATION_REPORT.md'

        report = []
        report.append("# EVIDENCE VALIDATION REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Summary
        report.append("## VALIDATION SUMMARY\n")
        total_quality = sum(v['quality_score'] for v in self.validation_results)
        avg_quality = total_quality / len(self.validation_results) if self.validation_results else 0

        report.append(f"- **Documents Validated:** {len(self.validation_results)}")
        report.append(f"- **Average Quality Score:** {avg_quality:.1f}/100")
        report.append(f"- **Cross-Reference Issues:** {len(self.cross_reference_issues)}")

        # Evidence Quality by Document
        report.append("\n## EVIDENCE QUALITY BY DOCUMENT\n")
        sorted_docs = sorted(self.validation_results, key=lambda x: x['quality_score'], reverse=True)

        for doc in sorted_docs:
            report.append(f"\n### {doc['file']}")
            report.append(f"- **Quality Score:** {doc['quality_score']}/{doc['max_score']}")
            report.append("- **Indicators:**")
            for indicator, count in doc['indicators'].items():
                report.append(f"  - {indicator}: {count}")

        # Completeness Assessment
        report.append("\n## INVESTIGATION COMPLETENESS\n")
        for category, scores in self.completeness_scores.items():
            report.append(f"\n### {category.upper()}\n")
            report.append(f"- **Count:** {scores['count']}")
            report.append(f"- **Avg Cross-References:** {scores['avg_references']:.1f}")

        # Cross-Reference Issues
        if self.cross_reference_issues:
            report.append("\n## CROSS-REFERENCE ISSUES\n")
            for issue in self.cross_reference_issues[:30]:
                report.append(f"\n- **Entity:** {issue['entity']}")
                report.append(f"  **Issue:** {issue['issue']}")
                report.append(f"  **References:** {issue['ref_count']}")
                report.append(f"  **Action:** {issue['recommendation']}")

        # Recommendations
        report.append("\n## RECOMMENDATIONS FOR IMPROVEMENT\n")
        report.append("""
1. **Increase Evidence Documentation:** Add more detailed evidence files
2. **Strengthen Weak Relationships:** Find additional proof for low-confidence connections
3. **Improve Cross-Referencing:** Link related entities more thoroughly
4. **Date All Evidence:** Ensure all findings include dates and timestamps
5. **Add Primary Sources:** Include references and citations
6. **Create Entity Files:** Establish dedicated profiles for key entities
7. **Document Timeline:** Create detailed chronological records
""")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Validation report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    validator = EvidenceValidator(vault_path, data_path)
    validator.run_validation()


if __name__ == '__main__':
    main()
