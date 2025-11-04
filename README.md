# GitHub .patch Scraper — Python prototype

This prototype fetches GitHub `.patch` URLs, parses the unified diff, and stores the raw and parsed result in a local SQLite database.

Quick start

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Run the CLI to fetch a .patch URL:

```bash
python -m scraper.cli fetch https://github.com/python/cpython/pull/12345.patch
```

3. The SQLite DB `data/patches.db` will contain the raw patch and parsed JSON.

Run tests:

```bash
python -m pytest -q
```
