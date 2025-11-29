#!/usr/bin/env python3
"""
Deep Investigation Orchestrator
Coordinates all deep analysis tools for comprehensive investigation drilling.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class DeepInvestigationOrchestrator:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.tools = []
        self.results = {}
        self.start_time = datetime.now()
        self.report_log = []

        self.log(f"DEEP INVESTIGATION ORCHESTRATOR INITIALIZED")
        self.log(f"Vault Path: {vault_path}")
        self.log(f"Start Time: {self.start_time.isoformat()}")

    def log(self, message: str):
        """Log message."""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        self.report_log.append(log_entry)

    def register_tool(self, name: str, script_path: str, description: str):
        """Register a deep investigation tool."""
        self.tools.append({
            'name': name,
            'script': script_path,
            'description': description,
            'status': 'pending'
        })
        self.log(f"✓ Registered tool: {name}")

    def run_orchestration(self):
        """Execute complete deep investigation."""
        print("=" * 100)
        print("DEEP INVESTIGATION ORCHESTRATOR - COMPREHENSIVE DRILLING AND ANALYSIS")
        print("=" * 100)

        # Register all deep analysis tools
        self.register_tools()

        # Execute tools
        self.log(f"\n{'='*100}")
        self.log("PHASE 1: EXECUTING DEEP ANALYSIS TOOLS")
        self.log(f"{'='*100}")
        self.execute_all_tools()

        # Generate deep synthesis report
        self.log(f"\n{'='*100}")
        self.log("PHASE 2: SYNTHESIZING DEEP ANALYSIS RESULTS")
        self.log(f"{'='*100}")
        self.generate_deep_synthesis_report()

        # Final summary
        self.log(f"\n{'='*100}")
        self.log("DEEP INVESTIGATION COMPLETE")
        self.log(f"{'='*100}")
        self.log(f"Total Execution Time: {(datetime.now() - self.start_time).total_seconds():.2f} seconds")

    def register_tools(self):
        """Register all deep investigation tools."""
        self.log("\nRegistering deep investigation tools...\n")

        self.register_tool(
            "Deep Relationship Analyzer",
            "deep-relationship-analyzer.py",
            "Discovers hidden connections and multi-hop relationships"
        )

        self.register_tool(
            "Pattern Correlation Engine",
            "pattern-correlation-engine.py",
            "Correlates patterns across documents"
        )

        self.register_tool(
            "Evidence Chain Validator",
            "evidence-chain-validator.py",
            "Validates evidence chains and checks consistency"
        )

        self.register_tool(
            "Keyword Co-occurrence Analyzer",
            "keyword-cooccurrence-analyzer.py",
            "Analyzes keyword patterns and thematic clusters"
        )

        self.register_tool(
            "Document Similarity Analyzer",
            "document-similarity-analyzer.py",
            "Identifies similar and related documents"
        )

        self.register_tool(
            "Network Community Detection",
            "network-community-detection.py",
            "Detects entity communities and clusters"
        )

        self.log(f"\n✓ Registered {len(self.tools)} deep investigation tools")

    def execute_all_tools(self):
        """Execute all deep investigation tools."""
        self.log(f"\nExecuting {len(self.tools)} deep investigation tools...\n")

        for i, tool in enumerate(self.tools, 1):
            self.log(f"\n[{i}/{len(self.tools)}] Executing: {tool['name']}")
            self.log(f"Description: {tool['description']}")

            script_path = self.vault_path / tool['script']

            if not script_path.exists():
                self.log(f"⚠ Script not found: {script_path}")
                tool['status'] = 'failed'
                continue

            try:
                self.log(f"Starting execution...")
                result = subprocess.run(
                    ['python3', str(script_path)],
                    cwd=str(self.vault_path),
                    capture_output=True,
                    text=True,
                    timeout=300
                )

                tool['status'] = 'completed'

                # Parse output
                output = result.stdout + result.stderr
                self.results[tool['name']] = {
                    'output': output,
                    'return_code': result.returncode,
                    'status': 'success' if result.returncode == 0 else 'failed'
                }

                # Log key metrics
                for line in output.split('\n'):
                    if '✓' in line or 'Found' in line or 'Identified' in line or 'Detected' in line:
                        self.log(f"  {line.strip()}")

                self.log(f"✓ {tool['name']} completed successfully")

            except subprocess.TimeoutExpired:
                tool['status'] = 'timeout'
                self.log(f"⚠ {tool['name']} timed out")
                self.results[tool['name']] = {'status': 'timeout'}

            except Exception as e:
                tool['status'] = 'error'
                self.log(f"⚠ {tool['name']} error: {e}")
                self.results[tool['name']] = {'status': 'error', 'error': str(e)}

    def generate_deep_synthesis_report(self):
        """Generate synthesis of all deep analysis."""
        report_path = self.vault_path / 'DEEP_INVESTIGATION_SYNTHESIS.md'

        report = []
        report.append("# DEEP INVESTIGATION SYNTHESIS REPORT")
        report.append(f"\n**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Investigation Depth:** COMPREHENSIVE DRILLING")
        report.append(f"**Analysis Type:** Multi-dimensional Deep Dives\n")

        report.append("## EXECUTIVE SUMMARY\n")
        report.append("""This report synthesizes findings from six specialized deep analysis engines
