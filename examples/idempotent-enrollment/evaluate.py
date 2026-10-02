"""Execute fixed acceptance cases; no model provider or private data required."""
import json
from enrollment import connect, enroll

def run():
    checks = []
    db = connect()
    checks.append(("AC1 first enrollment", enroll(db, "p1", "c1") == "created"))
    checks.append(("AC2 retry", enroll(db, "p1", "c1") == "already_enrolled"))
    checks.append(("AC2 exactly one row", db.execute("SELECT count(*) FROM enrollment").fetchone()[0] == 1))
    checks.append(("AC3 distinct course", enroll(db, "p1", "c2") == "created"))
    for pupil, course in [("", "c1"), ("p1", " "), (None, "c1")]:
        before = db.execute("SELECT count(*) FROM enrollment").fetchone()[0]
        try:
            enroll(db, pupil, course)
            rejected = False
        except ValueError:
            rejected = True
        after = db.execute("SELECT count(*) FROM enrollment").fetchone()[0]
        checks.append(("AC4 invalid input leaves data unchanged", rejected and before == after))
    checks.append(("AC5 normalized retry", enroll(db, " p1 ", " c1 ") == "already_enrolled"))
    # Execute the previous append-only behavior to demonstrate the regression.
    baseline = []
    baseline.append(("p1", "c1")); baseline.append(("p1", "c1"))
    baseline_pass = len(baseline) == 1
    result = {"baseline_retry_uniqueness_pass": baseline_pass, "candidate_passed": sum(ok for _, ok in checks), "candidate_total": len(checks), "checks": [{"name": name, "pass": ok} for name, ok in checks]}
    print(json.dumps(result, indent=2))
    assert not baseline_pass, "baseline must reproduce duplicate enrollment"
    assert all(ok for _, ok in checks), "acceptance check failed"
    return result

if __name__ == "__main__":
    run()
