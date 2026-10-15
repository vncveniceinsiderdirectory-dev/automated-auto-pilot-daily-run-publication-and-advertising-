"""Shopify Admin API client for the Venetian Threads auto-pilot.

Reads credentials from environment variables only -- never hardcode tokens:
  SHOPIFY_STORE_DOMAIN  e.g. venetian-threads.myshopify.com
  SHOPIFY_ACCESS_TOKEN  Admin API access token from a custom app
"""
import os

import requests

API_VERSION = "2025-07"
TIMEOUT = 30


def _session():
    domain = os.environ.get("SHOPIFY_STORE_DOMAIN")
    token = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    if not domain or not token:
        raise RuntimeError("Set SHOPIFY_STORE_DOMAIN and SHOPIFY_ACCESS_TOKEN")
    session = requests.Session()
    session.headers.update(
        {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json",
        }
    )
    return session, f"https://{domain}/admin/api/{API_VERSION}"


def create_product(title, body_html, vendor, product_type, price, tags=None):
    """Create a product in DRAFT status so a human reviews it before it goes live."""
    session, base = _session()
    payload = {
        "product": {
            "title": title,
            "body_html": body_html,
            "vendor": vendor,
            "product_type": product_type,
            "tags": ",".join(tags or []),
            "status": "draft",
            "variants": [{"price": price}],
        }
    }
    resp = session.post(f"{base}/products.json", json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["product"]


def get_product(product_id):
    session, base = _session()
    resp = session.get(f"{base}/products/{product_id}.json", timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()["product"]