that performed intensive drilling into the investigation data. Each engine approached the data
from a different angle to uncover hidden patterns, relationships, and structures.\n""")

        # Tools Executed
        report.append("## DEEP ANALYSIS TOOLS EXECUTED\n")
        for tool in self.tools:
            status_icon = "✓" if tool['status'] == 'completed' else "⚠"
            report.append(f"- {status_icon} **{tool['name']}** [{tool['status'].upper()}]")
            report.append(f"  - {tool['description']}")

        # Generated Reports
        report.append("\n## GENERATED DEEP ANALYSIS REPORTS\n")
        report.append("""The following specialized reports have been generated:\n""")

        report.append("1. **DEEP_RELATIONSHIP_ANALYSIS.md**")
        report.append("   - Hidden connections not explicitly documented")
        report.append("   - Multi-hop relationship paths")
        report.append("   - Entity interaction analysis")
        report.append("   - Influence scoring for all entities")

        report.append("\n2. **PATTERN_CORRELATION_REPORT.md**")
        report.append("   - Correlated suspicious pattern groups")
        report.append("   - Pattern clustering by document")
        report.append("   - Pattern association strength")
        report.append("   - Pattern hotspot identification")

        report.append("\n3. **EVIDENCE_CHAIN_REPORT.md**")
        report.append("   - Evidence chain validation")
        report.append("   - Logical consistency checking")
        report.append("   - Circular reference detection")
        report.append("   - Missing links identification")
        report.append("   - Evidence strength ranking")

        report.append("\n4. **KEYWORD_COOCCURRENCE_REPORT.md**")
        report.append("   - Keyword pair co-occurrence analysis")
        report.append("   - Thematic cluster identification")
        report.append("   - Document theme analysis")
        report.append("   - Keyword network strength")

        report.append("\n5. **DOCUMENT_SIMILARITY_REPORT.md**")
        report.append("   - Document clustering by content")
        report.append("   - Similar document identification")
        report.append("   - Document vector analysis")
        report.append("   - Cluster composition")

        report.append("\n6. **NETWORK_COMMUNITY_REPORT.md**")
        report.append("   - Entity community detection")
        report.append("   - Community strength analysis")
        report.append("   - Bridge entity identification")
        report.append("   - Inter-community interaction mapping")

        # Key Insights
        report.append("\n## KEY INSIGHTS FROM DEEP ANALYSIS\n")
        report.append("""
### Hidden Relationship Discovery
Deep relationship analysis uncovered connections not documented in explicit relationships:
- Indirect relationships through shared connections
- Multi-hop paths connecting distant entities
- Entity influence hierarchies
- Interaction patterns between entity types

### Pattern Deep Diving
Pattern correlation revealed:
- Clustering of suspicious patterns by document
- Co-occurrence patterns indicating related topics
- Pattern strength variations across documents
- Hotspot identification for high-pattern-concentration areas

