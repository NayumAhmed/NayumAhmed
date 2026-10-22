#!/usr/bin/env python3
"""Discover and conservatively fork quality open-source repositories for NayumAhmed.
Never clones or executes candidate code. Requires GITHUB_TOKEN environment variable.
"""
import json, os, sys, time
from datetime import datetime, timedelta, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://api.github.com"
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OWNER = os.environ.get("GITHUB_OWNER", "NayumAhmed")
LIMIT = int(os.environ.get("WEEKLY_FORK_LIMIT", "10"))
MIN_STARS = int(os.environ.get("MIN_STARS", "100"))
MAX_AGE = int(os.environ.get("MAX_PUSH_AGE_DAYS", "180"))
DRY_RUN = os.environ.get("DRY_RUN", "true").lower() != "false"
TOPICS = ["ai-tools", "browser-games", "developer-tools", "android-tv", "google-tv", "ai-agents", "web-apps"]
DENY_LICENSES = {"NOASSERTION", "OTHER", ""}
HEADERS = {"Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28", "User-Agent":"NayumAhmed-RepoDiscovery"}
if TOKEN:
    HEADERS["Authorization"] = "Bearer " + TOKEN

def api(path, params=None, method="GET", payload=None):
    url = API + path + (("?" + urlencode(params)) if params else "")
    body = json.dumps(payload).encode() if payload is not None else None
    headers = dict(HEADERS)
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(req, timeout=25) as response:
            raw = response.read()
            return response.status, json.loads(raw.decode()) if raw else {}
    except HTTPError as error:
        try:
            data = json.loads(error.read().decode(errors="replace"))
        except Exception:
            data = {"message":"HTTP error"}
        return error.code, data
    except (URLError, TimeoutError) as error:
        return 0, {"message":str(error)}

def get(path, params=None):
    status, data = api(path, params)
    return data if status == 200 else {}

def main():
    if not TOKEN:
        print("ERROR: Set GITHUB_TOKEN as a GitHub Actions secret; never paste it into chat.")
        sys.exit(2)
    own = get("/users/" + OWNER + "/repos", {"per_page":100,"type":"owner","sort":"updated"})
    existing = {r.get("full_name","").lower() for r in own if isinstance(r,dict)}
    existing_names = {r.get("name","").lower() for r in own if isinstance(r,dict)}
    candidates = {}
    for topic in TOPICS:
        data = get("/search/repositories", {"q":f"topic:{topic} stars:>={MIN_STARS} archived:false fork:false","sort":"updated","order":"desc","per_page":30})
        for repo in data.get("items",[]):
            full = repo.get("full_name","").lower()
            if full and full not in existing:
                candidates[full] = repo
        time.sleep(0.25)
    # Enforce a rolling seven-day cap using committed reports from previous runs.
    os.makedirs("reports", exist_ok=True)
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    prior_requests = 0
    for filename in os.listdir("reports"):
        if not filename.endswith(".json"):
            continue
        try:
            with open(os.path.join("reports", filename), encoding="utf-8") as previous_file:
                previous = json.load(previous_file)
            generated = datetime.fromisoformat(previous.get("generated_at_utc", "").replace("Z", "+00:00"))
            if generated >= cutoff:
                prior_requests += int(previous.get("fork_requests_accepted", 0))
        except Exception:
            continue
    remaining = max(0, LIMIT - prior_requests)
    ranked = sorted(candidates.values(), key=lambda r:(r.get("stargazers_count",0),r.get("updated_at","")), reverse=True)
    report, requested = [], 0
    for repo in ranked:
        source_owner = repo.get("owner",{}).get("login","")
        name = repo.get("name","")
        full = repo.get("full_name","")
        if not source_owner or not name:
            continue
        readme_status, readme = api(f"/repos/{source_owner}/{name}/readme")
        lic = ((repo.get("license") or {}).get("spdx_id") or "NOASSERTION").upper()
        reasons = []
        if source_owner.lower() == OWNER.lower(): reasons.append("already owned")
        if name.lower() in existing_names: reasons.append("repository name already exists in account; avoid duplicate fork")
        if repo.get("fork"): reasons.append("candidate is itself a fork")
        if repo.get("archived") or repo.get("disabled"): reasons.append("archived or disabled")
        if lic in DENY_LICENSES: reasons.append("no clear SPDX open-source licence")
        if repo.get("stargazers_count",0) < MIN_STARS: reasons.append("below star threshold")
        if len((repo.get("description") or "").strip()) < 12: reasons.append("description missing")
        try:
            pushed = datetime.fromisoformat(repo["pushed_at"].replace("Z","+00:00"))
            if pushed < datetime.now(timezone.utc)-timedelta(days=MAX_AGE): reasons.append("not updated in 180 days")
        except Exception: reasons.append("invalid push timestamp")
        if readme_status != 200: reasons.append("README not found")
        item = {"repository":full,"url":repo.get("html_url"),"stars":repo.get("stargazers_count",0),"license":lic,"pushed_at":repo.get("pushed_at"),"decision":"rejected" if reasons else ("dry-run candidate" if DRY_RUN else "pending fork"),"reasons":reasons}
        if not reasons and not DRY_RUN:
            if requested >= remaining:
                item["decision"] = "eligible but weekly fork allowance exhausted"
            else:
                status, result = api(f"/repos/{source_owner}/{name}/forks", method="POST", payload={})
                if status in (202,200):
                    requested += 1
                    item["decision"] = "fork request accepted (verify after GitHub processes it)"
                    item["expected_fork_url"] = f"https://github.com/{OWNER}/{name}"
                elif status == 422 and "already exists" in str(result).lower():
                    item["decision"] = "skipped: fork already exists"
                else:
                    item["decision"] = f"fork failed HTTP {status}"
                    item["error"] = result.get("message","unknown error")
                time.sleep(1)
        report.append(item)
    os.makedirs("reports",exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")
    with open(f"reports/discovery-{stamp}.json","w",encoding="utf-8") as f:
        json.dump({"generated_at_utc":datetime.now(timezone.utc).isoformat(),"owner":OWNER,"dry_run":DRY_RUN,"weekly_fork_limit":LIMIT,"prior_requests_in_rolling_week":prior_requests,"remaining_allowance_at_start":remaining,"fork_requests_accepted":requested,"topics":TOPICS,"minimum_stars":MIN_STARS,"max_push_age_days":MAX_AGE,"results":report,"warning":"Metadata screening is not a security audit. Never run candidate code without independent review."},f,indent=2)
    print(f"Reviewed {len(report)} candidates; accepted fork requests: {requested}; dry run: {DRY_RUN}")

if __name__ == "__main__":
    main()
