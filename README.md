# Daily Engineering Log

Automated daily log tracking developments in identity resolution, privacy, advertising technology, and data platforms.

[![Daily Log](https://github.com/Shubham-Safaya/daily-engineering-log/actions/workflows/daily-log.yml/badge.svg)](https://github.com/Shubham-Safaya/daily-engineering-log/actions/workflows/daily-log.yml)

## What This Is

A GitHub Action that runs every morning and generates a structured markdown entry covering:

- **Today I Learned** -- rotating deep-dives into identity resolution, differential privacy, clean rooms, retail media measurement, and related topics
- **Industry News** -- relevant stories from Hacker News about privacy, identity, and advertising technology
- **Reading List** -- queued topics for deeper exploration

## The Identity Layer (weekly book in progress)

Every Monday a second workflow publishes one chapter of **[The Identity Layer](book/BOOK.md)**, a long-form essay series on how customer identity, advertising, and privacy actually fit together. Each chapter is written in a clean, book-ready voice (no em dashes) and lands in `book/published/` ready to paste into Medium, while `book/BOOK.md` assembles the whole manuscript in order. The goal is a published body of work that compounds week over week into an actual book.

```
book/
  manuscript/        # source chapters (NN-slug.md), published in order
  published/         # dated, Medium-ready copies
  BOOK.md            # the full manuscript, auto-assembled
publish_weekly_essay.py
```

## Why

Staying current in a fast-moving space (privacy regulation, cookie deprecation, clean room adoption, retail media growth) requires daily practice. This log creates a searchable, version-controlled knowledge base, and the weekly essay turns that practice into published thought leadership.

## Structure

```
logs/
  2026/
    2026-05-26.md
    2026-05-27.md
    ...
INDEX.md          # Chronological index of all entries
generate_log.py   # Log generation script
```

## Topics Covered

- Differential privacy (Laplace mechanism, epsilon budgets)
- Identity graph algorithms (connected components, blocking, partitioning)
- Privacy-preserving computation (k-anonymity, l-diversity, federated learning)
- String matching for entity resolution (Jaro-Winkler, edit distance, Soundex)
- Data clean room architectures (centralized, federated, cryptographic)
- Retail media measurement (incrementality, PSM, attribution)
- Consent management (IAB TCF, CMP implementation)
- Emerging identifiers (UID 2.0, Topics API, Protected Audience)

## Running Locally

```bash
python generate_log.py
```
