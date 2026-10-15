"""Pinterest API v5 client for the Venetian Threads auto-pilot.

Reads credentials from environment variables only:
  PINTEREST_ACCESS_TOKEN  OAuth access token with pins:write scope
  PINTEREST_BOARD_ID      Default board to pin to
"""
import os

import requests

BASE = "https://api.pinterest.com/v5"
TIMEOUT = 30


def _headers():
    token = os.environ.get("PINTEREST_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("Set PINTEREST_ACCESS_TOKEN")
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def create_pin(board_id, title, description, link, media_source):
    """Create a pin. media_source looks like {"source_type": "image_url", "url": ...}."""
    payload = {
        "board_id": board_id or os.environ.get("PINTEREST_BOARD_ID"),
        "title": title,
        "description": description,
        "link": link,
        "media_source": media_source,
    }
    resp = requests.post(f"{BASE}/pins", json=payload, headers=_headers(), timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()
