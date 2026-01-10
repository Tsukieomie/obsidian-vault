#!/usr/bin/env python3
"""
Investigation Orchestrator
Complete automated investigation workflow with reporting and analysis
"""

import json
from typing import Dict, List
import os
from datetime import datetime
from automated_investigation import AutomatedInvestigation
from vault_api import ObsidianVault
from vault_insights import VaultInsights


class InvestigationOrchestrator:
    """Orchestrates complete investigation workflow"""

    def __init__(self, output_dir: str = 'investigation_output'):
        self.output_dir = output_dir
        self.vault = ObsidianVault()
        self.vault.load()
        self.investigation = AutomatedInvestigation()
        self.timestamp = datetime.now()
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def run_complete_investigation(self) -> Dict:
        """Run complete investigation workflow"""
        print("="*80)
        print("INVESTIGATION ORCHESTRATOR - COMPLETE WORKFLOW")
        print("="*80)
        print(f"Started: {self.timestamp.isoformat()}")
        print("")

        # Phase 1: Analysis
        print("PHASE 1: Running Automated Analysis...")
        analysis_results = self.investigation.run_full_investigation()
        print("✓ Automated analysis complete")
        print("")

        # Phase 2: Report Generation
        print("PHASE 2: Generating Comprehensive Reports...")
        reports = self._generate_all_reports(analysis_results)
        print("✓ Reports generated")
        print("")

        # Phase 3: Data Export
        print("PHASE 3: Exporting Investigation Data...")
        exports = self._export_investigation_data()
        print("✓ Data exported")
        print("")

        # Phase 4: Executive Summary
        print("PHASE 4: Creating Executive Summary...")
        summary = self._create_executive_summary(analysis_results, reports)
        print("✓ Executive summary created")
        print("")

        # Phase 5: File Organization
        print("PHASE 5: Organizing Investigation Files...")
        self._organize_output_files(reports, exports, summary)
        print("✓ Files organized")
        print("")

        print("="*80)
        print("INVESTIGATION COMPLETE")
        print("="*80)

        return {
            'timestamp': self.timestamp.isoformat(),
            'analysis': analysis_results,
            'reports': reports,
            'exports': exports,
            'summary': summary,
            'output_directory': self.output_dir
        }

    def _generate_all_reports(self, analysis_results) -> Dict:
        """Generate all investigation reports"""
        reports = {}

        # Main automated report
        reports['automated_analysis'] = analysis_results['report']

        # Entity report
        reports['entity_analysis'] = self._generate_entity_report()

        # Timeline report
        reports['timeline_analysis'] = self._generate_timeline_report()

        # Connection report
        reports['connection_analysis'] = self._generate_connection_report(analysis_results)

        # Evidence report
        reports['evidence_summary'] = self._generate_evidence_report()

        # Recommendation report
        reports['investigation_recommendations'] = self._generate_recommendation_report(analysis_results)

        return reports

    def _generate_entity_report(self) -> str:
        """Generate comprehensive entity analysis report"""
        lines = []
        lines.append("="*80)
        lines.append("ENTITY ANALYSIS REPORT")
        lines.append("="*80)
        lines.append("")

        entities = self.vault.list_entities()
        lines.append(f"Total Entities: {len(entities)}\n")

        # Group by type
        entity_types = {}
        for entity_name in entities:
            entity = self.vault.get_entity(entity_name)
            if entity:
                entity_type = entity.entity_type
                if entity_type not in entity_types:
                    entity_types[entity_type] = []
                entity_types[entity_type].append(entity_name)

        for entity_type, entity_list in sorted(entity_types.items()):
            lines.append(f"\n{entity_type.upper()} ({len(entity_list)} entities)")
            lines.append("-"*80)
            for entity_name in sorted(entity_list):
                entity = self.vault.get_entity(entity_name)
                if entity:
                    mentions = len(self.vault.loader.tag_index.get(entity_name, set()))
                    lines.append(f"  • {entity_name} ({mentions} mentions)")

        lines.append("\n" + "="*80)
        return "\n".join(lines)

    def _generate_timeline_report(self) -> str:
        """Generate timeline analysis report"""
        lines = []
        lines.append("="*80)
        lines.append("TIMELINE ANALYSIS REPORT")
        lines.append("="*80)
        lines.append("")

        # Find timeline documents
        timeline_files = [f for f in self.vault.list_files() if 'timeline' in f.lower()]

        if timeline_files:
            lines.append(f"Timeline Documents Found: {len(timeline_files)}\n")
            for file_path in timeline_files:
                file = self.vault.get_file(file_path)
                if file:
                    lines.append(f"  • {file.title}")
                    lines.append(f"    Path: {file_path}")
                    lines.append(f"    Size: {len(file.content)} characters")
                    lines.append("")
        else:
            lines.append("No timeline documents found. Timeline reconstruction needed.\n")

        # Analysis requirements
        lines.append("Timeline Analysis Requirements:")
        lines.append("-"*80)
        lines.append("  [ ] Identify investigation start date")
        lines.append("  [ ] Map major events chronologically")
        lines.append("  [ ] Identify pattern cycles and repetitions")
        lines.append("  [ ] Cross-reference with external events")
        lines.append("  [ ] Determine causality and dependencies")

        lines.append("\n" + "="*80)
        return "\n".join(lines)

    def _generate_connection_report(self, analysis_results) -> str:
        """Generate connection analysis report"""
        lines = []
        lines.append("="*80)
        lines.append("CONNECTION ANALYSIS REPORT")
        lines.append("="*80)
        lines.append("")

        stats = self.vault.get_statistics()
        lines.append(f"Total Relationships Documented: {stats['total_relationships']}\n")

        # Hidden connections
        hidden = analysis_results['hidden_connections']
        major_hubs = {}
        for entity, connections in hidden.items():
            if connections:
                major_hubs[entity] = len(connections)

        if major_hubs:
            lines.append("Major Connection Hubs (Indirect Connections):")
            lines.append("-"*80)
            for entity, count in sorted(major_hubs.items(), key=lambda x: x[1], reverse=True)[:10]:
                lines.append(f"  {entity}: {count} indirect connections")
            lines.append("")

        # Network analysis
        lines.append("Network Metrics:")
        lines.append("-"*80)
        entities = self.vault.list_entities()
        lines.append(f"  Total Entities: {len(entities)}")
        lines.append(f"  Known Relationships: {stats['total_relationships']}")
        lines.append(f"  Potential Density: {stats['total_relationships'] / (len(entities) * (len(entities)-1) / 2):.2%}")
        lines.append("")

        lines.append("="*80)
        return "\n".join(lines)

    def _generate_evidence_report(self) -> str:
        """Generate evidence summary report"""
        lines = []
        lines.append("="*80)
        lines.append("EVIDENCE SUMMARY REPORT")
        lines.append("="*80)
        lines.append("")

        # Find evidence-related documents
        evidence_files = [f for f in self.vault.list_files()
                         if 'evidence' in f.lower() or 'document' in f.lower()]

        lines.append(f"Evidence Documents: {len(evidence_files)}\n")

        if 'Evidence Repository' in [f.split('/')[-1].replace('.md', '') for f in self.vault.list_files()]:
            lines.append("Evidence Repository Location: Evidence Repository.md")
            lines.append("-"*80)
            lines.append("  See Evidence Repository.md for complete evidence index")
            lines.append("  All external evidence links stored in Google Drive")
            lines.append("")

        lines.append("Evidence Categories:")
        lines.append("-"*80)
        lines.append("  • Executive Reports and Briefings")
        lines.append("  • Evidence Compilations and Masters")
        lines.append("  • Intelligence Briefs")
        lines.append("  • Archived Collections")
        lines.append("")

        lines.append("Key Evidence Documents:")
        lines.append("-"*80)
        lines.append("  • INTELLIGENCE_BRIEF_Master_Report_KenRodrigues.pdf")
        lines.append("  • HLPS_Evidence_Summary_Kenny.pdf")
        lines.append("  • Smart_Harassment_Evidence_FUSED_MASTER_Binder.pdf")
        lines.append("  • MASTER_EVIDENCE_BINDER_CONFIDENTIAL.pdf")

        lines.append("\n" + "="*80)
        return "\n".join(lines)

    def _generate_recommendation_report(self, analysis_results) -> str:
        """Generate investigation recommendations report"""
        lines = []
        lines.append("="*80)
        lines.append("INVESTIGATION RECOMMENDATIONS REPORT")
        lines.append("="*80)
        lines.append("")

        recommendations = analysis_results['recommendations']

        lines.append(f"Total Recommendations: {len(recommendations)}\n")
        lines.append("CRITICAL PRIORITY (Immediate Action):")
        lines.append("-"*80)
        critical = [r for r in recommendations if r['priority'] == 'CRITICAL']
        for i, rec in enumerate(critical, 1):
            lines.append(f"{i}. {rec['action']}")
            lines.append(f"   Outcome: {rec['outcome']}")
        lines.append("")

        lines.append("HIGH PRIORITY (This Week):")
        lines.append("-"*80)
        high = [r for r in recommendations if r['priority'] == 'HIGH']
        for i, rec in enumerate(high, 1):
            lines.append(f"{i}. {rec['action']}")
            lines.append(f"   Outcome: {rec['outcome']}")
        lines.append("")

        lines.append("MEDIUM PRIORITY (This Month):")
        lines.append("-"*80)
        medium = [r for r in recommendations if r['priority'] == 'MEDIUM']
        for i, rec in enumerate(medium, 1):
            lines.append(f"{i}. {rec['action']}")
            lines.append(f"   Outcome: {rec['outcome']}")

        lines.append("\n" + "="*80)
        return "\n".join(lines)

    def _export_investigation_data(self) -> Dict:
        """Export investigation data in various formats"""
        exports = {}

        # Export vault data
        vault_export = self.vault.export_as_json(include_content=False)
        exports['vault_summary'] = vault_export

        # Export entity list
        exports['entities'] = self.vault.list_entities()

        # Export tags
        exports['tags'] = self.vault.list_tags()

        # Export statistics
        exports['statistics'] = self.vault.get_statistics()

        return exports

    def _create_executive_summary(self, analysis_results, reports) -> Dict:
        """Create executive summary of investigation"""
        summary = {
            'investigation_date': self.timestamp.isoformat(),
            'vault_status': {
                'total_files': len(self.vault.list_files()),
                'total_entities': len(self.vault.list_entities()),
                'total_relationships': self.vault.get_statistics()['total_relationships'],
            },
            'key_findings': {
                'investigation_hotspots': analysis_results['hotspots'],
                'emerging_leads': analysis_results['emerging_leads'][:5],
                'scope_expansion': analysis_results['scope']['scope_expansion_potential'],
            },
            'critical_recommendations': [
                r for r in analysis_results['recommendations']
                if r['priority'] == 'CRITICAL'
            ],
            'next_steps': self._generate_next_steps(analysis_results),
        }
        return summary

    def _generate_next_steps(self, analysis_results) -> List[str]:
        """Generate immediate next steps"""
        steps = [
            "1. Review automated investigation report",
            "2. Access and analyze evidence documents (Google Drive)",
            "3. Conduct deep analysis of entity hubs (Brandon Han, Asymptote, SalmonCloud)",
            "4. Research isolated entities and discover missing connections",
            "5. Reconstruct complete investigation timeline",
            "6. Systematically cross-reference all evidence",
            "7. Map institutional networks and affiliations",
            "8. Analyze Project Stargate parallels and historical context",
            "9. Identify personnel with government/research backgrounds",
            "10. Document findings and update investigation profile",
        ]
        return steps

    def _organize_output_files(self, reports, exports, summary):
        """Save all reports and data to organized files"""
        timestamp_str = self.timestamp.strftime('%Y%m%d_%H%M%S')

        # Save main report
        report_file = os.path.join(self.output_dir, f'investigation_report_{timestamp_str}.txt')
        with open(report_file, 'w') as f:
            f.write(reports['automated_analysis'])
        print(f"  Saved: {report_file}")

        # Save all reports
        for report_name, report_content in reports.items():
            if isinstance(report_content, str):
                file_path = os.path.join(self.output_dir, f'{report_name}_{timestamp_str}.txt')
                with open(file_path, 'w') as f:
                    f.write(report_content)

        # Save structured data
        data_file = os.path.join(self.output_dir, f'investigation_data_{timestamp_str}.json')
        with open(data_file, 'w') as f:
            json.dump({
                'exports': exports,
                'summary': summary,
            }, f, indent=2, default=str)

        # Save summary
        summary_file = os.path.join(self.output_dir, f'executive_summary_{timestamp_str}.json')
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        print(f"  Output directory: {self.output_dir}/")
        print(f"  Reports saved with timestamp: {timestamp_str}")


if __name__ == '__main__':
    orchestrator = InvestigationOrchestrator()
    results = orchestrator.run_complete_investigation()

    print("\nInvestigation Results Summary:")
    print(f"  Output Directory: {results['output_directory']}")
    print(f"  Files Generated: Multiple reports and exports")
    print(f"  Investigation Date: {results['timestamp']}")
    print("\nReview the output directory for complete investigation results.")
