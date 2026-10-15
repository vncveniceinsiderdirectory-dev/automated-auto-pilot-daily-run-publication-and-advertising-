"""Daily run: publish one product to Shopify (draft) + Pinterest.

Usage:
  python src/daily_run.py --product products/example.json

The product JSON holds title, description, price, image_url, link.
Secrets come from environment variables (see .env.example).
Nothing is published live without review: Shopify products are created
as drafts, and the run prints the created IDs for a human to check.
"""
import argparse
import json

from pinterest_api import create_pin
from shopify_api import create_product


def main():
    parser = argparse.ArgumentParser(description="Venetian Threads daily publish run")
    parser.add_argument("--product", required=True, help="Path to product JSON file")
    parser.add_argument("--vendor", default="Venetian Threads")
    parser.add_argument("--product-type", default="Apparel")
    args = parser.parse_args()

    with open(args.product) as f:
        product = json.load(f)

    shopify_product = create_product(
        title=product["title"],
        body_html=product.get("description", ""),
        vendor=args.vendor,
        product_type=args.product_type,
        price=product["price"],
        tags=product.get("tags"),
    )
    print(f"Shopify draft created: id={shopify_product['id']} title={shopify_product['title']}")

    pin = create_pin(
        board_id=None,
        title=product["title"],
        description=product.get("description", ""),
        link=product.get("link", ""),
        media_source={"source_type": "image_url", "url": product["image_url"]},
    )
    print(f"Pinterest pin created: id={pin.get('id')}")


if __name__ == "__main__":
    main()
