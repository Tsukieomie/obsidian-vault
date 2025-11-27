#!/usr/bin/env python3
"""
Supermemory Vault Sync Script
Uploads Obsidian vault documents to Supermemory for semantic search.

Usage:
    python3 .supermemory_sync.py

Environment:
    API_KEY - Supermemory API key (from ~/.env)
"""

import os
import sys
import time
import json
import hashlib
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

# Document categories with priority weights
CATEGORIES = {
    "patent": {"priority": 1, "tags": ["patent", "evidence", "legal"]},
    "entity": {"priority": 1, "tags": ["entity", "investigation"]},
    "video": {"priority": 1, "tags": ["video", "testimony", "evidence"]},
    "analysis": {"priority": 2, "tags": ["analysis", "investigation"]},
    "timeline": {"priority": 1, "tags": ["timeline", "chronology"]},
    "technical": {"priority": 2, "tags": ["technical", "infrastructure"]},
    "framework": {"priority": 2, "tags": ["framework", "legal"]},
    "general": {"priority": 3, "tags": ["general", "notes"]},
}

# Keywords for auto-categorization
CATEGORY_KEYWORDS = {
    "patent": ["patent", "US10945618", "filing", "claims"],
    "entity": ["DARPA", "Apple", "FreerLogic", "entity", "profile"],
    "video": ["video", "testimony", "Dr. Giordano", "briefing", "youtube"],
    "analysis": ["analysis", "deep dive", "investigation"],
    "timeline": ["timeline", "chronology", "2018", "2019", "2020", "2021"],
    "technical": ["infrastructure", "network", "technical", "architecture"],
    "framework": ["legal", "framework", "case", "evidence"],
}


