#!/usr/bin/env python3
"""
Claude API Integration for Obsidian Connector

This module provides seamless integration between the Obsidian connector
and Claude AI, enabling AI-powered note analysis, generation, and search.

Requirements:
    pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python claude_integration.py
"""

import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from obsidian_connector import ObsidianConnector, Note

try:
    from anthropic import Anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("Warning: anthropic package not installed. Run: pip install anthropic")


class ClaudeObsidianIntegration:
    """
    Integration class that combines Obsidian connector with Claude API.
    """

    def __init__(self, vault_path: str = None, api_key: str = None):
        """
        Initialize the integration.

        Args:
            vault_path: Path to Obsidian vault (default: current directory)
            api_key: Anthropic API key (default: from ANTHROPIC_API_KEY env var)
        """
        self.connector = ObsidianConnector(vault_path)

        if not ANTHROPIC_AVAILABLE:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("API key required. Set ANTHROPIC_API_KEY or pass api_key parameter")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def ask_about_note(self, note_path: str, question: str, max_tokens: int = 1024) -> str:
        """
        Ask Claude a question about a specific note.

        Args:
            note_path: Path to the note
            question: Question to ask
            max_tokens: Maximum tokens in response

        Returns:
            Claude's response
        """
        note = self.connector.read_note(note_path)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=[{
                "role": "user",
                "content": f"""I have a note from my Obsidian vault:

Title: {note.title}
Tags: {', '.join(note.tags) if note.tags else 'None'}
Links: {', '.join(note.links) if note.links else 'None'}

Content:
{note.content}

Question: {question}"""
            }]
        )

        return message.content[0].text

    def analyze_note(self, note_path: str, save_analysis: bool = True) -> str:
        """
        Have Claude analyze a note and optionally save the analysis.

        Args:
            note_path: Path to the note to analyze
            save_analysis: Whether to save analysis as a new note

        Returns:
            Analysis text
        """
        note = self.connector.read_note(note_path)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Analyze this note from my Obsidian vault:

Title: {note.title}
Tags: {', '.join(note.tags)}
Word count: {note.word_count}

Content:
{note.content}

Please provide:
1. A concise summary
2. Key insights or themes
3. Suggested connections or related topics
4. Any action items or follow-ups"""
            }]
        )

        analysis = message.content[0].text

        if save_analysis:
            # Save analysis as new note
            analysis_content = f"""# Analysis: {note.title}

**Original Note:** [[{note.title}]]
**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Model:** {self.model}

{analysis}

#ai-analysis #claude
"""
            analysis_path = f"Analysis/Claude - {note.title}.md"
            self.connector.write_note(analysis_path, analysis_content)
            print(f"✓ Analysis saved to: {analysis_path}")

        return analysis

    def summarize_notes(self, note_paths: List[str], save_summary: bool = True) -> str:
        """
        Generate a summary of multiple notes.

        Args:
            note_paths: List of note paths to summarize
            save_summary: Whether to save the summary

        Returns:
            Summary text
        """
        notes_content = []
        for path in note_paths:
            note = self.connector.read_note(path)
            notes_content.append(f"## {note.title}\n\n{note.content}\n")

        combined = "\n\n".join(notes_content)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Summarize these related notes from my Obsidian vault:

{combined}

Provide a cohesive summary that:
1. Synthesizes the key information
2. Identifies common themes
3. Highlights important connections
4. Notes any gaps or areas needing exploration"""
            }]
        )

        summary = message.content[0].text

        if save_summary:
            summary_content = f"""# Summary: Multiple Notes

**Notes Analyzed:** {len(note_paths)}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Model:** {self.model}

## Notes Included
{chr(10).join([f"- [[{self.connector.read_note(p).title}]]" for p in note_paths])}

## Summary

{summary}

#summary #ai-generated #claude
"""
            summary_path = f"Analysis/Summary - {datetime.now().strftime('%Y%m%d-%H%M')}.md"
            self.connector.write_note(summary_path, summary_content)
            print(f"✓ Summary saved to: {summary_path}")

        return summary

    def smart_search(self, query: str, max_results: int = 5) -> str:
        """
        Use Claude to help interpret search results intelligently.

        Args:
            query: Search query
            max_results: Maximum number of results to analyze

        Returns:
            Intelligent search summary
        """
        # First, do traditional search
        results = self.connector.search_notes(query)

        if not results:
            return f"No notes found matching '{query}'"

        # Prepare context for Claude
        context = []
        for result in results[:max_results]:
            note = self.connector.read_note(result['path'])
            context.append(f"## {note.title}\n\n{note.content[:500]}...")

        combined_context = "\n\n".join(context)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""The user searched for: "{query}"

