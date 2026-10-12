# HiveNexis social posts

Poster generator and image hosting for the HiveNexis Facebook Page.

- `make_poster.py` renders a 1080x1080 poster from a JSON spec: `python3 make_poster.py spec.json posts/2026-10-13-shopify.png`
- `posts/` holds the published poster images.
- `posted.md` is the log of what has been posted. `topics.md` is the idea backlog.

## Spec

```json
{"category": "shopify", "headline": "Turn Visitors|Into *Buyers*",
 "sub": "We build Shopify stores that are *designed to sell*, not just look good.",
 "bullets": ["High-converting product pages", "Fast, mobile-first design", "Checkout that closes the sale"],
 "product": "Your Product", "price": "$49.00", "badge": "Best Seller", "chip_label": "Orders", "chip_value": "+38%"}
```

```json
{"category": "seo", "headline": "Rank #1 on|*Google & AI*",
 "sub": "SEO that brings *buyers*, not just traffic.",
 "bullets": ["Keywords that drive sales", "Cited in AI search answers", "Clear monthly ranking reports"],
 "query": "best shopify agency near me", "keywords": ["kw one", "kw two", "kw three"], "score": "89"}
```

`|` breaks the headline into lines (2 lines, about 14 characters each, works best), `*...*` marks the purple words. Exactly 3 bullets, under 30 characters each. The script exits with an error if the text does not fit.
