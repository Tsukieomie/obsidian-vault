#!/usr/bin/env python3
"""
GitHub Connector for Claude - Smart Git Operations for Obsidian Vault
=====================================================================

A intelligent GitHub connector that provides:
- Smart commit message generation
- Entity change tracking
- TODO-based issue creation
- Activity reporting
"""

import os
import sys
import subprocess
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import argparse


class GitHubConnector:
    """Smart GitHub connector for investigation vault."""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path).resolve()
        self.config_path = self.vault_path / "github-connector.yml"
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            print(f"⚠️  Config file not found: {self.config_path}")
            return self._default_config()

        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            'repository': {'remote': 'origin', 'branch_prefix': 'claude/'},
            'commit_analysis': {'enabled': True},
            'sync': {'pull_before_push': True}
        }

    def _run_git(self, args: List[str], check=True) -> subprocess.CompletedProcess:
        """Run a git command in the vault directory."""
        cmd = ['git'] + args
        return subprocess.run(
            cmd,
            cwd=self.vault_path,
            capture_output=True,
            text=True,
            check=check
        )

    def get_status(self) -> Dict[str, List[str]]:
        """Get current git status organized by change type."""
        result = self._run_git(['status', '--porcelain'])

        status = {
            'modified': [],
            'added': [],
            'deleted': [],
            'untracked': []
        }

        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            code = line[:2]
            filepath = line[3:]

            if code == '??':
                status['untracked'].append(filepath)
            elif 'M' in code:
                status['modified'].append(filepath)
            elif 'A' in code:
                status['added'].append(filepath)
            elif 'D' in code:
                status['deleted'].append(filepath)

        return status

    def analyze_changes(self, status: Dict[str, List[str]]) -> str:
        """Generate intelligent commit message based on changes."""
        if not self.config.get('commit_analysis', {}).get('enabled', True):
            return f"Auto-sync: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        all_files = (status['modified'] + status['added'] +
                     status['deleted'] + status['untracked'])

        if not all_files:
            return "No changes"

        # Analyze file patterns
        entity_files = [f for f in all_files if f.startswith('Entities/')]
        analysis_files = [f for f in all_files if f.startswith('Analysis/')]
        technical_files = [f for f in all_files if f.startswith('Technical/')]

        # Generate context-aware message
        messages = []

        if entity_files:
            # Extract entity names
            entities = []
            for f in entity_files:
                name = Path(f).stem.replace('_', ' ')
                entities.append(name)

            if len(entities) == 1:
                messages.append(f"Update entity profile: {entities[0]}")
            else:
                messages.append(f"Update {len(entities)} entity profiles")

        if analysis_files:
            # Get analysis file names
            analyses = [Path(f).stem for f in analysis_files]
            if len(analyses) == 1:
                messages.append(f"Update analysis: {analyses[0]}")
            else:
                messages.append(f"Update {len(analyses)} analysis documents")

        if technical_files:
            messages.append(f"Update technical analysis ({len(technical_files)} files)")

        # Fallback to general message
        if not messages:
            file_count = len(all_files)
            if file_count == 1:
                messages.append(f"Update: {Path(all_files[0]).name}")
            else:
                messages.append(f"Update {file_count} files")

        return " | ".join(messages)

    def get_changed_entities(self, status: Dict[str, List[str]]) -> List[str]:
        """Get list of entities that have been modified."""
        entity_files = [f for f in status['modified'] + status['added']
                       if f.startswith('Entities/')]

        entities = []
        for f in entity_files:
            # Extract entity name from path
            name = Path(f).stem.replace('_', ' ')
            entity_type = 'Organization' if 'Organizations' in f else 'Person'
            entities.append(f"{entity_type}: {name}")

        return entities

    def sync(self, message: Optional[str] = None, push: bool = True) -> bool:
        """
        Perform intelligent sync operation.

        Args:
            message: Custom commit message (optional)
            push: Whether to push after committing

        Returns:
            True if successful, False otherwise
        """
        print("🔄 Starting GitHub sync...")

        # Check for changes
        status = self.get_status()
        total_changes = sum(len(files) for files in status.values())

        if total_changes == 0:
            print("✅ No changes to sync")
            return True

        print(f"📊 Found {total_changes} changes:")
        if status['modified']:
            print(f"   Modified: {len(status['modified'])}")
        if status['added']:
            print(f"   Added: {len(status['added'])}")
        if status['deleted']:
            print(f"   Deleted: {len(status['deleted'])}")
        if status['untracked']:
            print(f"   Untracked: {len(status['untracked'])}")

        # Pull latest changes if configured
        if self.config.get('sync', {}).get('pull_before_push', True):
            print("⬇️  Pulling latest changes...")
            try:
                result = self._run_git(['pull', '--rebase'], check=False)
                if result.returncode != 0:
                    print(f"⚠️  Pull warning: {result.stderr}")
            except Exception as e:
                print(f"⚠️  Pull failed: {e}")

        # Generate commit message
        if not message:
            message = self.analyze_changes(status)
            print(f"💬 Generated message: {message}")

        # Show entity changes if enabled
        if self.config.get('entity_tracking', {}).get('enabled', True):
            entities = self.get_changed_entities(status)
            if entities:
                print(f"👥 Entity changes:")
                for entity in entities:
                    print(f"   - {entity}")

        # Stage all changes
        print("➕ Staging changes...")
        self._run_git(['add', '-A'])

        # Commit
        print("💾 Creating commit...")
        try:
            self._run_git(['commit', '-m', message])
        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e.stderr}")
            return False

        # Push if requested
        if push:
            print("⬆️  Pushing to remote...")
            current_branch = self._run_git(['branch', '--show-current']).stdout.strip()

            try:
                self._run_git(['push', '-u', 'origin', current_branch])
                print(f"✅ Successfully pushed to {current_branch}")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Push failed: {e.stderr}")
                return False

        print("✅ Changes committed locally")
        return True

    def create_issue(self, title: str, body: str = "", labels: List[str] = None) -> None:
        """
        Create a GitHub issue (requires gh CLI).

        Args:
            title: Issue title
            body: Issue description
            labels: List of labels to apply
        """
        print(f"📝 Creating GitHub issue: {title}")

        # Check if gh CLI is available
        try:
            subprocess.run(['gh', '--version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ GitHub CLI (gh) not available.")
            print("💡 Install from: https://cli.github.com/")
            print(f"\n📋 Issue details:")
            print(f"   Title: {title}")
            if body:
                print(f"   Body: {body}")
            return

        # Build gh command
        cmd = ['gh', 'issue', 'create', '--title', title]

        if body:
            cmd.extend(['--body', body])

        if labels:
            cmd.extend(['--label', ','.join(labels)])
        elif 'issue_tracking' in self.config:
            default_labels = self.config['issue_tracking'].get('labels', [])
            if default_labels:
                cmd.extend(['--label', ','.join(default_labels)])

        try:
            result = subprocess.run(cmd, cwd=self.vault_path, capture_output=True, text=True, check=True)
            print(f"✅ Issue created: {result.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create issue: {e.stderr}")

    def scan_todos(self) -> List[Dict[str, str]]:
        """Scan configured files for TODO items."""
        if not self.config.get('issue_tracking', {}).get('enabled', True):
            return []

        todo_files = self.config.get('issue_tracking', {}).get('todo_sources', [])
        todos = []

        todo_pattern = re.compile(r'-\s*\[\s*\]\s*(.+)', re.IGNORECASE)

        for todo_file in todo_files:
            file_path = self.vault_path / todo_file
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    match = todo_pattern.search(line)
                    if match:
                        todos.append({
                            'file': todo_file,
                            'line': line_num,
                            'task': match.group(1).strip()
                        })

        return todos

    def report(self) -> None:
        """Generate activity report."""
        print("=" * 60)
        print("📊 GitHub Connector Report")
        print("=" * 60)

        # Current branch
        branch = self._run_git(['branch', '--show-current']).stdout.strip()
        print(f"\n🌿 Current Branch: {branch}")

        # Status
        status = self.get_status()
        total_changes = sum(len(files) for files in status.values())
        print(f"\n📝 Working Directory Status:")
        print(f"   Total changes: {total_changes}")
        if status['modified']:
            print(f"   Modified: {len(status['modified'])}")
        if status['added']:
            print(f"   Added: {len(status['added'])}")
        if status['deleted']:
            print(f"   Deleted: {len(status['deleted'])}")
        if status['untracked']:
            print(f"   Untracked: {len(status['untracked'])}")

        # Recent commits
        if self.config.get('reporting', {}).get('include_recent_commits', True):
            num_commits = self.config.get('reporting', {}).get('include_recent_commits', 5)
            print(f"\n📜 Recent Commits (last {num_commits}):")
            result = self._run_git(['log', f'-{num_commits}', '--pretty=format:%h - %s (%cr)'])
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")

        # Entity changes
        if self.config.get('entity_tracking', {}).get('enabled', True):
            entities = self.get_changed_entities(status)
            if entities:
                print(f"\n👥 Modified Entities:")
                for entity in entities:
                    print(f"   - {entity}")

        # TODO items
        todos = self.scan_todos()
        if todos:
            print(f"\n✅ TODO Items Found ({len(todos)}):")
            for todo in todos[:10]:  # Show first 10
                print(f"   - {todo['task']}")
                print(f"     ({todo['file']}:{todo['line']})")
            if len(todos) > 10:
                print(f"   ... and {len(todos) - 10} more")

        print("\n" + "=" * 60)

    def list_entities(self) -> None:
        """List all tracked entities."""
        print("👥 Tracked Entities\n")

        # Organizations
        org_dir = self.vault_path / "Entities" / "Organizations"
        if org_dir.exists():
            orgs = sorted([f.stem.replace('_', ' ') for f in org_dir.glob('*.md')])
            print(f"Organizations ({len(orgs)}):")
            for org in orgs:
                print(f"  - {org}")

        # People
        people_dir = self.vault_path / "Entities" / "People"
        if people_dir.exists():
            people = sorted([f.stem.replace('_', ' ') for f in people_dir.glob('*.md')])
            print(f"\nPeople ({len(people)}):")
            for person in people:
                print(f"  - {person}")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='GitHub Connector for Claude - Smart Git Operations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s sync                    # Smart sync with auto-generated message
  %(prog)s sync -m "Custom msg"    # Sync with custom message
  %(prog)s sync --no-push          # Commit but don't push
  %(prog)s report                  # Show activity report
  %(prog)s create-issue "Title"    # Create GitHub issue
  %(prog)s todos                   # List TODO items
  %(prog)s entities                # List all entities
        """
    )

    parser.add_argument(
        'command',
        choices=['sync', 'report', 'create-issue', 'todos', 'entities', 'status'],
        help='Command to execute'
    )

    parser.add_argument(
        'args',
        nargs='*',
        help='Additional arguments for the command'
    )

    parser.add_argument(
        '-m', '--message',
        help='Custom commit message for sync'
    )

    parser.add_argument(
        '--no-push',
        action='store_true',
        help='Commit but do not push (for sync command)'
    )

    parser.add_argument(
        '--vault',
        default='.',
        help='Path to vault directory (default: current directory)'
    )

    args = parser.parse_args()

    # Initialize connector
    connector = GitHubConnector(args.vault)

    # Execute command
    if args.command == 'sync':
        success = connector.sync(
            message=args.message,
            push=not args.no_push
        )
        sys.exit(0 if success else 1)

    elif args.command == 'report':
        connector.report()

    elif args.command == 'status':
        status = connector.get_status()
        total = sum(len(files) for files in status.values())
        print(f"Changes: {total}")
        for change_type, files in status.items():
            if files:
                print(f"\n{change_type.capitalize()}:")
                for f in files:
                    print(f"  - {f}")

    elif args.command == 'create-issue':
        if not args.args:
            print("❌ Error: Issue title required")
            print("Usage: github-connector create-issue \"Issue title\" [body]")
            sys.exit(1)

        title = args.args[0]
        body = args.args[1] if len(args.args) > 1 else ""
        connector.create_issue(title, body)

    elif args.command == 'todos':
        todos = connector.scan_todos()
        if todos:
            print(f"✅ Found {len(todos)} TODO items:\n")
            for i, todo in enumerate(todos, 1):
                print(f"{i}. {todo['task']}")
                print(f"   ({todo['file']}:{todo['line']})\n")
        else:
            print("No TODO items found")

    elif args.command == 'entities':
        connector.list_entities()


if __name__ == '__main__':
    main()
