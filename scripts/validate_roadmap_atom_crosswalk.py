#!/usr/bin/env python3
"""Check candidate crosswalk structure; never infer semantic correctness from its PASS."""
import json
import re
from pathlib import Path

path = Path(__file__).resolve().parent.parent / "research/roadmap-sh/atom-crosswalk-draft.json"
x = json.loads(path.read_text(encoding="utf-8"))
steps = x["steps"]
assert len(steps) == 171, "expected 171 steps"
assert len(set(a["id"] for a in steps)) == 171, "duplicate step IDs"
assert set(a["stage"] for a in steps) == set(range(1, 26)), "incomplete stages"
assert all(re.fullmatch(r"[0-9]{2}\.[0-9]{2}", a["id"]) for a in steps)
assert all(a["stage"] == int(a["id"][:2]) for a in steps)
assert all(a["mapping_status"] == "UNVERIFIED" or (a["evidence_refs"] and a["verified_roadmap_links"]) for a in steps), "verified link without evidence"
assert all(a["mapping_status"] != "VERIFIED" or a["test_refs"] for a in steps), "verified link without tests"
candidates = x["stage_candidates"]
assert len(candidates) == 25 and set(a["stage"] for a in candidates) == set(range(1, 26))
assert all(len(a["candidate_roadmaps"]) == len(set(a["candidate_roadmaps"])) for a in candidates)
print("PASS: 171 steps, 25 stages; no duplicate IDs and no falsely VERIFIED mapping")
