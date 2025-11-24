#!/usr/bin/env python3
"""
Obsidian Vault to Supermemory Bulk Sync Script

This script syncs all markdown files from your Obsidian vault to Supermemory,
allowing you to search and query your notes using Supermemory's AI-powered API.

Requirements:
    - Python 3.7+
    - supermemory Python package
    - python-dotenv (for environment variables)

Usage:
    python3 supermemory_bulk_sync.py [--vault-path PATH] [--sync-log FILE] [--force]

Environment Variables:
    SUPERMEMORY_API_KEY: Your Supermemory API key (required)
    OBSIDIAN_VAULT_PATH: Path to your Obsidian vault (optional, defaults to current directory)
"""

import os
import sys
import json
import hashlib
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# Try to import required packages
try:
    from dotenv import load_dotenv
except ImportError:
    print("Warning: python-dotenv not installed. Using system environment variables only.")
    load_dotenv = lambda: None

try:
    from supermemory import Supermemory
except ImportError:
    print("ERROR: supermemory package not installed.")
    print("Install it with: pip install --pre supermemory")
    sys.exit(1)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class ObsidianSupermemorySync:
    """Handles syncing Obsidian vault to Supermemory"""
    
    def __init__(self, vault_path: str, api_key: str, sync_log_file: str = ".supermemory-sync.json"):
        self.vault_path = Path(vault_path).resolve()
        self.api_key = api_key
        self.sync_log_file = self.vault_path / sync_log_file
        self.client = None
        self.sync_state = self._load_sync_state()
        
    def _load_sync_state(self) -> Dict:
        """Load the sync state from disk"""
        if self.sync_log_file.exists():
            try:
                with open(self.sync_log_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Could not load sync state: {e}. Starting fresh.")
        return {
            "last_sync": None,
            "synced_files": {},
            "stats": {
                "total_synced": 0,
                "last_run_uploaded": 0,
                "last_run_skipped": 0,
                "last_run_errors": 0
            }
        }
    
    def _save_sync_state(self):
        """Save the sync state to disk"""
        try:
            with open(self.sync_log_file, 'w') as f:
                json.dump(self.sync_state, f, indent=2)
        except Exception as e:
            logger.error(f"Could not save sync state: {e}")
    
    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file content"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Could not compute hash for {file_path}: {e}")
            return ""
    
    def _should_sync_file(self, file_path: Path, force: bool = False) -> bool:
        """Determine if a file needs to be synced"""
        if force:
            return True
        
        relative_path = str(file_path.relative_to(self.vault_path))
        
        # Check if file was synced before
        if relative_path not in self.sync_state["synced_files"]:
            return True
        
        # Check if file has been modified
        current_hash = self._compute_file_hash(file_path)
        previous_hash = self.sync_state["synced_files"][relative_path].get("hash", "")
        
        return current_hash != previous_hash
    
    def _get_markdown_files(self) -> List[Path]:
        """Get all markdown files in the vault, excluding hidden and system files"""
        exclude_dirs = {'.git', '.obsidian', '.trash', 'node_modules'}
        markdown_files = []
        
        for md_file in self.vault_path.rglob('*.md'):
            # Skip if in excluded directory
            if any(excl in md_file.parts for excl in exclude_dirs):
                continue
            
            # Skip hidden files
            if any(part.startswith('.') for part in md_file.parts[len(self.vault_path.parts):]):
                continue
            
            markdown_files.append(md_file)
        
        return sorted(markdown_files)
    
    def _upload_to_supermemory(self, file_path: Path) -> bool:
        """Upload a single file to Supermemory"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                logger.info(f"Skipping empty file: {file_path.name}")
                return False
            
            relative_path = str(file_path.relative_to(self.vault_path))
            
            # Create metadata for the memory
            metadata = {
                "source": "obsidian_vault",
                "file_path": relative_path,
                "file_name": file_path.name,
                "sync_date": datetime.now().isoformat()
            }
            
            # Upload to Supermemory
            # Note: The actual API method may vary depending on Supermemory SDK version
            # This uses a common pattern, but may need adjustment
            logger.info(f"Uploading: {relative_path}")
            
            # Add title to content for better context
            title = file_path.stem
            formatted_content = f"# {title}\n\nFile: {relative_path}\n\n{content}"
            
            response = self.client.add(
                content=formatted_content,
                metadata=metadata
            )
            
            logger.info(f"✓ Uploaded successfully: {relative_path}")
            
            # Update sync state
            file_hash = self._compute_file_hash(file_path)
            self.sync_state["synced_files"][relative_path] = {
                "hash": file_hash,
                "last_synced": datetime.now().isoformat(),
                "supermemory_id": getattr(response, 'id', None)
            }
            
            return True
            
        except Exception as e:
            logger.error(f"✗ Failed to upload {file_path.name}: {str(e)}")
            return False
    
    def connect(self) -> bool:
        """Connect to Supermemory API"""
        try:
            self.client = Supermemory(api_key=self.api_key)
            logger.info("✓ Connected to Supermemory API")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to Supermemory: {e}")
            return False
    
    def sync(self, force: bool = False, dry_run: bool = False) -> Dict:
        """
        Sync vault to Supermemory
        
        Args:
            force: Force sync all files, ignoring cache
            dry_run: Don't actually upload, just show what would be synced
        
        Returns:
            Dictionary with sync statistics
        """
        if not self.connect():
            return {"error": "Connection failed"}
        
        logger.info(f"Starting sync of vault: {self.vault_path}")
        
        # Get all markdown files
        markdown_files = self._get_markdown_files()
        logger.info(f"Found {len(markdown_files)} markdown files")
        
        # Filter files that need syncing
        files_to_sync = [
            f for f in markdown_files 
            if self._should_sync_file(f, force=force)
        ]
        
        logger.info(f"Files to sync: {len(files_to_sync)}")
        
        if dry_run:
            logger.info("DRY RUN - No files will be uploaded")
            for file_path in files_to_sync:
                relative_path = str(file_path.relative_to(self.vault_path))
                logger.info(f"  Would sync: {relative_path}")
            return {
                "dry_run": True,
                "total_files": len(markdown_files),
                "files_to_sync": len(files_to_sync)
            }
        
        # Sync files
        uploaded = 0
        skipped = 0
        errors = 0
        
        for i, file_path in enumerate(files_to_sync, 1):
            logger.info(f"Progress: {i}/{len(files_to_sync)}")
            
            if self._upload_to_supermemory(file_path):
                uploaded += 1
            else:
                errors += 1
        
        skipped = len(markdown_files) - len(files_to_sync)
        
        # Update stats
        self.sync_state["last_sync"] = datetime.now().isoformat()
        self.sync_state["stats"]["total_synced"] = len(self.sync_state["synced_files"])
        self.sync_state["stats"]["last_run_uploaded"] = uploaded
        self.sync_state["stats"]["last_run_skipped"] = skipped
        self.sync_state["stats"]["last_run_errors"] = errors
        
        # Save state
        self._save_sync_state()
        
        # Print summary
        logger.info("=" * 60)
        logger.info("SYNC COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total files in vault: {len(markdown_files)}")
        logger.info(f"Uploaded: {uploaded}")
        logger.info(f"Skipped (unchanged): {skipped}")
        logger.info(f"Errors: {errors}")
        logger.info(f"Total synced lifetime: {self.sync_state['stats']['total_synced']}")
        logger.info("=" * 60)
        
        return {
            "total_files": len(markdown_files),
            "uploaded": uploaded,
            "skipped": skipped,
            "errors": errors,
            "total_synced": self.sync_state['stats']['total_synced']
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Sync Obsidian vault to Supermemory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync vault in current directory
  python3 supermemory_bulk_sync.py
  
  # Sync specific vault path
  python3 supermemory_bulk_sync.py --vault-path /path/to/vault
  
  # Force re-sync all files
  python3 supermemory_bulk_sync.py --force
  
  # Dry run (don't actually upload)
  python3 supermemory_bulk_sync.py --dry-run
  
Environment Variables:
  SUPERMEMORY_API_KEY    Your Supermemory API key (required)
  OBSIDIAN_VAULT_PATH    Path to vault (optional, defaults to current dir)
        """
    )
    
    parser.add_argument(
        '--vault-path',
        type=str,
        help='Path to Obsidian vault (default: current directory or OBSIDIAN_VAULT_PATH env var)'
    )
    
    parser.add_argument(
        '--sync-log',
        type=str,
        default='.supermemory-sync.json',
        help='Sync state log file (default: .supermemory-sync.json)'
    )
    
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force sync all files, ignoring cache'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be synced without uploading'
    )
    
    args = parser.parse_args()
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('SUPERMEMORY_API_KEY')
    if not api_key:
        logger.error("ERROR: SUPERMEMORY_API_KEY environment variable not set")
        logger.error("Please set it in your environment or in a .env file")
        logger.error("Example: export SUPERMEMORY_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    # Get vault path
    vault_path = args.vault_path or os.getenv('OBSIDIAN_VAULT_PATH') or os.getcwd()
    
    if not os.path.isdir(vault_path):
        logger.error(f"ERROR: Vault path does not exist: {vault_path}")
        sys.exit(1)
    
    logger.info(f"Vault path: {vault_path}")
    logger.info(f"Sync log: {args.sync_log}")
    
    # Create sync handler
    sync_handler = ObsidianSupermemorySync(
        vault_path=vault_path,
        api_key=api_key,
        sync_log_file=args.sync_log
    )
    
    # Run sync
    try:
        result = sync_handler.sync(force=args.force, dry_run=args.dry_run)
        
        if "error" in result:
            logger.error(f"Sync failed: {result['error']}")
            sys.exit(1)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        logger.info("\nSync interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
