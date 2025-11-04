"""Parse unified diff/patch content using unidiff"""
from typing import Dict, Any, List
from unidiff import PatchSet


def parse_patch(patch_text: str) -> Dict[str, Any]:
    """Parse a unified diff/patch into structured data.
    
    Args:
        patch_text: Raw .patch content (unified diff format)
    
    Returns:
        Dictionary with parsed patch data:
        {
            "files": [
                {
                    "path": str,
                    "source_file": str,
                    "target_file": str,
                    "is_added_file": bool,
                    "is_removed_file": bool,
                    "is_binary_file": bool,
                    "hunks": [
                        {
                            "source_start": int,
                            "source_length": int,
                            "target_start": int,
                            "target_length": int,
                            "section_header": str,
                            "added": int,
                            "removed": int,
                        }
                    ]
                }
            ],
            "added": int,  # total added lines
            "removed": int,  # total removed lines
        }
    
    Raises:
        Exception if patch cannot be parsed
    """
    patchset = PatchSet(patch_text)
    
    files = []
    total_added = 0
    total_removed = 0
    
    for patched_file in patchset:
        hunks = []
        for hunk in patched_file:
            added = hunk.added
            removed = hunk.removed
            total_added += added
            total_removed += removed
            hunks.append({
                "source_start": hunk.source_start,
                "source_length": hunk.source_length,
                "target_start": hunk.target_start,
                "target_length": hunk.target_length,
                "section_header": hunk.section_header,
                "added": added,
                "removed": removed,
            })
        
        files.append({
            "path": patched_file.path,
            "source_file": patched_file.source_file,
            "target_file": patched_file.target_file,
            "is_added_file": patched_file.is_added_file,
            "is_removed_file": patched_file.is_removed_file,
            "is_binary_file": patched_file.is_binary_file,
            "hunks": hunks,
        })
    
    return {
        "files": files,
        "added": total_added,
        "removed": total_removed,
    }
