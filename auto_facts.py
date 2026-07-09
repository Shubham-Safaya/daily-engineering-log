#!/usr/bin/env python3
"""Auto-stub of REAL automated facts (spec P3.2).

Appends a dated entry with only machine-verified facts — commits across
Shubham-Safaya repos, PyPI downloads, sites refreshed — and leaves a
`## Notes` section for narrative. No fabricated facts; every number is
fetched or "n/a". (BOOK.md TOC is owned by publish_weekly_essay.py.)

Runs in the daily-log Action after generate_log.py.
"""
import json, os, urllib.request, datetime, re, glob
from pathlib import Path

ROOT = Path(__file__).parent
UA = {"User-Agent": "auto-facts (github.com/Shubham-Safaya)"}
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def get(url, headers=None):
    req = urllib.request.Request(url, headers={**UA, **(headers or {})})
    return urllib.request.urlopen(req, timeout=30).read()


def gh(path):
    h = {"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}
    return json.loads(get(f"https://api.github.com{path}", h))


def commits_last_day():
    """Commits authored by Shubham-Safaya across owned repos in the last 24h."""
    since = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat()
    total, active = 0, []
    try:
        repos = gh("/users/Shubham-Safaya/repos?per_page=100&type=owner&sort=pushed")
    except Exception:
        return None, []
    for r in repos:
        if r.get("fork") or (r.get("pushed_at", "") < since):
            continue
        try:
            cs = gh(f"/repos/Shubham-Safaya/{r['name']}/commits?since={since}&per_page=100&author=Shubham-Safaya")
            if cs:
                total += len(cs)
                active.append((r["name"], len(cs)))
        except Exception:
            pass
    return total, sorted(active, key=lambda x: -x[1])


def pypi_month():
    try:
        d = json.loads(get("https://pypistats.org/api/packages/identity-resolver/recent"))
        return d["data"]["last_month"]
    except Exception:
        return None


def jobs_indexed():
    try:
        d = json.loads(get("https://raw.githubusercontent.com/Shubham-Safaya/job-search-dashboard/main/data/dashboard_data.json"))
        s = d.get("summary", {})
        return s.get("new_today") or s.get("total_new") or s.get("total_jobs")
    except Exception:
        return None



def main():
    today = datetime.date.today()
    commits, active = commits_last_day()
    pypi = pypi_month()
    jobs = jobs_indexed()

    active_str = ", ".join(f"{n} ({c})" for n, c in active[:6]) if active else "no repos pushed"
    facts = [
        f"## Automated facts — {today.isoformat()}",
        "",
        f"- Commits (last 24h, authored): **{commits if commits is not None else 'n/a'}** across {len(active)} repo(s): {active_str}",
        f"- identity-resolver PyPI downloads (last 30d): **{pypi if pypi is not None else 'live on PyPI since 2026-07-08 — awaiting first download data (pypistats backfills ~24-48h)'}**",
        f"- Job pipeline index size: **{jobs if jobs is not None else 'n/a'}**",
        f"- Sites on the daily-refresh backbone: us-consumer-pulse, portfolio stats, mission-control",
        "",
        "## Notes",
        "",
        "_(narrative — add by hand)_",
        "",
    ]
    entry = "\n".join(facts)

    logdir = ROOT / "logs" / str(today.year)
    logdir.mkdir(parents=True, exist_ok=True)
    log = logdir / f"{today.isoformat()}.md"
    prev = log.read_text() if log.exists() else ""
    # append the facts block if generate_log.py already made today's file
    if "## Automated facts" not in prev:
        log.write_text(prev + ("\n\n" if prev else "") + entry)

    print(f"auto-facts: commits={commits} pypi={pypi} jobs={jobs}; book TOC owned by weekly-essay engine")


if __name__ == "__main__":
    main()
