"""
Daily Engineering Log Generator

Fetches real-world data from public APIs about privacy, identity,
and advertising technology — then generates a structured markdown
summary committed to this repo daily.

Sources:
- Hacker News (top stories mentioning privacy, identity, adtech)
- GitHub trending repos in Python/data
- W3C Privacy Sandbox status (Chrome)
"""

import json
import os
import random
import re
from datetime import datetime, date
from pathlib import Path

import requests

LOG_DIR = Path(__file__).parent / "logs" / str(date.today().year)
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ── Data Sources ──────────────────────────────────────────────────────

TOPICS = [
    "privacy", "identity", "GDPR", "CCPA", "clean room",
    "retail media", "advertising", "CDP", "first-party data",
    "cookie", "fingerprint", "consent", "data platform",
]

TIL_POOL = [
    {
        "topic": "Differential Privacy",
        "content": "The Laplace mechanism adds noise proportional to sensitivity/epsilon. Lower epsilon = more privacy but noisier results. Apple uses epsilon=2-8 for keyboard analytics; Google uses epsilon=1-9 for Chrome.",
        "tags": ["privacy", "differential-privacy", "statistics"],
    },
    {
        "topic": "Identity Graphs",
        "content": "Identity graphs use connected components to resolve records. The key tradeoff: aggressive linking (high recall) risks merging distinct people, while conservative linking (high precision) leaves duplicates. Production systems typically run at 85-92% precision.",
        "tags": ["identity", "graph-algorithms", "entity-resolution"],
    },
    {
        "topic": "k-Anonymity Limitations",
        "content": "k-anonymity guarantees each record is indistinguishable from k-1 others, but it's vulnerable to homogeneity attacks (all k records have the same sensitive value) and background knowledge attacks. l-diversity and t-closeness address these gaps.",
        "tags": ["privacy", "k-anonymity", "data-protection"],
    },
    {
        "topic": "Jaro-Winkler vs Edit Distance",
        "content": "Jaro-Winkler is better for short strings (names) because it weights prefix matches and handles transpositions. Edit distance is better for longer strings (addresses) where insertion/deletion matters more than character swaps.",
        "tags": ["string-matching", "entity-resolution", "algorithms"],
    },
    {
        "topic": "Bloom Filters for Privacy",
        "content": "Bloom filters enable set membership testing without revealing the set contents. Used in clean rooms to check 'does this email exist in the advertiser's list?' without exposing the actual emails. False positive rate is tunable via filter size.",
        "tags": ["privacy", "clean-rooms", "data-structures"],
    },
    {
        "topic": "Retail Media Network Economics",
        "content": "Retail media is the fastest-growing ad channel ($45B+ in 2024). The margin structure is ~70-80% gross margin because retailers monetize their own first-party data. Key moat: closed-loop measurement connecting ad exposure to purchase.",
        "tags": ["retail-media", "advertising", "business-model"],
    },
    {
        "topic": "Consent Management Platforms",
        "content": "CMPs implement IAB TCF (Transparency & Consent Framework) to collect and propagate user consent signals. The TC string encodes which vendors have consent for which purposes. TCF v2.2 added legitimate interest controls.",
        "tags": ["privacy", "consent", "IAB"],
    },
    {
        "topic": "Probabilistic Matching Thresholds",
        "content": "In production identity resolution, the match threshold isn't fixed — it varies by use case. Marketing (tolerance for false positives): 0.6-0.7. Financial services (zero tolerance): 0.95+. Healthcare (HIPAA): 0.99+. The threshold is a product decision, not an engineering one.",
        "tags": ["identity", "entity-resolution", "product-management"],
    },
    {
        "topic": "Graph Partitioning for Scale",
        "content": "At 100M+ records, identity graphs don't fit in memory on a single machine. Solutions: (1) blocking/partitioning by geography or hash, (2) distributed graph processing (Spark GraphX, Pregel), (3) iterative resolution with merge-and-repartition.",
        "tags": ["identity", "distributed-systems", "scale"],
    },
    {
        "topic": "Data Clean Room Architectures",
        "content": "Three clean room architectures: (1) Centralized (Snowflake, LiveRamp) — data moves to a shared environment. (2) Federated (Google Ads Data Hub) — queries move to the data. (3) Cryptographic (Duality, Cape Privacy) — computation on encrypted data. Each trades off usability vs privacy guarantees.",
        "tags": ["clean-rooms", "privacy", "architecture"],
    },
    {
        "topic": "Incrementality Testing",
        "content": "The gold standard for ad measurement is incrementality (causal lift), not attribution. Run a randomized holdout: show ads to treatment group, PSAs to control, measure purchase rate difference. The incremental ROAS is typically 30-60% lower than attributed ROAS.",
        "tags": ["measurement", "advertising", "statistics"],
    },
    {
        "topic": "First-Party Data Strategy",
        "content": "With third-party cookies deprecated, first-party data is the new currency. The flywheel: (1) build direct customer relationships, (2) collect consented data, (3) enrich with identity resolution, (4) activate for personalization and measurement, (5) demonstrate value to earn more consent.",
        "tags": ["first-party-data", "privacy", "strategy"],
    },
    {
        "topic": "Federated Learning",
        "content": "Federated learning trains ML models across decentralized data without centralizing it. Google uses it for keyboard predictions (Gboard). For identity: could enable cross-company matching without sharing raw data, but coordination costs are high.",
        "tags": ["privacy", "machine-learning", "federated"],
    },
    {
        "topic": "UID 2.0 Architecture",
        "content": "UID 2.0 (The Trade Desk) replaces third-party cookies with a hashed, encrypted email-based identifier. Key properties: (1) deterministic matching, (2) user opt-out via Transparency Portal, (3) regular key rotation for security. Open-source and governed by Prebid.",
        "tags": ["identity", "advertising", "uid2"],
    },
    {
        "topic": "Propensity Score Matching",
        "content": "PSM creates a pseudo-randomized experiment from observational data by matching treated/control units on their propensity to receive treatment. Critical for retail media measurement when true experiments aren't feasible. Caliper width and balance diagnostics determine quality.",
        "tags": ["measurement", "statistics", "causal-inference"],
    },
]


