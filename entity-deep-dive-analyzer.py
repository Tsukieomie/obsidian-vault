#!/usr/bin/env python3
"""
Entity Deep-Dive Analyzer
Performs intensive analysis on specific entity types and categories.
"""

import json
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Set

class EntityDeepDiveAnalyzer:
    def __init__(self, vault_path: str, investigation_data_path: str):
        self.vault_path = Path(vault_path)
        self.investigation_data = self.load_data(investigation_data_path)
        self.entity_profiles = defaultdict(dict)
        self.entity_connections = defaultdict(list)
        self.entity_mentions = defaultdict(list)

    def load_data(self, data_path: str) -> Dict:
        """Load investigation data."""
        try:
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load data: {e}")
            return {}

    def run_analysis(self):
        """Run entity deep-dive analysis."""
        print("=" * 80)
        print("ENTITY DEEP-DIVE ANALYZER")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] PROFILING ORGANIZATIONS...")
        self.profile_organizations()

        print("\n[PHASE 2] PROFILING PEOPLE...")
        self.profile_people()

        print("\n[PHASE 3] ANALYZING TECHNOLOGIES...")
        self.analyze_technologies()

        print("\n[PHASE 4] MAPPING ENTITY CONNECTIONS...")
        self.map_entity_connections()

        print("\n[PHASE 5] GENERATING ENTITY PROFILES...")
        self.generate_entity_profiles_report()

        print("\n" + "=" * 80)
        print("ENTITY DEEP-DIVE ANALYSIS COMPLETE")
        print("=" * 80)

    def profile_organizations(self):
        """Profile all organizations."""
        print(f"\nAnalyzing organizations...")

        organizations = self.investigation_data.get('entities', {}).get('organizations', [])
        print(f"Found {len(organizations)} organizations")

        # Create detailed profiles for each
        for org in organizations[:50]:  # Detailed profiles for top 50
            self.entity_profiles[org] = {
                'type': 'organization',
                'mentions': [],
                'connections': [],
                'files': set()
            }

            # Find mentions in vault
            for file_path in self.vault_path.glob('**/*.md'):
                if '.git' in str(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if org.lower() in content.lower():
                            count = content.lower().count(org.lower())
                            self.entity_profiles[org]['mentions'].append({
                                'file': str(file_path.relative_to(self.vault_path)),
                                'count': count
                            })
                            self.entity_profiles[org]['files'].add(str(file_path.relative_to(self.vault_path)))
                except Exception as e:
                    pass

        print(f"✓ Profiled {len([e for e in self.entity_profiles if self.entity_profiles[e].get('type') == 'organization'])} organizations")

    def profile_people(self):
        """Profile all people."""
        print(f"\nAnalyzing people...")

        people = self.investigation_data.get('entities', {}).get('people', [])
        print(f"Found {len(people)} individuals")

        # Create detailed profiles for each
        for person in people[:50]:  # Detailed profiles for top 50
            self.entity_profiles[person] = {
                'type': 'person',
                'mentions': [],
                'connections': [],
                'files': set()
            }

            # Find mentions
            for file_path in self.vault_path.glob('**/*.md'):
                if '.git' in str(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if person.lower() in content.lower():
                            count = content.lower().count(person.lower())
                            self.entity_profiles[person]['mentions'].append({
                                'file': str(file_path.relative_to(self.vault_path)),
                                'count': count
                            })
                            self.entity_profiles[person]['files'].add(str(file_path.relative_to(self.vault_path)))
                except Exception as e:
                    pass

        print(f"✓ Profiled {len([e for e in self.entity_profiles if self.entity_profiles[e].get('type') == 'person'])} people")

    def analyze_technologies(self):
        """Analyze technologies and projects."""
        print(f"\nAnalyzing technologies...")

        technologies = self.investigation_data.get('entities', {}).get('technologies', [])
        print(f"Found {len(technologies)} technologies")

        # Profile each technology
        for tech in technologies:
            self.entity_profiles[tech] = {
                'type': 'technology',
                'mentions': [],
                'connections': [],
                'files': set(),
                'related_entities': set()
            }

            # Find mentions and related entities
            for file_path in self.vault_path.glob('**/*.md'):
                if '.git' in str(file_path):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if tech.lower() in content.lower():
                            count = content.lower().count(tech.lower())
                            self.entity_profiles[tech]['mentions'].append({
                                'file': str(file_path.relative_to(self.vault_path)),
                                'count': count
                            })
                            self.entity_profiles[tech]['files'].add(str(file_path.relative_to(self.vault_path)))

                            # Find related entities in same file
                            all_entities = (
                                self.investigation_data.get('entities', {}).get('organizations', []) +
                                self.investigation_data.get('entities', {}).get('people', [])
                            )
                            for entity in all_entities:
                                if entity.lower() in content.lower():
                                    self.entity_profiles[tech]['related_entities'].add(entity)

                except Exception as e:
                    pass

        print(f"✓ Analyzed {len(technologies)} technologies")

    def map_entity_connections(self):
        """Map connections between entities."""
        print(f"\nMapping entity connections...")

        relationships = self.investigation_data.get('relationships', [])

        for rel in relationships:
            source = rel.get('source', '')
            target = rel.get('target', '')

            if source in self.entity_profiles:
                self.entity_profiles[source]['connections'].append({
                    'target': target,
                    'confidence': rel.get('confidence', 0.5)
                })

            if target in self.entity_profiles:
                self.entity_profiles[target]['connections'].append({
                    'target': source,
                    'confidence': rel.get('confidence', 0.5)
                })

        print(f"✓ Mapped connections for {len([e for e in self.entity_profiles if self.entity_profiles[e].get('connections')])} entities")

    def generate_entity_profiles_report(self):
        """Generate entity profiles report."""
        report_path = self.vault_path / 'ENTITY_PROFILES_REPORT.md'

        report = []
        report.append("# ENTITY PROFILES REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Organize by type
        organizations = {e: p for e, p in self.entity_profiles.items() if p.get('type') == 'organization'}
        people = {e: p for e, p in self.entity_profiles.items() if p.get('type') == 'person'}
        technologies = {e: p for e, p in self.entity_profiles.items() if p.get('type') == 'technology'}

        # Organizations
        report.append("## ORGANIZATIONS\n")
        for org, profile in sorted(organizations.items()):
            report.append(f"\n### {org}\n")
            report.append(f"- **Type:** Organization")
            report.append(f"- **Mentions:** {len(profile.get('mentions', []))} files")
            report.append(f"- **Files Present:** {len(profile.get('files', []))}")
            report.append(f"- **Connections:** {len(profile.get('connections', []))}")

            if profile.get('mentions'):
                total_mentions = sum(m['count'] for m in profile['mentions'])
                report.append(f"- **Total Mentions:** {total_mentions}")

        # People
        report.append("\n## PEOPLE\n")
        for person, profile in sorted(people.items()):
            report.append(f"\n### {person}\n")
            report.append(f"- **Type:** Individual")
            report.append(f"- **Mentions:** {len(profile.get('mentions', []))} files")
            report.append(f"- **Files Present:** {len(profile.get('files', []))}")
            report.append(f"- **Connections:** {len(profile.get('connections', []))}")

            if profile.get('mentions'):
                total_mentions = sum(m['count'] for m in profile['mentions'])
                report.append(f"- **Total Mentions:** {total_mentions}")

        # Technologies
        report.append("\n## TECHNOLOGIES\n")
        for tech, profile in sorted(technologies.items()):
            report.append(f"\n### {tech}\n")
            report.append(f"- **Type:** Technology/Project")
            report.append(f"- **Files Present:** {len(profile.get('files', []))}")
            report.append(f"- **Related Entities:** {len(profile.get('related_entities', []))}")

            if profile.get('related_entities'):
                report.append("- **Related Entities:**")
                for entity in list(profile['related_entities'])[:10]:
                    report.append(f"  - {entity}")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Entity profiles report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    data_path = '/home/user/obsidian-vault/investigation_data.json'

    analyzer = EntityDeepDiveAnalyzer(vault_path, data_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