Here are the top {len(context)} matching notes from their vault:

{combined_context}

Please provide:
1. A brief summary of what these notes are about
2. How they relate to the search query
3. Key insights across these notes
4. Suggested next steps or related topics to explore"""
            }]
        )

        return message.content[0].text

    def generate_note(self, topic: str, include_tags: List[str] = None,
                     link_to: List[str] = None, save: bool = True) -> str:
        """
        Generate a new note on a topic using Claude.

        Args:
            topic: Topic for the note
            include_tags: Tags to include
            link_to: Notes to link to
            save: Whether to save the note

        Returns:
            Generated note content
        """
        # Build context from linked notes
        context = ""
        if link_to:
            context = "\n\nRelated notes for context:\n"
            for link in link_to:
                try:
                    note = self.connector.read_note(link)
                    context += f"\n## {note.title}\n{note.content[:300]}...\n"
                except:
                    pass

        tags_str = ' '.join([f'#{tag}' for tag in (include_tags or [])])

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Create a comprehensive note about: {topic}

The note should be in Markdown format suitable for Obsidian.

Include:
- Clear heading structure
- Well-organized content
- Relevant details and insights
- These tags at the end: {tags_str} #ai-generated

{context}

Format the note as if you were adding it to a knowledge base."""
            }]
        )

        content = message.content[0].text

        if save:
            # Clean up the filename
            filename = topic.replace('/', '-').replace('\\', '-')
            note_path = f"AI Generated/{filename}.md"
            self.connector.write_note(note_path, content)
            print(f"✓ Note generated and saved to: {note_path}")

        return content

    def extract_entities(self, note_path: str) -> Dict[str, List[str]]:
        """
        Extract entities (people, organizations, topics) from a note.

        Args:
            note_path: Path to the note

        Returns:
            Dictionary of entity types and lists
        """
        note = self.connector.read_note(note_path)

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Extract entities from this note:

{note.content}

Return a JSON object with these categories:
- people: List of person names
- organizations: List of organizations
- locations: List of locations
- topics: List of key topics/concepts
- dates: List of important dates

Return ONLY valid JSON, no other text."""
            }]
        )

        try:
            entities = json.loads(message.content[0].text)
            return entities
        except json.JSONDecodeError:
            return {"error": "Could not parse entity extraction"}

    def suggest_tags(self, note_path: str, max_tags: int = 5) -> List[str]:
        """
        Suggest tags for a note based on its content.

        Args:
            note_path: Path to the note
            max_tags: Maximum number of tags to suggest

        Returns:
            List of suggested tags
        """
        note = self.connector.read_note(note_path)

        # Get existing tags in vault for context
        all_tags = self.connector.get_all_tags()
        common_tags = list(all_tags.keys())[:20]  # Top 20 existing tags

        message = self.client.messages.create(
            model=self.model,
            max_tokens=256,
            messages=[{
                "role": "user",
                "content": f"""Suggest {max_tags} relevant tags for this note:

Title: {note.title}
Current tags: {', '.join(note.tags) if note.tags else 'None'}

Content:
{note.content[:1000]}

Common tags in this vault: {', '.join(common_tags)}

