#!/usr/bin/env python3
"""
Obsidian Vault CLI - Command-line interface for vault analysis
"""

import argparse
import sys
import json
from typing import Optional
from vault_api import ObsidianVault


class VaultCLI:
    """Command-line interface for Obsidian vault"""

    def __init__(self):
        self.vault = None

    def load_vault(self, path: str = '/home/user/obsidian-vault'):
        """Load the vault"""
        self.vault = ObsidianVault(path)
        self.vault.load()

    def cmd_info(self, args):
        """Show vault information"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        summary = self.vault.get_vault_summary()
        stats = summary['statistics']

        print("\n" + "="*60)
        print("OBSIDIAN VAULT INFORMATION")
        print("="*60)
        print(f"Vault Path: {summary['path']}")
        print(f"\nStatistics:")
        print(f"  Files: {stats['total_files']}")
        print(f"  Entities: {stats['total_entities']}")
        print(f"  Tags: {stats['total_tags']}")
        print(f"  Relationships: {stats['total_relationships']}")
        print(f"\nCategories:")
        for cat, count in summary['categories'].items():
            print(f"  {cat}: {count} files")
        print(f"\nTop Entities:")
        for i, entity in enumerate(summary['top_entities'][:10], 1):
            print(f"  {i}. {entity}")
        print("="*60 + "\n")

    def cmd_search(self, args):
        """Search the vault"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        results = self.vault.search(
            args.query,
            search_type=args.type,
            limit=args.limit
        )

        if not results:
            print(f"No results found for '{args.query}'")
            return

        print(f"\nSearch Results for '{args.query}' ({len(results)} results):\n")
        for i, result in enumerate(results, 1):
            relevance_bar = "█" * int(result.relevance * 10)
            print(f"{i}. {result.title}")
            print(f"   Type: {result.match_type} | Relevance: [{relevance_bar:<10}] {result.relevance:.2f}")
            if args.verbose and result.matched_text:
                preview = result.matched_text[:80].replace('\n', ' ')
                print(f"   Preview: {preview}...")
            print()

    def cmd_entities(self, args):
        """List or search entities"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        if args.query:
            entities = self.vault.search_entities(args.query)
            if not entities:
                print(f"No entities found matching '{args.query}'")
                return
            print(f"\nEntities matching '{args.query}':\n")
        else:
            entities = self.vault.list_entities()
            print(f"\nAll Entities ({len(entities)} total):\n")

        for i, entity in enumerate(entities, 1):
            print(f"{i}. {entity}")

        print()

    def cmd_entity(self, args):
        """Get detailed entity information"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        info = self.vault.get_entity_info(args.name)

        if not info:
            print(f"Entity '{args.name}' not found")
            return

        print(f"\n{'='*60}")
        print(f"ENTITY: {info['name']}")
        print(f"{'='*60}")
        print(f"Type: {info['type']}")
        print(f"File: {info['file']}")
        print(f"Mentions: {info['mentions_count']} times")
        print(f"\nTags: {', '.join(info['tags']) if info['tags'] else 'None'}")
        print(f"\nConnected Entities ({len(info['network']['nodes'])-1}):")
        for entity in sorted(info['network']['nodes']):
            if entity != info['name']:
                print(f"  - {entity}")
        print(f"{'='*60}\n")

    def cmd_graph(self, args):
        """Show entity relationships"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        if args.source and args.target:
            # Find path between entities
            path = self.vault.find_path(args.source, args.target)
            if path:
                print(f"\nPath from '{args.source}' to '{args.target}':")
                print(" → ".join(path))
            else:
                print(f"No path found between '{args.source}' and '{args.target}'")
            print()
        elif args.common:
            # Find common connections
            parts = args.common.split(',')
            if len(parts) != 2:
                print("Error: --common requires two entities separated by comma")
                return
            entity1, entity2 = parts[0].strip(), parts[1].strip()
            common = self.vault.find_common_connections(entity1, entity2)
            if common:
                print(f"\nCommon connections between '{entity1}' and '{entity2}':")
                for entity in common:
                    print(f"  - {entity}")
            else:
                print(f"No common connections found")
            print()
        elif args.name:
            # Show network around entity
            network = self.vault.get_entity_relationships(args.name)
            if network:
                print(f"\nNetwork around '{args.name}':")
                print(f"Connected entities ({len(network['nodes'])-1}):")
                for node in sorted(network['nodes']):
                    if node != args.name:
                        print(f"  - {node}")
                print(f"\nRelationships: {len(network['edges'])}")
                for edge in network['edges'][:10]:
                    print(f"  {edge['source']} → {edge['target']}")
                if len(network['edges']) > 10:
                    print(f"  ... and {len(network['edges'])-10} more")
            print()
        else:
            print("Error: Use --name, --source/--target, or --common")

    def cmd_files(self, args):
        """List vault files"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        if args.category:
            files = self.vault.list_files(category=args.category)
            print(f"\nFiles in category '{args.category}':\n")
        else:
            files = self.vault.list_files()
            print(f"\nAll vault files ({len(files)} total):\n")

        for i, file_path in enumerate(files, 1):
            file = self.vault.get_file(file_path)
            if file:
                print(f"{i}. {file.title}")
                print(f"   Path: {file_path}")
                if file.tags:
                    print(f"   Tags: {', '.join(sorted(file.tags))}")
                print()

    def cmd_tags(self, args):
        """List vault tags"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        tags = self.vault.list_tags()

        if args.tag:
            files = self.vault.get_files_by_tag(args.tag)
            if files:
                print(f"\nFiles tagged with '#{args.tag}' ({len(files)} files):\n")
                for file_path in files:
                    file = self.vault.get_file(file_path)
                    if file:
                        print(f"  - {file.title}")
            else:
                print(f"No files found with tag '#{args.tag}'")
            print()
        else:
            print(f"\nAll tags in vault ({len(tags)} unique tags):\n")
            # Sort by frequency
            for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:20]:
                print(f"  #{tag}: {count} files")
            if len(tags) > 20:
                print(f"  ... and {len(tags)-20} more tags")
            print()

    def cmd_related(self, args):
        """Find related files"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        file = self.vault.get_file_by_title(args.title)
        if not file:
            # Try as path
            file = self.vault.get_file(args.title)

        if not file:
            print(f"File '{args.title}' not found")
            return

        related = self.vault.find_related_files(file.relative_path, limit=args.limit)

        print(f"\nFiles related to '{file.title}':\n")
        for i, (related_path, score) in enumerate(related, 1):
            related_file = self.vault.get_file(related_path)
            if related_file:
                print(f"{i}. {related_file.title}")
                print(f"   Relevance: {'█'*int(score*2):<10} {score:.2f}")
                print()

    def cmd_export(self, args):
        """Export vault data"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        if args.format == 'json':
            data = self.vault.export_as_json(include_content=args.content)
            output = json.dumps(data, indent=2)

            if args.output:
                with open(args.output, 'w') as f:
                    f.write(output)
                print(f"Exported to {args.output}")
            else:
                print(output)
        elif args.format == 'csv':
            # Export files as CSV
            import csv

            files = self.vault.list_files()

            if args.output:
                f = open(args.output, 'w', newline='')
                writer = csv.writer(f)
            else:
                writer = csv.writer(sys.stdout)

            writer.writerow(['Title', 'Path', 'Category', 'Tags', 'Links', 'Mentions'])

            for file_path in files:
                file = self.vault.get_file(file_path)
                if file:
                    writer.writerow([
                        file.title,
                        file_path,
                        file.category or '',
                        ';'.join(sorted(file.tags)),
                        ';'.join(sorted(file.internal_links)),
                        str(len(self.vault.loader.tag_index.get(file.title, set())))
                    ])

            if args.output:
                f.close()
                print(f"Exported to {args.output}")

    def cmd_report(self, args):
        """Generate analysis report"""
        if not self.vault or not self.vault.is_loaded():
            self.load_vault(args.path)

        stats = self.vault.get_statistics()

        report = []
        report.append("="*70)
        report.append("OBSIDIAN VAULT ANALYSIS REPORT")
        report.append("="*70)
        report.append("")

        report.append("VAULT OVERVIEW")
        report.append("-" * 70)
        report.append(f"Total Files: {stats['total_files']}")
        report.append(f"Total Entities: {stats['total_entities']}")
        report.append(f"Total Tags: {stats['total_tags']}")
        report.append(f"Total Relationships: {stats['total_relationships']}")
        report.append("")

        report.append("CATEGORIES")
        report.append("-" * 70)
        for cat, count in stats['index_stats']['categories'].items():
            report.append(f"  {cat}: {count} files")
        report.append("")

        report.append("TOP ENTITIES BY MENTIONS")
        report.append("-" * 70)
        entity_mentions = stats['index_stats']['entity_mentions']
        for entity, count in sorted(entity_mentions.items(), key=lambda x: x[1], reverse=True)[:15]:
            report.append(f"  {entity}: {count} mentions")
        report.append("")

        report.append("="*70)

        output = "\n".join(report)

        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"Report written to {args.output}")
        else:
            print("\n" + output)

    def main(self):
        """Main CLI entry point"""
        parser = argparse.ArgumentParser(
            description='Obsidian Vault Analysis Tool',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
Examples:
  %(prog)s info                           Show vault information
  %(prog)s search "investigation"         Search vault
  %(prog)s entities                       List all entities
  %(prog)s entity "Junyuan Wang"          Get entity details
  %(prog)s graph --name "Junyuan Wang"    Show entity network
  %(prog)s files --category Analysis      List files by category
  %(prog)s tags                           List all tags
  %(prog)s export --format json --output vault.json
            '''
        )

        parser.add_argument(
            '--path',
            default='/home/user/obsidian-vault',
            help='Path to Obsidian vault (default: /home/user/obsidian-vault)'
        )

        subparsers = parser.add_subparsers(dest='command', help='Command to run')

        # info command
        subparsers.add_parser('info', help='Show vault information')

        # search command
        search_parser = subparsers.add_parser('search', help='Search vault')
        search_parser.add_argument('query', help='Search query')
        search_parser.add_argument(
            '--type',
            choices=['all', 'title', 'content', 'tags', 'entities'],
            default='all',
            help='Search type'
        )
        search_parser.add_argument(
            '--limit',
            type=int,
            default=20,
            help='Maximum results (default: 20)'
        )
        search_parser.add_argument(
            '-v', '--verbose',
            action='store_true',
            help='Show matched text preview'
        )

        # entities command
        entities_parser = subparsers.add_parser('entities', help='List or search entities')
        entities_parser.add_argument(
            'query',
            nargs='?',
            help='Search query (optional)'
        )

        # entity command
        entity_parser = subparsers.add_parser('entity', help='Get entity details')
        entity_parser.add_argument('name', help='Entity name')

        # graph command
        graph_parser = subparsers.add_parser('graph', help='Show entity relationships')
        graph_parser.add_argument('--name', help='Entity name for network')
        graph_parser.add_argument('--source', help='Source entity')
        graph_parser.add_argument('--target', help='Target entity')
        graph_parser.add_argument(
            '--common',
            help='Find common connections (format: "entity1,entity2")'
        )

        # files command
        files_parser = subparsers.add_parser('files', help='List vault files')
        files_parser.add_argument(
            '--category',
            help='Filter by category'
        )

        # tags command
        tags_parser = subparsers.add_parser('tags', help='List vault tags')
        tags_parser.add_argument(
            '--tag',
            help='Show files with this tag'
        )

        # related command
        related_parser = subparsers.add_parser('related', help='Find related files')
        related_parser.add_argument('title', help='File title or path')
        related_parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum results (default: 10)'
        )

        # export command
        export_parser = subparsers.add_parser('export', help='Export vault data')
        export_parser.add_argument(
            '--format',
            choices=['json', 'csv'],
            default='json',
            help='Export format (default: json)'
        )
        export_parser.add_argument(
            '--output',
            help='Output file (if not specified, prints to stdout)'
        )
        export_parser.add_argument(
            '--content',
            action='store_true',
            help='Include full file content (JSON only)'
        )

        # report command
        report_parser = subparsers.add_parser('report', help='Generate analysis report')
        report_parser.add_argument(
            '--output',
            help='Output file (if not specified, prints to stdout)'
        )

        args = parser.parse_args()

        if not args.command:
            parser.print_help()
            return

        # Route commands
        try:
            if args.command == 'info':
                self.cmd_info(args)
            elif args.command == 'search':
                self.cmd_search(args)
            elif args.command == 'entities':
                self.cmd_entities(args)
            elif args.command == 'entity':
                self.cmd_entity(args)
            elif args.command == 'graph':
                self.cmd_graph(args)
            elif args.command == 'files':
                self.cmd_files(args)
            elif args.command == 'tags':
                self.cmd_tags(args)
            elif args.command == 'related':
                self.cmd_related(args)
            elif args.command == 'export':
                self.cmd_export(args)
            elif args.command == 'report':
                self.cmd_report(args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    cli = VaultCLI()
    cli.main()
