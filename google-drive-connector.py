#!/usr/bin/env python3
"""
Google Drive Connector for Obsidian Vault
==========================================

Allows Claude to access and sync your Obsidian vault from anywhere
by fetching the vault manifest from Google Drive.

Usage:
    ./google-drive-connector.py search          # Search for manifest
    ./google-drive-connector.py connect         # Connect to vault
    ./google-drive-connector.py sync            # Sync vault
    ./google-drive-connector.py status          # Show connection status
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, Optional
import argparse


class GoogleDriveConnector:
    """Connector for accessing Obsidian vault via Google Drive."""

    def __init__(self):
        self.manifest_filename = "obsidian-vault-manifest.json"
        self.home = Path.home()
        self.config_dir = self.home / ".config" / "obsidian-vault-connector"
        self.config_file = self.config_dir / "connection.json"

        # Common Google Drive paths
        self.gdrive_paths = [
            self.home / "Google Drive",
            self.home / "GoogleDrive",
            self.home / "Library" / "CloudStorage" / "GoogleDrive-*",
            "/mnt/google-drive",
            Path("/") / "Volumes" / "GoogleDrive"
        ]

    def _ensure_config_dir(self):
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)

    def _save_connection(self, manifest_path: str, vault_path: str):
        """Save connection information."""
        self._ensure_config_dir()

        connection = {
            "manifest_path": str(manifest_path),
            "vault_path": str(vault_path),
            "connected_at": self._get_timestamp()
        }

        with open(self.config_file, 'w') as f:
            json.dump(connection, f, indent=2)

    def _load_connection(self) -> Optional[Dict]:
        """Load saved connection information."""
        if not self.config_file.exists():
            return None

        with open(self.config_file, 'r') as f:
            return json.load(f)

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().isoformat()

    def search_manifest(self) -> Optional[Path]:
        """
        Search for vault manifest in Google Drive.

        Returns path to manifest if found.
        """
        print("🔍 Searching for vault manifest in Google Drive...")

        # Method 1: Check common Google Drive paths
        for gdrive_pattern in self.gdrive_paths:
            gdrive_str = str(gdrive_pattern)

            if '*' in gdrive_str:
                # Handle wildcard paths
                import glob
                matching_paths = glob.glob(gdrive_str)
                for gdrive_path in matching_paths:
                    manifest = Path(gdrive_path) / self.manifest_filename
                    if manifest.exists():
                        print(f"✅ Found manifest: {manifest}")
                        return manifest
            else:
                # Direct path check
                gdrive_path = Path(gdrive_pattern)
                if gdrive_path.exists():
                    manifest = gdrive_path / self.manifest_filename
                    if manifest.exists():
                        print(f"✅ Found manifest: {manifest}")
                        return manifest

        # Method 2: Search current directory and parent directories
        current = Path.cwd()
        for _ in range(5):  # Search up to 5 levels up
            manifest = current / self.manifest_filename
            if manifest.exists():
                print(f"✅ Found manifest: {manifest}")
                return manifest
            current = current.parent

        # Method 3: Check if already in vault directory
        local_manifest = Path(self.manifest_filename)
        if local_manifest.exists():
            print(f"✅ Found manifest: {local_manifest.absolute()}")
            return local_manifest.absolute()

        print("❌ Manifest not found in common Google Drive locations")
        print("\n💡 Tips:")
        print("   1. Ensure Google Drive desktop app is installed and synced")
        print("   2. Upload 'obsidian-vault-manifest.json' to your Google Drive")
        print("   3. Or manually specify path: --manifest /path/to/manifest.json")

        return None

    def read_manifest(self, manifest_path: Path) -> Dict:
        """Read and parse vault manifest."""
        print(f"📖 Reading manifest: {manifest_path}")

        with open(manifest_path, 'r') as f:
            manifest = json.load(f)

        print(f"✅ Loaded manifest for: {manifest['vault_name']}")
        return manifest

    def clone_vault(self, manifest: Dict, target_dir: Optional[str] = None) -> Path:
        """
        Clone vault from repository.

        Args:
            manifest: Vault manifest dictionary
            target_dir: Target directory (optional)

        Returns:
            Path to cloned vault
        """
        repo_url = manifest['repository']['git_url']
        repo_name = manifest['repository']['name']

        if target_dir:
            vault_path = Path(target_dir)
        else:
            vault_path = Path.cwd() / repo_name

        if vault_path.exists():
            print(f"⚠️  Directory already exists: {vault_path}")
            print("   Use 'sync' command to update existing vault")
            return vault_path

        print(f"📦 Cloning vault from: {repo_url}")
        print(f"   Target: {vault_path}")

        try:
            subprocess.run(
                ['git', 'clone', repo_url, str(vault_path)],
                check=True,
                capture_output=True,
                text=True
            )
            print(f"✅ Vault cloned successfully!")
            return vault_path

        except subprocess.CalledProcessError as e:
            print(f"❌ Clone failed: {e.stderr}")
            sys.exit(1)

    def sync_vault(self, vault_path: Path) -> bool:
        """
        Sync vault using GitHub connector.

        Args:
            vault_path: Path to vault directory

        Returns:
            True if successful
        """
        print(f"🔄 Syncing vault: {vault_path}")

        connector_script = vault_path / "github-connector.py"

        if not connector_script.exists():
            print(f"⚠️  GitHub connector not found: {connector_script}")
            print("   Pulling latest changes with git...")

            try:
                subprocess.run(
                    ['git', 'pull'],
                    cwd=vault_path,
                    check=True,
                    capture_output=True,
                    text=True
                )
                print("✅ Vault synced with git pull")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Sync failed: {e.stderr}")
                return False

        # Use GitHub connector
        try:
            result = subprocess.run(
                ['python3', str(connector_script), 'sync'],
                cwd=vault_path,
                capture_output=True,
                text=True,
                check=True
            )
            print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Sync failed: {e.stderr}")
            return False

    def show_status(self):
        """Show connection status."""
        print("=" * 60)
        print("📊 Google Drive Connector Status")
        print("=" * 60)

        # Check for saved connection
        connection = self._load_connection()

        if connection:
            print(f"\n✅ Connected")
            print(f"   Manifest: {connection['manifest_path']}")
            print(f"   Vault: {connection['vault_path']}")
            print(f"   Connected: {connection['connected_at']}")

            # Check if vault exists
            vault_path = Path(connection['vault_path'])
            if vault_path.exists():
                print(f"\n📂 Vault Status:")
                print(f"   Path: {vault_path}")
                print(f"   Exists: ✅")

                # Check for GitHub connector
                connector = vault_path / "github-connector.py"
                if connector.exists():
                    print(f"   GitHub Connector: ✅")

                    # Get vault status
                    try:
                        result = subprocess.run(
                            ['python3', str(connector), 'status'],
                            cwd=vault_path,
                            capture_output=True,
                            text=True
                        )
                        print(f"\n{result.stdout}")
                    except Exception as e:
                        print(f"   Could not get status: {e}")
            else:
                print(f"\n⚠️  Vault directory not found: {vault_path}")
        else:
            print("\n❌ Not connected")
            print("   Run: ./google-drive-connector.py connect")

        # Check Google Drive access
        print("\n🔍 Google Drive Access:")
        manifest = self.search_manifest()
        if manifest:
            print(f"   Manifest found: ✅")
            print(f"   Location: {manifest}")
        else:
            print(f"   Manifest found: ❌")

        print("\n" + "=" * 60)

    def connect(self, manifest_path: Optional[str] = None, target_dir: Optional[str] = None):
        """
        Connect to vault via Google Drive.

        Args:
            manifest_path: Path to manifest (optional, will search if not provided)
            target_dir: Target directory for vault (optional)
        """
        print("🚀 Connecting to Obsidian vault via Google Drive...\n")

        # Find or use provided manifest
        if manifest_path:
            manifest_file = Path(manifest_path)
            if not manifest_file.exists():
                print(f"❌ Manifest not found: {manifest_path}")
                sys.exit(1)
        else:
            manifest_file = self.search_manifest()
            if not manifest_file:
                sys.exit(1)

        # Read manifest
        manifest = self.read_manifest(manifest_file)

        # Clone or locate vault
        vault_path = self.clone_vault(manifest, target_dir)

        # Save connection
        self._save_connection(str(manifest_file), str(vault_path))

        print(f"\n✅ Connected successfully!")
        print(f"\n📂 Vault location: {vault_path}")
        print(f"\n💡 Next steps:")
        print(f"   cd {vault_path}")
        print(f"   ./github-connector.py report")

    def open_vault(self):
        """Open vault directory."""
        connection = self._load_connection()

        if not connection:
            print("❌ Not connected. Run: ./google-drive-connector.py connect")
            sys.exit(1)

        vault_path = Path(connection['vault_path'])

        if not vault_path.exists():
            print(f"❌ Vault not found: {vault_path}")
            sys.exit(1)

        print(f"📂 Opening vault: {vault_path}")

        # Change to vault directory
        os.chdir(vault_path)
        print(f"✅ Now in: {Path.cwd()}")

        # Show quick status
        try:
            result = subprocess.run(
                ['python3', 'github-connector.py', 'report'],
                capture_output=True,
                text=True
            )
            print(result.stdout)
        except Exception:
            pass


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Google Drive Connector for Obsidian Vault',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s search                        # Search for manifest in Google Drive
  %(prog)s connect                       # Connect to vault (auto-search manifest)
  %(prog)s connect --manifest /path      # Connect with specific manifest
  %(prog)s sync                          # Sync connected vault
  %(prog)s status                        # Show connection status
  %(prog)s open                          # Open vault directory

Workflow with Claude:
  1. Upload obsidian-vault-manifest.json to Google Drive
  2. Ask Claude: "Search my Google Drive for obsidian-vault-manifest.json"
  3. Run: ./google-drive-connector.py connect
  4. Access vault: cd <vault-path>
  5. Use: ./github-connector.py <command>
        """
    )

    parser.add_argument(
        'command',
        choices=['search', 'connect', 'sync', 'status', 'open'],
        help='Command to execute'
    )

    parser.add_argument(
        '--manifest',
        help='Path to manifest file (for connect command)'
    )

    parser.add_argument(
        '--target',
        help='Target directory for vault (for connect command)'
    )

    args = parser.parse_args()

    # Initialize connector
    connector = GoogleDriveConnector()

    # Execute command
    if args.command == 'search':
        manifest = connector.search_manifest()
        if manifest:
            print(f"\n💡 To connect: ./google-drive-connector.py connect --manifest \"{manifest}\"")
        sys.exit(0 if manifest else 1)

    elif args.command == 'connect':
        connector.connect(args.manifest, args.target)

    elif args.command == 'sync':
        connection = connector._load_connection()
        if not connection:
            print("❌ Not connected. Run: ./google-drive-connector.py connect")
            sys.exit(1)

        vault_path = Path(connection['vault_path'])
        success = connector.sync_vault(vault_path)
        sys.exit(0 if success else 1)

    elif args.command == 'status':
        connector.show_status()

    elif args.command == 'open':
        connector.open_vault()


if __name__ == '__main__':
    main()
