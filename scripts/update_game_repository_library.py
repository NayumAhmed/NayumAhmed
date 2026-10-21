#!/usr/bin/env python3
"""Refresh the game-port library in NayumAhmed/arcade-orbit47 using GitHub metadata only.

This records source repositories and project pages, never game binaries or copyrighted assets.
"""
import base64
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = os.environ.get("GITHUB_OWNER", "NayumAhmed")
TARGET_REPO = os.environ.get("GAME_LIBRARY_REPO", f"{OWNER}/arcade-orbit47")
TARGET_PATH = os.environ.get("GAME_LIBRARY_PATH", "repositories/README.md")
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "NayumAhmed-Game-Port-Library",
}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN

SEARCHES = [
    ('"source port" game', "Source ports"),
    ('game recompilation OR decompilation', "Recompilations / decompilations"),
    ('game engine recreation open source', "Engine reimplementations"),
    ('open source game remake', "Remakes / reimplementations"),
    ('God of War III PC port', "Community ports"),
]
MIN_STARS = int(os.environ.get("GAME_LIBRARY_MIN_STARS", "5"))
MAX_RESULTS_PER_QUERY = 15

def request(method, url, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    headers = dict(HEADERS)
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=30) as response:
            raw = response.read()
            return response.status, json.loads(raw.decode()) if raw else {}
    except HTTPError as error:
        body = error.read().decode(errors="replace")
        return error.code, {"message": body[:500]}
    except (URLError, TimeoutError) as error:
        return 0, {"message": str(error)}

def api_get(path, params=None):
    url = API + path + (("?" + urlencode(params)) if params else "")
    return request("GET", url)

def clean(value):
    return str(value or "").replace("|", "\\|").replace("\r", " ").replace("\n", " ").strip()

def main():
    if not TOKEN:
        print("ERROR: GITHUB_TOKEN is required.")
        return 2

    found = {}
    for query, category in SEARCHES:
        status, data = api_get("/search/repositories", {
            "q": query + " stars:>=" + str(MIN_STARS) + " archived:false fork:false",
            "sort": "updated", "order": "desc", "per_page": MAX_RESULTS_PER_QUERY,
        })
        if status != 200:
            print(f"WARNING: search failed for {query!r}: HTTP {status}; {data.get('message', '')}")
            continue
        for repo in data.get("items", []):
            full = (repo.get("full_name") or "").lower()
            description = (repo.get("description") or "").strip()
            if not full or not description or repo.get("archived") or repo.get("disabled"):
                continue
            if repo.get("owner", {}).get("login", "").lower() == OWNER.lower():
                continue
            # Skip obvious ROM/ISO distribution repositories; do not index piracy-focused projects.
            haystack = (full + " " + description).lower()
            if any(term in haystack for term in ("rom download", "iso download", "pirated games", "full game download", "cracked game")):
                continue
            found[full] = {
                "name": repo.get("full_name", full),
                "url": repo.get("html_url", ""),
                "description": description,
                "stars": int(repo.get("stargazers_count") or 0),
                "license": (repo.get("license") or {}).get("spdx_id") or "Not specified",
                "updated": (repo.get("pushed_at") or "")[:10] or "Unknown",
                "category": category,
                "archived": bool(repo.get("archived")),
            }

    # Prioritize most recently maintained and popular projects; stable URLs prevent duplicate entries.
    entries = sorted(found.values(), key=lambda r: (r["updated"], r["stars"]), reverse=True)
    status, current = api_get(f"/repos/{TARGET_REPO}/contents/{TARGET_PATH}")
    if status != 200:
        print(f"ERROR: Cannot read {TARGET_REPO}/{TARGET_PATH}: HTTP {status}; {current.get('message', '')}")
        return 1
    sha = current.get("sha")
    try:
        content = base64.b64decode(current.get("content", "")).decode("utf-8")
    except Exception:
        print("ERROR: Could not decode current game library README.")
        return 1

    start_marker = "<!-- AUTO_DISCOVERED_GAME_PROJECTS_START -->"
    end_marker = "<!-- AUTO_DISCOVERED_GAME_PROJECTS_END -->"
    generated = [
        start_marker,
        "## 🔎 Automatically discovered game-port projects",
        "",
        f"> Refreshed by the Repository Discovery workflow on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}. These are repository leads, not endorsements or verified playable builds.",
        "",
        "| Project | Description | Stars | Licence | Last pushed |",
        "|---|---|---:|---|---|",
    ]
    if entries:
        for item in entries[:60]:
            generated.append(
                f"| [{clean(item['name'])}]({item['url']}) | {clean(item['description'])} "
                f"| {item['stars']} | {clean(item['license'])} | {clean(item['updated'])} |"
            )
    else:
        generated.append("| No new candidates passed the metadata filters in this run. | — | — | — | — |")
    generated += [
        "",
        "Only source repositories and project pages are indexed here. No ROMs, ISOs, BIOS files, copyrighted assets, cracked binaries, or unauthorized game downloads are hosted or linked. Review licences, release notes, dependencies, and safety before use.",
        end_marker,
    ]
    section = "\n".join(generated)
    if start_marker in content and end_marker in content:
        before, tail = content.split(start_marker, 1)
        _, after = tail.split(end_marker, 1)
        updated_content = before.rstrip() + "\n\n" + section + "\n" + after.lstrip("\n")
    else:
        updated_content = content.rstrip() + "\n\n" + section + "\n"

    if updated_content == content:
        print(f"Game library already current; {len(entries)} candidate projects checked.")
        return 0

    payload = {
        "message": "Refresh automatically discovered game-port library",
        "content": base64.b64encode(updated_content.encode()).decode(),
        "sha": sha,
        "branch": "main",
    }
    put_status, result = request("PUT", f"{API}/repos/{TARGET_REPO}/contents/{TARGET_PATH}", payload)
    if put_status not in (200, 201):
        print(f"ERROR: Could not update game library (HTTP {put_status}): {result.get('message', '')}")
        print("Check that FORK_AUTOMATION_TOKEN has Contents: Read and write access to the game repository.")
        return 1
    print(f"Updated {TARGET_REPO}/{TARGET_PATH} with {min(len(entries), 60)} discovered project links.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
