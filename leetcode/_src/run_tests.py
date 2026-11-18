#!/usr/bin/env python3
"""Validate problem files: dict shape, runnable solution, TESTS pass. Usage: run_tests.py [slug ...] (default: all)."""
import sys, os, re, importlib.util, traceback, glob
HERE = os.path.dirname(os.path.abspath(__file__))
CATS = {"Array","Binary","Dynamic Programming","Graph","Interval","Linked List","Matrix","String","Tree","Heap"}

def load(path):
    spec = importlib.util.spec_from_file_location("p", path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def helpers_ns():
    ns = {}; exec(open(os.path.join(HERE, "helpers.py")).read(), ns); return ns

def validate(P, slug):
    errs = []
    need = ["slug","number","title","category","difficulty","url","premium","statement_html","intro_html","blocks","complexity"]
    for k in need:
        if k not in P: errs.append(f"missing key {k}")
    if errs: return errs
    if P["slug"] != slug: errs.append(f"slug {P['slug']!r} != file {slug!r}")
    if P["category"] not in CATS: errs.append(f"bad category {P['category']!r}")
    if P["difficulty"] not in ("Easy","Medium","Hard"): errs.append("bad difficulty")
    if not isinstance(P["number"], int) or P["number"] <= 0: errs.append("number must be positive int")
    if not P["url"].startswith("https://leetcode.com/problems/"): errs.append("bad url")
    b = P["blocks"]
    if not (5 <= len(b) <= 14): errs.append(f"{len(b)} blocks (want 5..14)")
    for i, x in enumerate(b):
        for k in ("code","explain","diagram"):
            if k not in x: errs.append(f"block {i} missing {k}")
        if x.get("code","").strip() == "": errs.append(f"block {i} empty code")
        if not re.search(r"<p>", x.get("explain","")): errs.append(f"block {i} explain has no <p>")
        if x.get("diagram") is not None:
            lines = x["diagram"].split("\n")
            if len(lines) > 16: errs.append(f"block {i} diagram {len(lines)} lines (max 16)")
            if max(len(l) for l in lines) > 78: errs.append(f"block {i} diagram wider than 78 cols")
            if "&lt;" in x["diagram"] or "&gt;" in x["diagram"]: errs.append(f"block {i} diagram has HTML entities")
        if re.search(r"<(?!/?(p|code|strong|em|ul|li|pre|br|sup|sub)\b)", x.get("explain","")): errs.append(f"block {i} explain: raw < or unexpected tag")
    withd = sum(1 for x in b if x.get("diagram"))
    if withd * 2 < len(b): errs.append(f"only {withd}/{len(b)} blocks have diagrams (need at least half)")
    if "<pre>" not in P["statement_html"]: errs.append("statement_html has no <pre> example")
    if "<ul>" not in P["statement_html"]: errs.append("statement_html has no <ul> constraints")
    if "—" in (P["statement_html"] + P["intro_html"] + "".join(x["explain"] for x in b)): errs.append("em dash found")
    return errs

def run(slug):
    path = os.path.join(HERE, "problems", slug + ".py")
    try: m = load(path)
    except Exception as e: return [f"import error: {e}"]
    P = getattr(m, "PROBLEM", None); T = getattr(m, "TESTS", None)
    if not isinstance(P, dict) or not isinstance(T, str): return ["PROBLEM dict or TESTS string missing"]
    errs = validate(P, slug)
    code = "\n".join(x["code"] for x in P["blocks"])
    ns = helpers_ns()
    try: exec(compile(code, slug + ".py", "exec"), ns)
    except Exception: errs.append("solution does not run:\n" + traceback.format_exc(limit=2)); return errs
    if T.count("assert") < 4: errs.append(f"only {T.count('assert')} asserts (need 4)")
    try: exec(compile(T, slug + "_tests.py", "exec"), ns)
    except AssertionError: errs.append("TESTS failed:\n" + traceback.format_exc(limit=2))
    except Exception: errs.append("TESTS crashed:\n" + traceback.format_exc(limit=2))
    return errs

if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, "problems", "*.py")))
    bad = 0
    for s in slugs:
        e = run(s)
        if e: bad += 1; print(f"FAIL {s}"); [print("   -", x) for x in e]
        else: print(f"PASS {s}")
    print(f"{len(slugs)-bad}/{len(slugs)} passed"); sys.exit(1 if bad else 0)
