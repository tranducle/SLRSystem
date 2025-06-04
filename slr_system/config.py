"""Configuration helpers."""

import os

DB_URL = os.environ.get("SLR_DB_URL", "sqlite:///slr.db")
