"""Tests for the parser module"""
import pytest
from scraper.parser import parse_patch


# Sample unified diff
SAMPLE_PATCH = """diff --git a/example.py b/example.py
index 1234567..abcdefg 100644
--- a/example.py
+++ b/example.py
@@ -1,5 +1,6 @@
 def hello():
-    print("Hello")
+    print("Hello, world!")
+    return True
 
 def main():
     hello()
"""


def test_parse_patch_basic():
    """Test parsing a simple patch."""
    result = parse_patch(SAMPLE_PATCH)
    
    assert "files" in result
    assert "added" in result
    assert "removed" in result
    
    assert len(result["files"]) == 1
    assert result["added"] == 2
    assert result["removed"] == 1
    
    file_data = result["files"][0]
    assert file_data["path"] == "example.py"
    assert file_data["is_added_file"] is False
    assert file_data["is_removed_file"] is False
    assert len(file_data["hunks"]) == 1
    
    hunk = file_data["hunks"][0]
    assert hunk["source_start"] == 1
    assert hunk["target_start"] == 1
    assert hunk["added"] == 2
    assert hunk["removed"] == 1


def test_parse_patch_empty():
    """Test parsing an empty patch."""
    result = parse_patch("")
    
    assert result["files"] == []
    assert result["added"] == 0
    assert result["removed"] == 0


def test_parse_patch_new_file():
    """Test parsing a patch for a new file."""
    new_file_patch = """diff --git a/newfile.txt b/newfile.txt
new file mode 100644
index 0000000..1234567
--- /dev/null
+++ b/newfile.txt
@@ -0,0 +1,3 @@
+Line 1
+Line 2
+Line 3
"""
    result = parse_patch(new_file_patch)
    
    assert len(result["files"]) == 1
    assert result["files"][0]["is_added_file"] is True
    assert result["added"] == 3
    assert result["removed"] == 0
