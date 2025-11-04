"""Tests for the storage module"""
import tempfile
import pytest
from pathlib import Path
from scraper.storage import PatchStorage


@pytest.fixture
def temp_storage():
    """Create a temporary storage for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        storage = PatchStorage(str(db_path))
        yield storage


def test_save_and_retrieve_patch(temp_storage):
    """Test saving and retrieving a patch."""
    url = "https://github.com/test/repo/pull/1.patch"
    raw_patch = "diff --git a/file.py b/file.py\n..."
    parsed_data = {"files": [], "added": 10, "removed": 5}
    
    # Save
    row_id = temp_storage.save_patch(url, raw_patch, parsed_data)
    assert row_id > 0
    
    # Retrieve
    retrieved = temp_storage.get_patch_by_url(url)
    assert retrieved is not None
    assert retrieved["url"] == url
    assert retrieved["raw_patch"] == raw_patch
    assert retrieved["parse_error"] is None


def test_save_patch_with_error(temp_storage):
    """Test saving a patch with parse error."""
    url = "https://github.com/test/repo/pull/2.patch"
    raw_patch = "invalid patch"
    parse_error = "Failed to parse"
    
    row_id = temp_storage.save_patch(url, raw_patch, parse_error=parse_error)
    assert row_id > 0
    
    retrieved = temp_storage.get_patch_by_url(url)
    assert retrieved["parse_error"] == parse_error
    assert retrieved["parsed_data"] is None


def test_list_patches(temp_storage):
    """Test listing patches."""
    # Save multiple patches
    for i in range(5):
        url = f"https://github.com/test/repo/pull/{i}.patch"
        temp_storage.save_patch(url, f"patch {i}")
    
    patches = temp_storage.list_patches(limit=10)
    assert len(patches) == 5
    
    # Should be ordered by created_at DESC
    patches = temp_storage.list_patches(limit=2)
    assert len(patches) == 2


def test_duplicate_url_update(temp_storage):
    """Test that saving the same URL updates the existing record."""
    url = "https://github.com/test/repo/pull/1.patch"
    
    # First save
    temp_storage.save_patch(url, "original patch")
    
    # Second save with same URL
    temp_storage.save_patch(url, "updated patch", parsed_data={"updated": True})
    
    retrieved = temp_storage.get_patch_by_url(url)
    assert retrieved["raw_patch"] == "updated patch"
    
    # Should still have only one record
    all_patches = temp_storage.list_patches(limit=100)
    assert len(all_patches) == 1
