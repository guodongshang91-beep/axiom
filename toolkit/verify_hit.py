#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_hit.py - put a scan hit through the five false-positive guards.

A "200" is not a finding. This compares a candidate response against a
random-path baseline, then applies the guards from docs/verification.md.
It prints a verdict; it never claims a vulnerability.

Usage:
    python toolkit/verify_hit.py --baseline base.json --candidate hit.json
    python toolkit/verify_hit.py --baseline base.json --candidate hit.json \
        --pattern 'org\\.h2\\.server\\.web' --echo-token my-marker
    python toolkit/verify_hit.py --self-test

Input files are small JSON objects:
    {"status": 200, "headers": {"content-type": "text/html"},
     "body": "...", "url": "https://example.invalid/random"}

Output (stdout): one JSON object
    {"verdict": "candidate" | "rejected", "checks": [...], "reasons": [...],
     "body_md5": "...", "baseline_md5": "..."}

Exit codes: 0 = verdict produced, 2 = bad arguments / unreadable input.
"""
import argparse
import hashlib
import json
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

WAF_MARKERS = (
    "request blocked", "security check", "access denied by", "waf",
    "captcha", "verify you are human", "拦截", "防火墙",
)


def md5(text):
    return hashlib.md5(text.encode("utf-8", "replace")).hexdigest()


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    return {
        "status": int(d.get("status", 0)),
        "headers": d.get("headers") or {},
        "body": str(d.get("body") or ""),
        "url": str(d.get("url") or ""),
    }


def judge(base, cand, pattern=None, echo_token=None):
    checks, reasons = [], []

    b_md5, c_md5 = md5(base["body"]), md5(cand["body"])

    # Guard 1: random-path baseline / soft-404.
    same = (base["status"] == cand["status"] and b_md5 == c_md5)
    checks.append({"guard": "random-path-baseline", "passed": not same})
    if same:
        reasons.append("identical to random-path baseline (catch-all or soft-404)")

    # Guard 2: component-specific signature.
    if pattern:
        matched = re.search(pattern, cand["body"], re.I) is not None
        checks.append({"guard": "tight-signature", "passed": matched})
        if not matched:
            reasons.append("component-specific pattern not present in body")
    else:
        checks.append({"guard": "tight-signature", "passed": None,
                       "note": "no --pattern supplied; run with one before reporting"})

    # Guard 3: duplicate fingerprint.
    dup = b_md5 == c_md5
    checks.append({"guard": "dedupe", "passed": not dup})
    if dup:
        reasons.append("same body fingerprint as baseline; counted once")

    # Guard 4: WAF / interception page.
    low = cand["body"].lower()
    blocked = any(m in low for m in WAF_MARKERS)
    checks.append({"guard": "waf-block", "passed": not blocked})
    if blocked:
        reasons.append("WAF or interception page markers (WAF_BLOCK)")

    # Guard 5: request echo / reflection.
    echoed = bool(echo_token and echo_token in cand["body"])
    checks.append({"guard": "err-echo", "passed": not echoed})
    if echoed:
        reasons.append("request token reflected verbatim (ERR_ECHO), not execution")

    hard_fail = same or blocked or echoed or dup or (pattern and not any(
        c["guard"] == "tight-signature" and c["passed"] for c in checks))
    return {
        "verdict": "rejected" if hard_fail else "candidate",
        "checks": checks,
        "reasons": reasons,
        "body_md5": c_md5,
        "baseline_md5": b_md5,
        "note": "candidate only; reproduce twice and store the raw response",
    }


def self_test():
    base = {"status": 200, "headers": {}, "body": "<html>SPA home</html>", "url": "https://example.invalid/rand"}
    spa = dict(base, url="https://example.invalid/admin")
    real = {"status": 200, "headers": {}, "body": "H2 Console org.h2.server.web", "url": "https://example.invalid/h2"}
    waf = {"status": 200, "headers": {}, "body": "Request blocked by WAF", "url": "https://example.invalid/.env"}

    r1 = judge(base, spa)
    r2 = judge(base, real, pattern=r"org\.h2\.server\.web")
    r3 = judge(base, waf)
    r4 = judge(base, dict(real, body=real["body"] + " my-marker"),
               pattern=r"org\.h2\.server\.web", echo_token="my-marker")
    expected = ["rejected", "candidate", "rejected", "rejected"]
    got = [r1["verdict"], r2["verdict"], r3["verdict"], r4["verdict"]]
    print(json.dumps({"expected": expected, "got": got, "pass": expected == got},
                     ensure_ascii=False, indent=2))
    return 0 if expected == got else 1


def main():
    ap = argparse.ArgumentParser(description="False-positive guard for a scan hit")
    ap.add_argument("--baseline", help="JSON file with a random-path response")
    ap.add_argument("--candidate", help="JSON file with the hit response")
    ap.add_argument("--pattern", help="component-specific regex; generic words will mislead")
    ap.add_argument("--echo-token", help="string injected in the request, to detect reflection")
    ap.add_argument("--self-test", action="store_true", help="run built-in cases")
    a = ap.parse_args()

    if a.self_test:
        return self_test()
    if not (a.baseline and a.candidate):
        ap.print_help()
        return 2
    try:
        base, cand = load(a.baseline), load(a.candidate)
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print("input error: %s" % e, file=sys.stderr)
        return 2
    print(json.dumps(judge(base, cand, a.pattern, a.echo_token),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
