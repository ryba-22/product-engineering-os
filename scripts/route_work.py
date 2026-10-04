#!/usr/bin/env python3
"""Produce a deterministic baseline PEOS route from a JSON task descriptor."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "machine" / "workflow-router.json"
RISK = {f"R{i}": i for i in range(5)}


def load_config():
    return json.loads(CONFIG.read_text())


def route_task(payload, config=None):
    config = config or load_config()
    task_class = str(payload.get("task_class", "")).upper()
    if task_class not in config["task_classes"]:
        raise ValueError(f"unknown task_class: {task_class or '<missing>'}")
    concerns = payload.get("concerns", [])
    if not isinstance(concerns, list):
        raise ValueError("concerns must be a list")
    unknown = sorted(set(concerns) - set(config["concern_overlays"]))
    if unknown:
        raise ValueError("unknown concerns: " + ", ".join(unknown))

    requested = str(payload.get("risk", "R0")).upper()
    if requested not in RISK:
        raise ValueError(f"invalid risk: {requested}")

    class_cfg = config["task_classes"][task_class]
    floors = [requested, class_cfg["risk_floor"]]
    stages = list(class_cfg["stages"])
    reasons = {str(s): [f"default for {task_class}"] for s in stages}
    for concern in concerns:
        overlay = config["concern_overlays"][concern]
        floors.append(overlay["risk_floor"])
        for stage in overlay["stages"]:
            stages.append(stage)
            reasons.setdefault(str(stage), []).append(f"concern: {concern}")

    effective_risk = max(floors, key=lambda r: RISK[r])
    order = {stage: i for i, stage in enumerate(config["ordering"])}
    stages = sorted(set(stages), key=lambda s: order.get(s, 999))

    requested_skips = payload.get("evidence_satisfied_stages", [])
    if not isinstance(requested_skips, list) or any(not isinstance(x, int) for x in requested_skips):
        raise ValueError("evidence_satisfied_stages must be a list of integers")
    protected = set()
    if effective_risk in {"R3", "R4"}:
        protected.add(15)
    if "production_data_mutation" in concerns:
        protected.update({14, 15, 20, 21})
    if task_class == "INCIDENT":
        protected.update({20, 21})
    skipped = []
    for stage in requested_skips:
        if stage in stages and stage not in protected:
            stages.remove(stage)
            skipped.append({"stage": stage, "reason": "decision already backed by current evidence"})

    return {
        "task_class": task_class,
        "risk": effective_risk,
        "stages": stages,
        "reasons": {k: v for k, v in reasons.items() if int(k) in stages},
        "skipped": skipped,
        "required_evidence": payload.get("required_evidence", []),
        "stop_condition": class_cfg["stop"],
        "reroute_triggers": config["reroute_triggers"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task_json", help="path to task descriptor JSON or '-' for stdin")
    args = parser.parse_args()
    raw = sys.stdin.read() if args.task_json == "-" else Path(args.task_json).read_text()
    try:
        result = route_task(json.loads(raw))
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ROUTER ERROR: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