Return ONLY a comma-separated list of {max_tags} tag names (without # symbols)."""
            }]
        )

        tags_text = message.content[0].text.strip()
        suggested = [tag.strip().lstrip('#') for tag in tags_text.split(',')]
        return suggested[:max_tags]

    def find_connections(self, note_path: str) -> List[Dict]:
        """
        Find potential connections between this note and others.

        Args:
            note_path: Path to the note

        Returns:
            List of suggested connections with reasons
        """
        note = self.connector.read_note(note_path)

        # Get some context notes
        all_notes = self.connector.list_notes()[:50]  # Sample
        context_notes = []
        for path in all_notes:
            if path != note_path:
                try:
                    n = self.connector.read_note(path)
                    context_notes.append(f"- {n.title} (tags: {', '.join(n.tags[:3])})")
                except:
                    pass

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Find connections between this note and others in the vault.

Current note: {note.title}
Content: {note.content[:500]}...

Other notes in vault:
{chr(10).join(context_notes[:30])}

Suggest up to 5 notes that should be linked to this one. Return JSON array with:
[{{"title": "Note Title", "reason": "Why they should be connected"}}]

Return ONLY valid JSON array, no other text."""
            }]
        )

        try:
            connections = json.loads(message.content[0].text)
            return connections
        except json.JSONDecodeError:
            return []

    def batch_analyze_by_tag(self, tag: str, save_report: bool = True) -> str:
        """
        Analyze all notes with a specific tag and generate insights.

        Args:
            tag: Tag to filter by
            save_report: Whether to save the report

        Returns:
            Analysis report
        """
        notes = self.connector.search_by_tag(tag)

        if not notes:
            return f"No notes found with tag #{tag}"

        # Combine notes for analysis
        combined = f"# Notes tagged with #{tag}\n\n"
        for note in notes[:10]:  # Limit to 10 for token management
            combined += f"## {note.title}\n\n{note.content[:300]}...\n\n"

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{
                "role": "user",
                "content": f"""Analyze these notes all tagged with #{tag}:

{combined}

Provide:
1. Overview of what these notes cover
2. Common themes and patterns
3. Key insights
4. Gaps or areas to explore further
5. Suggested next actions"""
            }]
        )

        report = message.content[0].text

        if save_report:
            report_content = f"""# Tag Analysis: #{tag}

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Notes Analyzed:** {len(notes)}
**Model:** {self.model}

{report}

#tag-analysis #ai-generated #claude
"""
            report_path = f"Analysis/Tag Analysis - {tag}.md"
            self.connector.write_note(report_path, report_content)
            print(f"✓ Report saved to: {report_path}")

        return report


def main():
    """Example usage of Claude-Obsidian integration"""
    print("\n" + "="*80)
    print(" "*25 + "CLAUDE-OBSIDIAN INTEGRATION")
    print("="*80)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("\n❌ Error: ANTHROPIC_API_KEY not set")
        print("\nSet your API key:")
        print("  export ANTHROPIC_API_KEY='your-key-here'")
        print("\nGet your API key at: https://console.anthropic.com/")
        return

    try:
        # Initialize integration
        print("\nInitializing Claude-Obsidian integration...")
        integration = ClaudeObsidianIntegration()
        print("✓ Integration ready!")

        # Example 1: Analyze a note
        print("\n" + "="*80)
        print("EXAMPLE: Analyzing a note")
        print("="*80)

        notes = integration.connector.list_notes()
        if notes:
            sample_note = notes[0]
            print(f"\nAnalyzing: {sample_note}")
            analysis = integration.analyze_note(sample_note, save_analysis=False)
            print(f"\nAnalysis:\n{analysis[:500]}...")

        # Example 2: Smart search
        print("\n" + "="*80)
        print("EXAMPLE: Smart search")
        print("="*80)

        query = "investigation"
        print(f"\nSearching for: {query}")
        result = integration.smart_search(query, max_results=3)
        print(f"\n{result}")

        print("\n" + "="*80)
        print("✓ Examples completed!")
        print("="*80)
        print("\nSee claude_integration.py for more methods:")
        print("  • ask_about_note() - Ask questions about notes")
        print("  • generate_note() - Generate new notes")
        print("  • suggest_tags() - Get tag suggestions")
        print("  • find_connections() - Find related notes")
        print("  • extract_entities() - Extract people, orgs, etc.")
        print("  • batch_analyze_by_tag() - Analyze notes by tag")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
