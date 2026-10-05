import copy
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("production_evidence",ROOT/"scripts"/"production_evidence.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
BASE=json.loads((ROOT/"examples"/"production-evidence.example.json").read_text())

def test_example_is_valid_and_segment_harm_blocks_success():
    assert mod.validate_record(BASE)==[]
    assert mod.value_status(BASE)=="OUTCOME_CHALLENGED"

def test_healthy_release_without_outcome_evidence_is_unverified():
    data=copy.deepcopy(BASE)
    data["outcome"]["evidence_refs"]=[]
    data["outcome"]["target_met"]=None
    data["outcome"]["guardrails"]="UNKNOWN"
    data["outcome"]["segment_harm"]=None
    assert mod.value_status(data)=="UNVERIFIED_OUTCOME"

def test_success_requires_outcome_guardrails_and_no_segment_harm():
    data=copy.deepcopy(BASE)
    data["outcome"]["target_met"]=True
    data["outcome"]["guardrails"]="PASS"
    data["outcome"]["segment_harm"]=False
    data["delta"]={"present":False,"statement":"","classification":"NONE","learning_effect":"SUPPORT","confidence":"high"}
    data["propagation"]=[{"ref":"outcome:review","status":"NO_CHANGE","owner":"product-owner"}]
    data["closure"]="CLOSED"
    assert mod.validate_record(data)==[]
    assert mod.value_status(data)=="SUCCESS_SUPPORTED"

def test_unknown_instrumentation_cannot_support_success():
    data=copy.deepcopy(BASE)
    data["outcome"]["guardrails"]="PASS"
    data["outcome"]["segment_harm"]=False
    data["observation"]["instrumentation"]["quality"]="unknown"
    assert mod.value_status(data)=="UNVERIFIED_OUTCOME"

def test_material_delta_requires_propagation_review():
    data=copy.deepcopy(BASE)
    data["propagation"]=[]
    assert "material production delta requires propagation review" in mod.validate_record(data)

def test_closed_record_cannot_hide_open_propagation():
    data=copy.deepcopy(BASE)
    data["closure"]="CLOSED"
    assert "closure=CLOSED with unresolved propagation" in mod.validate_record(data)