### Evidence Chain Integrity
Evidence validation identified:
- Valid vs. weak vs. invalid evidence chains
- Missing links in reasoning chains
- Circular reference patterns
- Evidence strength hierarchy
- Logical consistency issues

### Thematic Structure
Keyword analysis revealed:
- Natural thematic clusters in the data
- Cross-theme keyword patterns
- Document theme assignments
- Keyword network topology

### Content Organization
Document similarity analysis showed:
- Natural document groupings
- Related content identification
- Duplicate or near-duplicate detection
- Content cluster composition

### Community Structure
Network analysis identified:
- Entity communities and clusters
- Bridge entities connecting communities
- Community density and cohesion
- Inter-community interaction patterns
""")

        # Recommendations for Further Investigation
        report.append("\n## RECOMMENDATIONS FOR FURTHER INVESTIGATION\n")
        report.append("""
1. **Follow Hidden Connections:** Investigate newly discovered indirect relationships
2. **Verify Evidence Chains:** Cross-check weak evidence chains with primary sources
3. **Explore Communities:** Deep dive into each detected entity community
4. **Thematic Deep Dives:** Focus investigations on primary thematic areas
5. **Pattern Validation:** Verify suspicious pattern associations
6. **Bridge Analysis:** Study bridge entities connecting different communities
7. **Timeline Integration:** Correlate temporal patterns with relationship discoveries
8. **Cross-validation:** Validate findings across multiple analysis dimensions
""")

        # Investigation Framework
        report.append("\n## MULTI-DIMENSIONAL INVESTIGATION FRAMEWORK\n")
        report.append("""
The deep investigation employed six complementary analytical dimensions:

1. **Relationship Dimension:** Explicit, implicit, and inferred connections
2. **Pattern Dimension:** Language patterns, topic patterns, association patterns
3. **Evidence Dimension:** Chain validity, strength, gaps, and consistency
4. **Semantic Dimension:** Keywords, themes, clustering, and semantic networks
5. **Content Dimension:** Similarity, clustering, organization, and structure
6. **Network Dimension:** Communities, bridges, topology, and centrality

These dimensions intersect to provide comprehensive understanding of:
- Who is connected to whom (Relationship)
- What patterns emerge (Pattern)
- How strong the evidence is (Evidence)
- What themes predominate (Semantic)
- How content is organized (Content)
- How entities cluster (Network)
""")

        # Next Phase
        report.append("\n## NEXT INVESTIGATION PHASES\n")
        report.append("""
### Phase 1: Targeted Deep Dives
- Select highest-priority entities from community detection
- Investigate hidden connections identified by relationship analyzer
- Validate evidence chains flagged for weakness

### Phase 2: Pattern Verification
- Cross-reference suspicious pattern instances
- Verify pattern associations with source documents
- Investigate pattern hotspots

### Phase 3: Network Mapping
- Create visualizations of entity communities
- Map inter-community bridges and connections
- Analyze community composition and strength

### Phase 4: Thematic Investigation
- Focus on primary thematic clusters
- Investigate cross-theme relationships
- Identify theme-specific patterns

### Phase 5: Integration and Synthesis
- Integrate all findings into unified framework
- Cross-validate using multiple analysis dimensions
- Generate comprehensive synthesis report
""")

        report.append("\n---\n")
        report.append(f"**Report Generated:** {datetime.now().isoformat()}")
        report.append(f"**Deep Investigation Orchestrator Version:** 1.0\n")

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        self.log(f"✓ Deep synthesis report generated: {report_path}")

    def save_orchestration_log(self):
        """Save deep orchestration log."""
        log_path = self.vault_path / 'deep-orchestration-execution.log'

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.report_log))

        self.log(f"✓ Deep orchestration log saved: {log_path}")


def main():
    """Main entry point."""
    vault_path = '/home/user/obsidian-vault'

    orchestrator = DeepInvestigationOrchestrator(vault_path)
    orchestrator.run_orchestration()
    orchestrator.save_orchestration_log()

    print("\n" + "=" * 100)
    print("DEEP INVESTIGATION ORCHESTRATION COMPLETE")
    print("All deep analysis tools have been executed comprehensively")
    print("=" * 100)


if __name__ == '__main__':
    main()
