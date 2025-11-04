"""Simple SQLite storage for patches"""
import sqlite3
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class PatchStorage:
    """Store patches in SQLite database."""
    
    def __init__(self, db_path: str = "data/patches.db"):
        """Initialize storage, create tables if needed."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Create patches table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS patches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    raw_patch TEXT NOT NULL,
                    parsed_data TEXT,
                    parse_error TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_url ON patches(url)
            """)
            conn.commit()
    
    def save_patch(
        self,
        url: str,
        raw_patch: str,
        parsed_data: Optional[Dict[str, Any]] = None,
        parse_error: Optional[str] = None,
    ) -> int:
        """Save or update a patch.
        
        Args:
            url: The .patch URL
            raw_patch: Raw patch text
            parsed_data: Parsed patch structure (optional)
            parse_error: Parse error message if parsing failed (optional)
        
        Returns:
            The row id
        """
        now = datetime.utcnow().isoformat()
        parsed_json = json.dumps(parsed_data) if parsed_data else None
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                INSERT INTO patches (url, raw_patch, parsed_data, parse_error, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(url) DO UPDATE SET
                    raw_patch=excluded.raw_patch,
                    parsed_data=excluded.parsed_data,
                    parse_error=excluded.parse_error,
                    updated_at=excluded.updated_at
                """,
                (url, raw_patch, parsed_json, parse_error, now, now),
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_patch_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve a patch by URL."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM patches WHERE url = ?", (url,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
    
    def list_patches(self, limit: int = 100) -> list:
        """List recent patches."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT id, url, created_at, updated_at FROM patches ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]
