#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Strata self-check. CI runs this exact file.

    python check.py            # compile + CLI smoke + asset/secret guard
    python check.py --quick    # compile + guard only

Blocks on: syntax errors, a CLI tool whose -h fails, or any real vendor
domain / private address / credential left in the tree. Exit 0 means green.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):   # Windows consoles default to cp1252
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
CODE_DIRS = ["targets", "toolkit"]

VENDOR = re.compile(
    r"\b[a-z0-9][a-z0-9-]*\.(?:163|126|netease|jd|baidu|bytedance|toutiao|douyin|"
    r"kuaishou|meituan|sina|weibo|pinduoduo|ctrip|qunar|didiglobal|360|so|qihoo|"
    r"xiaomi|mi|huawei|alipay|taobao|tmall|youku|iqiyi|bilibili|zhihu|91)\.(?:com|cn|net)\b",
    re.I,
)
PRIVATE_IP = re.compile(r"\b(?:10\.\d{1,3}|192\.168|172\.(?:1[6-9]|2\d|3[01]))\.\d{1,3}\.\d{1,3}\b")
SECRET = re.compile(r"\b(?:LTAI[0-9A-Za-z]{12,}|AKIA[0-9A-Z]{16}|ghp_[0-9A-Za-z]{30,}|github_pat_[0-9A-Za-z_]{30,})\b")
SKIP_EXT = {".svg", ".png", ".jpg", ".jpeg", ".ico", ".zip", ".pcap", ".mp4", ".pyc"}
SKIP_DIR = {".git", "__pycache__", ".venv", "venv", "out", "evidence"}


def sh(args, cwd=ROOT):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def py_scripts():
    out = []
    for base in CODE_DIRS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, base)):
            dn[:] = [d for d in dn if d not in SKIP_DIR]
            for f in fn:
                if f.endswith(".py"):
                    out.append(os.path.relpath(os.path.join(dp, f), ROOT))
    return sorted(out)


def step_compile():
    print("[1/3] compileall ...")
    r = sh([PY, "-m", "compileall", "-q"] + CODE_DIRS)
    if r.returncode != 0:
        print((r.stdout + r.stderr)[-1500:])
        return False
    print("      ok")
    return True


def step_cli():
    print("[2/3] CLI -h smoke ...")
    bad = []
    for rel in py_scripts():
        r = sh([PY, os.path.join(ROOT, rel), "-h"])
        if r.returncode != 0:
            tail = (r.stderr or r.stdout).strip().splitlines()
            bad.append((rel, tail[-1] if tail else "exit %d" % r.returncode))
        else:
            print("      ok  %s" % rel)
    for rel, why in bad:
        print("      FAIL %s -> %s" % (rel, why))
    return not bad


def step_guard():
    print("[3/3] real-asset / credential guard ...")
    hits = []
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = [d for d in dn if d not in SKIP_DIR]
        for f in fn:
            if os.path.splitext(f)[1].lower() in SKIP_EXT:
                continue
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 3_000_000:
                    continue
                text = open(p, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            rel = os.path.relpath(p, ROOT)
            for name, rx in (("vendor-domain", VENDOR), ("private-ip", PRIVATE_IP), ("secret", SECRET)):
                for m in rx.finditer(text):
                    line = text[:m.start()].count("\n") + 1
                    hits.append("%s:%d  %s  (%s)" % (rel, line, m.group(0), name))
    if hits:
        print("      %d hit(s) need cleaning:" % len(hits))
        for h in hits[:40]:
            print("      - " + h)
        return False
    print("      ok")
    return True


def step_pyflakes():
    print("[opt] pyflakes ...")
    if not shutil.which("pyflakes") and sh([PY, "-c", "import pyflakes"]).returncode != 0:
        print("      skipped (pip install pyflakes to enable)")
        return True
    r = sh([PY, "-m", "pyflakes"] + CODE_DIRS)
    out = (r.stdout + r.stderr).strip()
    if out:
        print("      notices (non-blocking):")
        for line in out.splitlines()[:30]:
            print("      " + line)
    else:
        print("      ok")
    return True


def main():
    ap = argparse.ArgumentParser(description="Strata self-check")
    ap.add_argument("--quick", action="store_true", help="compile + guard only")
    a = ap.parse_args()

    ok = step_compile()
    if not a.quick:
        ok &= step_cli()
    ok &= step_guard()
    if not a.quick:
        step_pyflakes()

    print()
    print("result: " + ("all green" if ok else "blocking failures above"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
