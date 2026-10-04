import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("route_work", ROOT / "scripts" / "route_work.py")
route_work = importlib.util.module_from_spec(spec)
spec.loader.exec_module(route_work)


def test_simple_ui_change_stays_small():
    result = route_work.route_task({"task_class": "UI_UX", "risk": "R0"})
    assert result["risk"] == "R0"
    assert result["stages"] == [7, 8, 12, 15]
    assert 3 not in result["stages"]
    assert 16 not in result["stages"]


def test_financial_rule_escalates_feature_to_r3_and_domain():
    result = route_work.route_task({
        "task_class": "FEATURE",
        "risk": "R1",
        "concerns": ["money_or_critical_business_rule"],
    })
    assert result["risk"] == "R3"
    assert result["stages"] == [3, 4, 15]


def test_incident_routes_observability_and_recovery_and_keeps_them_protected():
    result = route_work.route_task({
        "task_class": "INCIDENT",
        "risk": "R0",
        "evidence_satisfied_stages": [20, 21],
    })
    assert result["risk"] == "R3"
    assert 20 in result["stages"] and 21 in result["stages"]
    assert result["skipped"] == []


def test_production_data_mutation_requires_recovery_evidence_route():
    result = route_work.route_task({
        "task_class": "DATA_REPAIR",
        "concerns": ["production_data_mutation"],
        "evidence_satisfied_stages": [4, 14],
    })
    assert result["risk"] == "R3"
    assert result["stages"] == [14, 15, 20, 21]
    assert {x["stage"] for x in result["skipped"]} == {4}


def test_unknown_concern_fails_closed():
    with pytest.raises(ValueError, match="unknown concerns"):
        route_work.route_task({"task_class": "BUG", "concerns": ["magic"]})
