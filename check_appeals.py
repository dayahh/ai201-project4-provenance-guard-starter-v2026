#!/usr/bin/env python3
"""
Criterion 5 — the appeal path, three trials.

    python app.py                          # in one terminal
    python check_appeals.py --label before # in another

`run_eval.py` only sends text, and an appeal needs a content_id that a real
submission handed back. So each trial here submits five pieces, appeals every
one, checks the response says `under_review`, checks the audit log gained an
appeal entry for that id, and then appeals an id that doesn't exist (which
should be a 404).

Writes `results/appeals_<date>_<label>.md`.
"""

import argparse
import datetime as dt
import json

import requests

import config
from scenarios import MY_WRITING

DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"


def run_trial(url, trial):
    results = []
    for i, text in enumerate(MY_WRITING[:5], 1):
        submitted = requests.post(f"{url}/submit", timeout=90, json={
            "text": text, "creator_id": f"appeal_t{trial}_{i}"}).json()
        content_id = submitted["content_id"]
        response = requests.post(f"{url}/appeal", timeout=30, json={
            "content_id": content_id,
            "reasoning": "I wrote this myself for class."})
        body = response.json()
        log = requests.get(f"{url}/log", params={"limit": 50}, timeout=30).json()
        logged = any(e.get("content_id") == content_id and e.get("event") == "appeal"
                     for e in log["entries"])
        results.append({
            "content_id": content_id,
            "appeal_status_code": response.status_code,
            "status": body.get("status"),
            "appeal_in_log": logged,
            "passed": response.status_code == 200
                      and body.get("status") == "under_review" and logged,
        })

    bogus = requests.post(f"{url}/appeal", timeout=30, json={
        "content_id": "does-not-exist", "reasoning": "typo test"})
    results.append({
        "content_id": "does-not-exist",
        "appeal_status_code": bogus.status_code,
        "passed": bogus.status_code == 404,
    })
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    args = parser.parse_args()

    lines = [f"# Appeal check{f' — {args.label}' if args.label else ''}", "",
             "- Produced by: `check_appeals.py::main`",
             "- Service: `app.py::appeal`",
             f"- {args.trials} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for trial in range(1, args.trials + 1):
        results = run_trial(args.url, trial)
        passed = sum(r["passed"] for r in results)
        print(f"trial {trial}: {passed}/{len(results)} passed")
        lines += [f"**Trial {trial}: {passed}/{len(results)} passed**", "", "```json",
                  json.dumps(results, indent=2), "```", ""]

    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeals_{stamp}{label}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
