# API setup — Venetian Threads auto-pilot

The daily run publishes one product to Shopify (as a **draft**) and Pinterest.
All secrets come from environment variables. Nothing is hardcoded, and `.env`
is gitignored — never commit real tokens.

## 1. Install

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in real values
```

## 2. Shopify

1. In Shopify Admin, create a **custom app** (Settings → Apps and sales channels
   → Develop apps) with `write_products` / `read_products` access.
2. Install it on the store and copy the Admin API access token.
3. Set in `.env`:
   - `SHOPIFY_STORE_DOMAIN` — e.g. `venetian-threads.myshopify.com`
   - `SHOPIFY_ACCESS_TOKEN` — the token from step 2

Products are created as **drafts**, so a human reviews them before they go live.

## 3. Pinterest

1. Create a Pinterest developer app and complete OAuth with the `pins:write`
   scope to get an access token.
2. Set in `.env`:
   - `PINTEREST_ACCESS_TOKEN`
   - `PINTEREST_BOARD_ID` — the board pins go to

## 4. Run

```bash
python src/daily_run.py --product products/example.json
```

Replace `products/example.json` with real product data (title, description,
price, image URL, link) before a real run.

## 5. Bonfire

Bonfire does not offer a public API for creating campaigns, so Bonfire stays
a **manual step**: create the campaign on bonfire.com, then paste the campaign
URL into the product's `link` field so Shopify and Pinterest point at it.

## Safety

- Tokens live only in `.env`, never in code or git history.
- The Shopify client creates drafts only — nothing goes live automatically.
- Review the printed Shopify draft ID and Pinterest pin ID after every run.
