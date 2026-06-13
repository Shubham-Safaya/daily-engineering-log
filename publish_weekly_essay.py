"""
Weekly Essay Publisher — "The Identity Layer" (book in progress)

Each week this picks the next unpublished chapter from book/manuscript/,
stamps it with a date and a Medium-ready header, drops it into
book/published/, and rebuilds book/BOOK.md (the full manuscript in order).

Design goals:
- No runtime API key needed. Chapters are real, pre-written, book-quality.
- No em dashes anywhere (enforced programmatically before writing).
- Deterministic order: chapters are numbered NN-slug.md and published in order.
- The assembled BOOK.md is the EB1A "book / sustained body of work" artifact.

Each published file is ready to paste straight into Medium.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent
MANUSCRIPT = ROOT / "book" / "manuscript"
PUBLISHED = ROOT / "book" / "published"
BOOK = ROOT / "book" / "BOOK.md"
PUBLISHED.mkdir(parents=True, exist_ok=True)

# Em dash and en dash are banned in the published voice. Replace with clean ASCII.
BANNED = {
    "—": ", ",   # em dash -> comma+space (then we tidy doubles)
    "–": "-",     # en dash -> hyphen
    "‒": "-",
    "―": "-",
}


def strip_dashes(text: str) -> str:
    for bad, good in BANNED.items():
        text = text.replace(bad, good)
    # tidy accidental ", ," or " ,"
    text = text.replace(" , ", ", ").replace(",  ", ", ").replace(" ,", ",")
    return text


def chapters() -> list[Path]:
    return sorted(MANUSCRIPT.glob("[0-9][0-9]-*.md"))


def already_published_stems() -> set[str]:
    out = set()
    for p in PUBLISHED.glob("*.md"):
        # published name: YYYY-MM-DD__NN-slug.md
        stem = p.stem.split("__", 1)[-1]
        out.add(stem)
    return out


def next_chapter() -> Path | None:
    done = already_published_stems()
    for ch in chapters():
        if ch.stem not in done:
            return ch
    return None


def publish(ch: Path) -> Path:
    raw = strip_dashes(ch.read_text())
    today = date.today().isoformat()

    # The first markdown H1 is the title; keep the body, prepend a Medium header.
    lines = raw.splitlines()
    title = next((l[2:].strip() for l in lines if l.startswith("# ")), ch.stem)

    header = (
        f"<!-- Ready for Medium. Published {today}. "
        f"Part of 'The Identity Layer' by Shubham Safaya. No em dashes. -->\n\n"
    )
    body = strip_dashes(raw)
    out_text = header + body + (
        "\n\n---\n\n"
        "*This essay is part of an ongoing series, "
        "[The Identity Layer](https://github.com/Shubham-Safaya/daily-engineering-log/tree/main/book), "
        "where I work out in public how customer identity, advertising, and privacy fit together. "
        "I am a Senior Product Manager at Walmart Global Tech. "
        "Follow on [LinkedIn](https://www.linkedin.com/in/shubham-safaya/).*\n"
    )

    out_path = PUBLISHED / f"{today}__{ch.stem}.md"
    out_path.write_text(out_text)
    print(f"Published: {out_path.name}  ('{title}')")
    return out_path


def rebuild_book():
    parts = [
        "# The Identity Layer",
        "### How customer identity, advertising, and privacy actually fit together",
        "",
        "*A book assembling itself in public, one weekly essay at a time, by Shubham Safaya.*",
        "",
        f"*Manuscript regenerated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}.*",
        "",
        "---",
        "",
        "## Table of contents",
        "",
    ]
    chs = chapters()
    for i, ch in enumerate(chs, 1):
        title = next((l[2:].strip() for l in ch.read_text().splitlines() if l.startswith("# ")), ch.stem)
        title = strip_dashes(title)
        parts.append(f"{i}. {title}")
    parts.append("\n---\n")

    for i, ch in enumerate(chs, 1):
        body = strip_dashes(ch.read_text()).strip()
        # demote chapter H1 to H2 so the book has one H1
        body = body.replace("# ", "## ", 1) if body.startswith("# ") else body
        parts.append(f"\n## Chapter {i}\n\n{body}\n\n---\n")

    BOOK.write_text("\n".join(parts))
    print(f"Rebuilt BOOK.md ({len(chs)} chapters)")


def update_index(published_path: Path):
    idx = ROOT / "book" / "PUBLISHED_INDEX.md"
    entry = f"- {date.today().isoformat()} — `{published_path.name}`"
    if idx.exists():
        content = idx.read_text()
        if entry not in content:
            idx.write_text(content.rstrip() + "\n" + entry + "\n")
    else:
        idx.write_text("# Published Essays (Medium-ready)\n\n" + entry + "\n")


if __name__ == "__main__":
    ch = next_chapter()
    if ch is None:
        print("All chapters published. Add more files to book/manuscript/ to continue.")
        rebuild_book()
    else:
        out = publish(ch)
        update_index(out)
        rebuild_book()