class SupermemorySync:
    """Handles synchronization of vault documents to Supermemory."""

    def __init__(self, require_api_key: bool = True):
        self.api_key = self._get_api_key(required=require_api_key)
        self.headers = {
            "Authorization": f"Bearer {self.api_key}" if self.api_key else "",
            "Content-Type": "application/json",
        }
        self.sync_log = []
        self.stats = {"uploaded": 0, "skipped": 0, "failed": 0}

    def _get_api_key(self, required: bool = True) -> str:
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
                            # Remove quotes if present
                            api_key = api_key.strip("'\"")
                            break
        if not api_key and required:
            print("Error: API_KEY not found in environment or ~/.env")
            print("Set with: export API_KEY=your-api-key")
            sys.exit(1)
        return api_key or ""

    def _categorize_document(self, path: Path, content: str) -> str:
        """Determine document category based on path and content."""
        path_str = str(path).lower()
        content_lower = content.lower()

        # Check path-based categories
        if "patent" in path_str:
            return "patent"
        if "entit" in path_str:
            return "entity"
        if "video" in path_str or "youtube" in path_str:
            return "video"
        if "timeline" in path_str:
            return "timeline"
        if "technical" in path_str:
            return "technical"
        if "analysis" in path_str:
            return "analysis"

        # Check content-based categories
        for category, keywords in CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in content_lower:
                    return category

        return "general"

    def _generate_tags(self, path: Path, content: str, category: str) -> list:
        """Generate tags for a document."""
        tags = CATEGORIES.get(category, {}).get("tags", []).copy()

        # Add filename-based tags
        filename = path.stem.lower().replace("_", "-").replace(" ", "-")
        tags.append(filename)

        # Add content-based tags
        content_lower = content.lower()
        tag_keywords = [
            ("darpa", "darpa"),
            ("apple", "apple"),
            ("freerlogic", "freerlogic"),
            ("patent", "patent"),
            ("smoking gun", "smoking-gun"),
            ("tier 1", "tier-1"),
            ("dr. giordano", "dr-giordano"),
            ("neural", "neural-monitoring"),
            ("investigation", "investigation"),
        ]
        for keyword, tag in tag_keywords:
            if keyword in content_lower and tag not in tags:
                tags.append(tag)

        return tags

    def _calculate_hash(self, content: str) -> str:
        """Calculate hash of content for change detection."""
        return hashlib.md5(content.encode()).hexdigest()

    def _upload_document(
        self,
        title: str,
        content: str,
        metadata: dict,
        tags: list,
    ) -> bool:
        """Upload a single document to Supermemory."""
        payload = {
            "content": content,
            "title": title,
            "metadata": metadata,
            "tags": tags,
        }

        try:
            response = requests.post(
                f"{BASE_URL}/memorize",
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            if response.status_code in (200, 201):
                return True
            else:
                print(f"  Error: {response.status_code} - {response.text[:100]}")
                return False
        except requests.exceptions.Timeout:
            print("  Error: Request timed out")
            return False
        except requests.exceptions.RequestException as e:
            print(f"  Error: {e}")
            return False

    def _get_markdown_files(self, priority_only: bool = False) -> list:
        """Get list of markdown files to sync."""
        files = []

        for md_file in VAULT_DIR.rglob("*.md"):
            # Skip hidden files and directories
            if any(part.startswith(".") for part in md_file.parts[len(VAULT_DIR.parts):]):
                continue

            # Read content
            try:
                content = md_file.read_text(encoding="utf-8")
            except Exception:
                continue

            # Skip small/empty files
            if len(content) < 100:
                continue

            # Determine category
            category = self._categorize_document(md_file, content)
            priority = CATEGORIES.get(category, {}).get("priority", 3)

            if priority_only and priority > 1:
                continue

            files.append(
                {
                    "path": md_file,
                    "content": content,
                    "category": category,
                    "priority": priority,
                }
            )

        # Sort by priority
        files.sort(key=lambda x: x["priority"])
        return files

    def sync_vault(self, priority_only: bool = False):
        """Sync vault documents to Supermemory."""
        files = self._get_markdown_files(priority_only)

        if not files:
            print("No files to sync.")
            return

        print(f"\nFound {len(files)} files to sync.\n")
        print("=" * 60)

        for i, file_info in enumerate(files, 1):
            path = file_info["path"]
            content = file_info["content"]
            category = file_info["category"]

            relative_path = path.relative_to(VAULT_DIR)
            title = path.stem

            tags = self._generate_tags(path, content, category)
            metadata = {
                "path": str(relative_path),
                "category": category,
                "size": len(content),
                "hash": self._calculate_hash(content),
            }

            print(f"[{i}/{len(files)}] {relative_path}")
            print(f"  Category: {category}")
            print(f"  Tags: {', '.join(tags[:5])}")

            if self._upload_document(title, content, metadata, tags):
                print("  ✅ Uploaded")
                self.stats["uploaded"] += 1
                self.sync_log.append({"file": str(relative_path), "status": "uploaded"})
            else:
                print("  ❌ Failed")
                self.stats["failed"] += 1
                self.sync_log.append({"file": str(relative_path), "status": "failed"})

            # Rate limiting
            time.sleep(1)
            print()

        print("=" * 60)
        print("\nSync Complete!")
        print(f"  Uploaded: {self.stats['uploaded']}")
        print(f"  Failed: {self.stats['failed']}")
        print(f"  Skipped: {self.stats['skipped']}")

    def list_categories(self):
        """List files by category."""
        files = self._get_markdown_files()

        by_category = {}
        for f in files:
            cat = f["category"]
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(f["path"].relative_to(VAULT_DIR))

        print("\nFiles by Category:")
        print("=" * 60)
        for cat, cat_files in sorted(by_category.items()):
            priority = CATEGORIES.get(cat, {}).get("priority", 3)
            print(f"\n{cat.upper()} (Priority {priority})")
            for f in cat_files:
                print(f"  - {f}")
        print()


def main():
    """Main entry point."""
    print("=" * 60)
    print("SUPERMEMORY VAULT SYNC")
    print("=" * 60)
    print("\nOptions:")
    print("  1. Sync priority documents only (recommended first)")
    print("  2. Sync all documents (full backup)")
    print("  3. List files by category")
    print("  4. Exit")
    print()

    try:
        choice = input("Select option [1-4]: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        sys.exit(0)

    if choice == "3":
        # List categories doesn't need API key
        sync = SupermemorySync(require_api_key=False)
        sync.list_categories()
    elif choice == "1":
        sync = SupermemorySync(require_api_key=True)
        print("\nStarting priority sync...")
        sync.sync_vault(priority_only=True)
    elif choice == "2":
        sync = SupermemorySync(require_api_key=True)
        print("\nStarting full sync...")
        sync.sync_vault(priority_only=False)
    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid option. Exiting.")


if __name__ == "__main__":
    main()
