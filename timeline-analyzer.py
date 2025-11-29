#!/usr/bin/env python3
"""
Timeline Analysis Tool
Builds comprehensive chronological timelines and identifies temporal relationships.
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Tuple

class TimelineAnalyzer:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.timeline_events = defaultdict(list)
        self.undated_events = []
        self.temporal_clusters = defaultdict(list)
        self.event_density = defaultdict(int)

        # Date patterns to search for
        self.date_patterns = [
            (r'(\d{4})-(\d{2})-(\d{2})', 'YYYY-MM-DD'),
            (r'([A-Za-z]+)\s+(\d{1,2}),?\s+(\d{4})', 'Month DD, YYYY'),
            (r'(\d{1,2})/(\d{1,2})/(\d{4})', 'MM/DD/YYYY'),
            (r'(\w+)\s+(\d{4})', 'Month YYYY'),
            (r'(\d{4})', 'YYYY'),
        ]

        # Month mapping
        self.months = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4,
            'may': 5, 'june': 6, 'july': 7, 'august': 8,
            'september': 9, 'october': 10, 'november': 11, 'december': 12
        }

    def run_analysis(self):
        """Run complete timeline analysis."""
        print("=" * 80)
        print("TIMELINE ANALYSIS ENGINE")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("=" * 80)

        print("\n[PHASE 1] EXTRACTING DATE INFORMATION...")
        self.extract_dates()

        print("\n[PHASE 2] BUILDING CHRONOLOGICAL TIMELINE...")
        self.build_timeline()

        print("\n[PHASE 3] IDENTIFYING TEMPORAL CLUSTERS...")
        self.identify_temporal_clusters()

        print("\n[PHASE 4] ANALYZING EVENT DENSITY...")
        self.analyze_event_density()

        print("\n[PHASE 5] GENERATING TIMELINE REPORT...")
        self.generate_timeline_report()

        print("\n" + "=" * 80)
        print("TIMELINE ANALYSIS COMPLETE")
        print("=" * 80)

    def extract_dates(self):
        """Extract all dates from vault files."""
        print(f"\nScanning all files for dates...")

        date_count = 0

        for file_path in self.vault_path.glob('**/*.md'):
            if '.git' in str(file_path):
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')

                for line_num, line in enumerate(lines):
                    # Try each pattern
                    for pattern, pattern_type in self.date_patterns:
                        matches = re.finditer(pattern, line, re.IGNORECASE)
                        for match in matches:
                            date_info = self.parse_date(match, pattern_type)
                            if date_info:
                                # Get context
                                context = line[max(0, match.start()-50):min(len(line), match.end()+50)]

                                event = {
                                    'date': date_info,
                                    'file': str(file_path.relative_to(self.vault_path)),
                                    'line': line_num,
                                    'context': context,
                                    'pattern_type': pattern_type
                                }

                                # Store by year
                                year = date_info.get('year')
                                if year:
                                    self.timeline_events[year].append(event)
                                    self.event_density[year] += 1
                                    date_count += 1
                                else:
                                    self.undated_events.append(event)

            except Exception as e:
                pass

        print(f"✓ Extracted {date_count} dated events from files")
        print(f"✓ Found {len(self.undated_events)} undated event references")

    def parse_date(self, match, pattern_type: str) -> Dict:
        """Parse date from regex match."""
        try:
            if pattern_type == 'YYYY-MM-DD':
                return {
                    'year': int(match.group(1)),
                    'month': int(match.group(2)),
                    'day': int(match.group(3)),
                    'full': match.group(0)
                }
            elif pattern_type == 'Month DD, YYYY':
                month_str = match.group(1).lower()
                month = self.months.get(month_str, 0)
                if month:
                    return {
                        'year': int(match.group(3)),
                        'month': month,
                        'day': int(match.group(2)),
                        'full': match.group(0)
                    }
            elif pattern_type == 'MM/DD/YYYY':
                return {
                    'year': int(match.group(3)),
                    'month': int(match.group(1)),
                    'day': int(match.group(2)),
                    'full': match.group(0)
                }
            elif pattern_type == 'Month YYYY':
                month_str = match.group(1).lower()
                month = self.months.get(month_str, 0)
                if month:
                    return {
                        'year': int(match.group(2)),
                        'month': month,
                        'full': match.group(0)
                    }
            elif pattern_type == 'YYYY':
                return {
                    'year': int(match.group(1)),
                    'full': match.group(0)
                }
        except (ValueError, AttributeError):
            pass

        return None

    def build_timeline(self):
        """Build chronological timeline."""
        print(f"\nBuilding chronological timeline...")

        total_events = sum(len(events) for events in self.timeline_events.values())
        print(f"✓ Timeline spans {len(self.timeline_events)} years with {total_events} events")

    def identify_temporal_clusters(self):
        """Identify clusters of high-activity periods."""
        print(f"\nIdentifying temporal clusters...")

        # Find years with high activity
        sorted_years = sorted(self.event_density.items(), key=lambda x: x[1], reverse=True)

        for year, count in sorted_years[:20]:
            if count >= 5:  # Threshold for cluster
                self.temporal_clusters[year] = {
                    'events': count,
                    'files': len(set(e['file'] for e in self.timeline_events.get(year, [])))
                }

        print(f"✓ Identified {len(self.temporal_clusters)} temporal clusters")

    def analyze_event_density(self):
        """Analyze event density over time."""
        print(f"\nAnalyzing event density...")

        all_years = sorted(self.event_density.keys())
        if all_years:
            min_year = all_years[0]
            max_year = all_years[-1]
            total_span = max_year - min_year

            avg_events = sum(self.event_density.values()) / len(self.event_density)
            max_events = max(self.event_density.values())
            min_events = min(self.event_density.values())

            print(f"  Time Span: {min_year} - {max_year} ({total_span} years)")
            print(f"  Avg Events/Year: {avg_events:.1f}")
            print(f"  Peak Activity: {max_events} events")
            print(f"  Low Activity: {min_events} event(s)")

    def generate_timeline_report(self):
        """Generate comprehensive timeline report."""
        report_path = self.vault_path / 'TIMELINE_ANALYSIS_REPORT.md'

        report = []
        report.append("# TIMELINE ANALYSIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}\n")

        # Overall Statistics
        total_events = sum(len(events) for events in self.timeline_events.values())
        report.append("## TIMELINE STATISTICS\n")
        report.append(f"- **Total Dated Events:** {total_events}")
        report.append(f"- **Undated References:** {len(self.undated_events)}")
        report.append(f"- **Years Covered:** {len(self.timeline_events)}")
        if self.timeline_events:
            report.append(f"- **Time Span:** {min(self.timeline_events.keys())} - {max(self.timeline_events.keys())}")

        # Chronological Timeline
        report.append("\n## CHRONOLOGICAL TIMELINE\n")

        sorted_years = sorted(self.timeline_events.items())
        for year, events in sorted_years:
            report.append(f"\n### {year} ({len(events)} events)\n")

            # Sort events by month within year
            sorted_events = sorted(events, key=lambda x: (x['date'].get('month', 0), x['date'].get('day', 0)))

            for event in sorted_events[:30]:  # Top 30 per year
                date_str = event['date'].get('full', str(year))
                context = event['context'].strip()[:100]
                report.append(f"- **{date_str}** - {context}")
                report.append(f"  (File: `{event['file']}`, Line: {event['line']})")

            if len(sorted_events) > 30:
                report.append(f"- ... and {len(sorted_events) - 30} more events")

        # High Activity Years
        report.append("\n## HIGH ACTIVITY PERIODS\n")
        if self.temporal_clusters:
            report.append("\nYears with significant documentation activity:\n")
            for year in sorted(self.temporal_clusters.keys(), reverse=True):
                cluster = self.temporal_clusters[year]
                report.append(f"- **{year}**: {cluster['events']} events across {cluster['files']} files")

        # Temporal Gaps
        report.append("\n## TEMPORAL GAPS\n")
        if self.timeline_events:
            all_years = set(self.timeline_events.keys())
            min_year = min(all_years)
            max_year = max(all_years)

            missing_years = []
            for year in range(min_year, max_year + 1):
                if year not in all_years:
                    missing_years.append(year)

            if missing_years:
                report.append(f"\nYears with no documented events:\n")
                for year in missing_years[-20:]:  # Last 20
                    report.append(f"- {year}")

        # Undated Events
        if self.undated_events:
            report.append(f"\n## UNDATED REFERENCES ({len(self.undated_events)})\n")
            report.append("Events mentioned but not clearly dated:\n")
            for event in self.undated_events[:20]:
                report.append(f"- {event['context'][:80]}")
                report.append(f"  (File: `{event['file']}`)")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✓ Timeline report generated: {report_path}")


def main():
    vault_path = '/home/user/obsidian-vault'
    analyzer = TimelineAnalyzer(vault_path)
    analyzer.run_analysis()


if __name__ == '__main__':
    main()
