#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

DELTA_CLASSES = {
    "NONE","IMPLEMENTATION_DEFECT","DOMAIN_GAP","REQUIREMENT_GAP","DATA_QUALITY",
    "INSTRUMENTATION_DEFECT","OPERATOR_WORKFLOW_SIGNAL","MISSING_EXCEPTION",
    "NEW_CONTEXT","SECURITY_RELIABILITY_INCIDENT","OUTCOME_HYPOTHESIS_FALSIFIED","UNRESOLVED"
}
LEARNING = {"NO_CHANGE","SUPPORT","SCOPE","EXTEND","CHALLENGE","FALSIFY","UNRESOLVED"}
PROPAGATION = {"NO_CHANGE","UPDATE_REQUIRED","SUPERSEDE","NEW_EVAL","UNKNOWN"}

def validate_record(data):
    errors=[]
    for key in ("id","owner","expectation","release","observation","outcome","delta","propagation"):
        if key not in data:
            errors.append(f"missing {key}")
    if errors:
        return errors

    exp=data["expectation"]
    for key in ("ref","kind","statement","population"):
        if not exp.get(key):
            errors.append(f"expectation.{key} is required")

    release=data["release"]
    if release.get("environment") != "production":
        errors.append("release.environment must be production")
    if not release.get("ref"):
        errors.append("release.ref is required")
    if not isinstance(release.get("healthy"), bool):
        errors.append("release.healthy must be boolean")

    obs=data["observation"]
    for key in ("statement","population"):
        if not obs.get(key):
            errors.append(f"observation.{key} is required")
    window=obs.get("window",{})
    if not window.get("from") or not window.get("to"):
        errors.append("observation.window.from/to are required")
    if not obs.get("evidence_refs"):
        errors.append("observation.evidence_refs must be non-empty")
    instrumentation=obs.get("instrumentation",{})
    quality=instrumentation.get("quality")
    if quality not in {"known","limited","unknown"}:
        errors.append("observation.instrumentation.quality invalid")
    if not isinstance(instrumentation.get("limitations"), list):
        errors.append("observation.instrumentation.limitations must be a list")

    outcome=data["outcome"]
    if not isinstance(outcome.get("evidence_refs"), list):
        errors.append("outcome.evidence_refs must be a list")
    if outcome.get("target_met") not in {True,False,None}:
        errors.append("outcome.target_met must be boolean or null")
    if outcome.get("guardrails") not in {"PASS","FAIL","UNKNOWN"}:
        errors.append("outcome.guardrails invalid")
    if outcome.get("segment_harm") not in {True,False,None}:
        errors.append("outcome.segment_harm must be boolean or null")

    delta=data["delta"]
    if not isinstance(delta.get("present"), bool):
        errors.append("delta.present must be boolean")
    if delta.get("classification") not in DELTA_CLASSES:
        errors.append("delta.classification invalid")
    if delta.get("learning_effect") not in LEARNING:
        errors.append("delta.learning_effect invalid")
    if delta.get("confidence") not in {"low","medium","high"}:
        errors.append("delta.confidence invalid")
    if delta.get("present") and not str(delta.get("statement","")).strip():
        errors.append("delta.statement is required when delta.present=true")
    if not delta.get("present") and delta.get("classification") != "NONE":
        errors.append("delta.classification must be NONE when no delta is present")

    propagation=data["propagation"]
    if not isinstance(propagation,list):
        errors.append("propagation must be a list")
    else:
        for i,item in enumerate(propagation):
            if not item.get("ref") or not item.get("owner"):
                errors.append(f"propagation[{i}] requires ref and owner")
            if item.get("status") not in PROPAGATION:
                errors.append(f"propagation[{i}].status invalid")
    if delta.get("present") and not propagation:
        errors.append("material production delta requires propagation review")

    if data.get("closure") == "CLOSED":
        unresolved=[x for x in propagation if x.get("status") in {"UPDATE_REQUIRED","UNKNOWN"}]
        if unresolved:
            errors.append("closure=CLOSED with unresolved propagation")
        if delta.get("present") and delta.get("learning_effect") == "UNRESOLVED":
            errors.append("closure=CLOSED with unresolved learning effect")
    return errors

def value_status(data):
    release=data["release"]
    outcome=data["outcome"]
    quality=data["observation"]["instrumentation"]["quality"]
    if not release["healthy"]:
        return "NOT_HEALTHY"
    if not outcome["evidence_refs"] or outcome["target_met"] is None:
        return "UNVERIFIED_OUTCOME"
    if quality == "unknown":
        return "UNVERIFIED_OUTCOME"
    if outcome["target_met"] is False:
        return "OUTCOME_CHALLENGED"
    if outcome["guardrails"] != "PASS":
        return "OUTCOME_CHALLENGED"
    if outcome["segment_harm"] is not False:
        return "OUTCOME_CHALLENGED"
    return "SUCCESS_SUPPORTED"

def summarize(data):
    return {
        "id":data["id"],
        "value_status":value_status(data),
        "delta_present":data["delta"]["present"],
        "delta_classification":data["delta"]["classification"],
        "learning_effect":data["delta"]["learning_effect"],
        "propagation_open":[
            x["ref"] for x in data["propagation"]
            if x["status"] in {"UPDATE_REQUIRED","UNKNOWN","NEW_EVAL"}
        ],
        "closure":data.get("closure","OPEN")
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("record")
    p.add_argument("--check",action="store_true")
    args=p.parse_args()
    data=json.loads(Path(args.record).read_text(encoding="utf-8"))
    errors=validate_record(data)
    if errors:
        print("PRODUCTION EVIDENCE FAIL")
        for e in errors:
            print("-",e)
        return 1
    summary=summarize(data)
    if args.check:
        print("PRODUCTION EVIDENCE PASS")
        print(f"value_status={summary['value_status']} closure={summary['closure']}")
    else:
        print(json.dumps(summary,indent=2,ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
