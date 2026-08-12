#!/usr/bin/env python3
"""Refresh the official documentation manifest from the pinned cf-docs navigation."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from portal.corpus import refresh_official_manifest


if __name__ == "__main__":
    count = refresh_official_manifest()
    print(f"indexed {count} official file-backed MDX navigation pages")
