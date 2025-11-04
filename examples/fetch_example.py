#!/usr/bin/env python3
"""
Example: Fetch and analyze a GitHub .patch URL
Run: python3 examples/fetch_example.py
"""
import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from scraper.fetcher import fetch_patch
from scraper.parser import parse_patch
from scraper.storage import PatchStorage


async def main():
    # Example: Fetch a real GitHub PR patch
    # This is a small, public PR from the requests library
    url = "https://github.com/psf/requests/pull/6000.patch"
    
    print(f"🔍 Fetching: {url}")
    print()
    
    try:
        # Fetch the patch
        raw_patch = await fetch_patch(url)
        print(f"✓ Fetched {len(raw_patch)} bytes")
        
        # Parse the patch
        parsed = parse_patch(raw_patch)
        print(f"✓ Parsed successfully")
        print()
        
        # Display statistics
        print("📊 Statistics:")
        print(f"  Files changed: {len(parsed['files'])}")
        print(f"  Lines added:   +{parsed['added']}")
        print(f"  Lines removed: -{parsed['removed']}")
        print()
        
        # Display file details
        print("📁 Files:")
        for file in parsed['files']:
            status = ""
            if file['is_added_file']:
                status = " [NEW]"
            elif file['is_removed_file']:
                status = " [DELETED]"
            print(f"  • {file['path']}{status}")
        print()
        
        # Save to database
        storage = PatchStorage("data/patches.db")
        row_id = storage.save_patch(url, raw_patch, parsed)
        print(f"💾 Saved to database (id={row_id})")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
