#!/usr/bin/env python3
"""
Investigation Query Tool
Semantic search across investigation evidence via Supermemory.

Usage:
    python3 .investigation_query.py

Environment:
    API_KEY - Supermemory API key (from ~/.env)
"""

import os
import sys
import re
import subprocess
from pathlib import Path
from typing import Optional

# Check for requests library
try:
    import requests
except ImportError:
    print("Error: 'requests' library not installed.")
    print("Install with: pip install requests")
    sys.exit(1)

# Configuration
BASE_URL = "https://api.supermemory.ai/v1"
VAULT_DIR = Path(__file__).parent.resolve()


class InvestigationQuery:
    """Query interface for investigation evidence."""

    def __init__(self):
        self.api_key = self._get_api_key()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _get_api_key(self) -> str:
        """Get API key from environment variable."""
        api_key = os.getenv("API_KEY")
        if not api_key:
            # Try loading from ~/.env
            env_file = Path.home() / ".env"
            if env_file.exists():
                with open(env_file) as f:
                    for line in f:
                        if line.startswith("API_KEY="):
                            api_key = line.strip().split("=", 1)[1]
                            api_key = api_key.strip("'\"")
                            break
        if not api_key:
            print("Warning: API_KEY not found. Semantic search unavailable.")
            print("Set with: export API_KEY=your-api-key")
            return ""
        return api_key

    def semantic_search(self, query: str, limit: int = 10) -> list:
        """Search documents semantically via Supermemory."""
        if not self.api_key:
            return []

        payload = {
            "query": query,
            "limit": limit,
        }

        try:
            response = requests.post(
                f"{BASE_URL}/search",
                headers=self.headers,
                json=payload,
                timeout=30,
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
            else:
                print(f"Search error: {response.status_code}")
                return []
        except requests.exceptions.RequestException as e:
            print(f"Search error: {e}")
            return []

    def local_search(self, query: str) -> list:
        """Search local vault using grep."""
        results = []
        query_lower = query.lower()

        for md_file in VAULT_DIR.rglob("*.md"):
            # Skip hidden files
            try:
                relative_parts = md_file.relative_to(VAULT_DIR).parts
                if any(part.startswith(".") for part in relative_parts):
                    continue
            except ValueError:
                continue

            try:
                content = md_file.read_text(encoding="utf-8")
                if query_lower in content.lower():
                    # Find matching lines
                    lines = content.split("\n")
                    matches = []
                    for i, line in enumerate(lines, 1):
                        if query_lower in line.lower():
                            matches.append({"line": i, "text": line.strip()[:100]})

                    results.append(
                        {
                            "path": str(md_file.relative_to(VAULT_DIR)),
                            "matches": matches[:3],  # Limit matches per file
                        }
                    )
            except Exception:
                continue

        return results

    def query(self, query_str: str, limit: int = 10):
        """Execute a query and display results."""
        print(f"\n🔍 Searching: {query_str}")
        print("=" * 60)

        # Semantic search
        print("\n📊 SEMANTIC RESULTS (Supermemory)")
        print("-" * 40)
        semantic_results = self.semantic_search(query_str, limit)
        if semantic_results:
            for i, result in enumerate(semantic_results, 1):
                title = result.get("title", "Unknown")
                score = result.get("score", 0)
                snippet = result.get("content", "")[:150]
                print(f"\n  {i}. {title}")
                print(f"     Score: {score:.2f}")
                print(f"     {snippet}...")
        else:
            print("  No semantic results found.")
            if not self.api_key:
                print("  (API key not configured)")

        # Local search
        print("\n📁 LOCAL RESULTS (grep)")
        print("-" * 40)
        local_results = self.local_search(query_str)
        if local_results:
            for i, result in enumerate(local_results[:5], 1):
                print(f"\n  {i}. {result['path']}")
                for match in result["matches"]:
                    print(f"     Line {match['line']}: {match['text']}")
        else:
            print("  No local results found.")

        print("\n" + "=" * 60)

    def cross_reference(self, entity1: str, entity2: str):
        """Find cross-references between two entities."""
        print(f"\n🔗 CROSS-REFERENCE ANALYSIS")
        print(f"   {entity1} ⟷ {entity2}")
        print("=" * 60)

        # Search for documents mentioning both
        query = f"{entity1} {entity2}"

        # Semantic search
        print("\n📊 SEMANTIC CONNECTIONS")
        print("-" * 40)
        semantic_results = self.semantic_search(query, 10)
        if semantic_results:
            for i, result in enumerate(semantic_results, 1):
                title = result.get("title", "Unknown")
                score = result.get("score", 0)
                print(f"  {i}. {title} (Score: {score:.2f})")
        else:
            print("  No semantic connections found.")

        # Local search for both entities
        print("\n📁 LOCAL CONNECTIONS")
        print("-" * 40)
        files_with_both = []
        for md_file in VAULT_DIR.rglob("*.md"):
            try:
                relative_parts = md_file.relative_to(VAULT_DIR).parts
                if any(part.startswith(".") for part in relative_parts):
                    continue
            except ValueError:
                continue
            try:
                content = md_file.read_text(encoding="utf-8").lower()
                if entity1.lower() in content and entity2.lower() in content:
                    files_with_both.append(md_file.relative_to(VAULT_DIR))
            except Exception:
                continue

        if files_with_both:
            for f in files_with_both:
                print(f"  - {f}")
        else:
            print("  No local files mention both entities.")

        print("\n" + "=" * 60)

    def timeline_query(self, year: int):
        """Query events from a specific year."""
        print(f"\n📅 TIMELINE QUERY: {year}")
        print("=" * 60)

        # Semantic search
        query = f"events in {year} timeline"
        print("\n📊 SEMANTIC RESULTS")
        print("-" * 40)
        semantic_results = self.semantic_search(query, 10)
        if semantic_results:
            for i, result in enumerate(semantic_results, 1):
                title = result.get("title", "Unknown")
                score = result.get("score", 0)
                print(f"  {i}. {title} (Score: {score:.2f})")
        else:
            print("  No semantic results found.")

        # Local search for year
        print(f"\n📁 LOCAL MENTIONS OF {year}")
        print("-" * 40)
        local_results = self.local_search(str(year))
        if local_results:
            for result in local_results[:5]:
                print(f"  - {result['path']}")
        else:
            print(f"  No local files mention {year}.")

        print("\n" + "=" * 60)

    def evidence_query(self, evidence_type: str):
        """Query for specific type of evidence."""
        print(f"\n📋 EVIDENCE QUERY: {evidence_type.upper()}")
        print("=" * 60)

        # Semantic search
        query = f"{evidence_type} evidence investigation"
        print("\n📊 SEMANTIC RESULTS")
        print("-" * 40)
        semantic_results = self.semantic_search(query, 10)
        if semantic_results:
            for i, result in enumerate(semantic_results, 1):
                title = result.get("title", "Unknown")
                score = result.get("score", 0)
                print(f"  {i}. {title} (Score: {score:.2f})")
        else:
            print("  No semantic results found.")

        # Local search
        print(f"\n📁 LOCAL EVIDENCE: {evidence_type}")
        print("-" * 40)
        local_results = self.local_search(evidence_type)
        if local_results:
            for result in local_results[:5]:
                print(f"  - {result['path']}")
        else:
            print(f"  No local files mention '{evidence_type}'.")

        print("\n" + "=" * 60)


def parse_command(cmd: str, investigator: InvestigationQuery):
    """Parse and execute a query command."""
    cmd = cmd.strip()

    if not cmd:
        return

    # Parse command
    parts = cmd.split(None, 1)
    command = parts[0].lower()

    if command == "query" and len(parts) > 1:
        investigator.query(parts[1])
    elif command == "cross" and len(parts) > 1:
        entities = parts[1].split()
        if len(entities) >= 2:
            investigator.cross_reference(entities[0], entities[1])
        else:
            print("Usage: cross <entity1> <entity2>")
    elif command == "timeline" and len(parts) > 1:
        try:
            year = int(parts[1])
            investigator.timeline_query(year)
        except ValueError:
            print("Usage: timeline <year>")
    elif command == "evidence" and len(parts) > 1:
        investigator.evidence_query(parts[1])
    elif command in ("help", "?"):
        print_help()
    elif command in ("quit", "exit", "q"):
        print("Exiting.")
        sys.exit(0)
    else:
        # Treat as a direct query
        investigator.query(cmd)


def print_help():
    """Print help information."""
    print("""
INVESTIGATION QUERY TOOL
========================

Commands:
  query <text>          - Natural language search
  cross <e1> <e2>       - Cross-reference two entities
  timeline <year>       - Query events from a year
  evidence <type>       - Query specific evidence type
  help                  - Show this help
  quit                  - Exit

Examples:
  query How is Apple connected to DARPA?
  cross Apple DARPA
  timeline 2018
  evidence patent
  query smoking gun evidence
""")


def main():
    """Main entry point."""
    print("=" * 60)
    print("INVESTIGATION QUERY TOOL")
    print("Semantic Search for Investigation Evidence")
    print("=" * 60)

    investigator = InvestigationQuery()

    print("\nType 'help' for commands or enter a query directly.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            cmd = input("🔍 Query: ").strip()
            parse_command(cmd, investigator)
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