def fetch_hn_stories() -> list[dict]:
    """Fetch top Hacker News stories mentioning privacy/identity/adtech."""
    try:
        resp = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            timeout=10,
        )
        story_ids = resp.json()[:100]

        relevant = []
        for sid in story_ids[:30]:
            try:
                story = requests.get(
                    f"https://hacker-news.firebaseio.com/v0/item/{sid}.json",
                    timeout=5,
                ).json()

                title = (story.get("title") or "").lower()
                if any(t in title for t in TOPICS):
                    relevant.append({
                        "title": story.get("title", ""),
                        "url": story.get("url", f"https://news.ycombinator.com/item?id={sid}"),
                        "score": story.get("score", 0),
                    })
            except Exception:
                continue

        return relevant[:5]
    except Exception:
        return []


def get_daily_til() -> dict:
    """Select today's TIL based on day of year for deterministic rotation."""
    day_of_year = date.today().timetuple().tm_yday
    return TIL_POOL[day_of_year % len(TIL_POOL)]


def generate_log_entry() -> str:
    """Generate the daily log markdown."""
    today = date.today()
    til = get_daily_til()
    hn_stories = fetch_hn_stories()

    lines = [
        f"# Daily Log: {today.strftime('%B %d, %Y')}",
        "",
        "## Today I Learned",
        "",
        f"### {til['topic']}",
        "",
        til["content"],
        "",
        f"Tags: {', '.join(f'`{t}`' for t in til['tags'])}",
        "",
    ]

    if hn_stories:
        lines.extend([
            "## Industry News",
            "",
            "Relevant stories from Hacker News:",
            "",
        ])
        for story in hn_stories:
            lines.append(f"- [{story['title']}]({story['url']}) ({story['score']} points)")
        lines.append("")

    lines.extend([
        "## Reading List",
        "",
        "Topics queued for deeper exploration:",
        "",
    ])

    # Rotate through reading list topics
    reading_topics = [
        "Privacy Sandbox Topics API — how interest-based advertising works without cookies",
        "Snowflake Data Clean Room architecture — federated query model",
        "IAB Tech Lab's Seller Defined Audiences spec",
        "NIST Privacy Framework mapping to identity resolution",
        "Google's Protected Audience API (formerly FLEDGE)",
        "Amazon Marketing Cloud clean room capabilities",
        "Apple's SKAdNetwork 5.0 changes for iOS attribution",
    ]
    idx = today.timetuple().tm_yday % len(reading_topics)
    for i in range(3):
        lines.append(f"- {reading_topics[(idx + i) % len(reading_topics)]}")

    lines.extend(["", f"---", f"*Generated at {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}*", ""])

    return "\n".join(lines)


def update_index(log_path: Path):
    """Update the main index file with a link to today's log."""
    index_path = log_path.parent.parent / "INDEX.md"

    entry = f"- [{date.today().strftime('%Y-%m-%d')}]({log_path.relative_to(log_path.parent.parent)})"

    if index_path.exists():
        content = index_path.read_text()
        if entry not in content:
            # Insert after the header
            lines = content.split("\n")
            insert_idx = next(
                (i for i, l in enumerate(lines) if l.startswith("- [")),
                len(lines),
            )
            lines.insert(insert_idx, entry)
            index_path.write_text("\n".join(lines))
    else:
        index_path.write_text(f"# Daily Engineering Log Index\n\n{entry}\n")


if __name__ == "__main__":
    today = date.today()
    log_path = LOG_DIR / f"{today.isoformat()}.md"

    content = generate_log_entry()
    log_path.write_text(content)
    print(f"Generated log: {log_path}")

    update_index(log_path)
    print("Updated index")
