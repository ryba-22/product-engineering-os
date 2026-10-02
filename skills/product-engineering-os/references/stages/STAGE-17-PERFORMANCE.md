# Stage 17 — Performance

**Module:** quality-engineering  
**Gate:** G8  
**Evidence anchors:** EVD-PERF-002, EVD-PERF-003  
**Primary artifact:** `07-templates/PERFORMANCE-BUDGET.md`

## Purpose
Make performance a measurable product/system contract rather than a late optimization exercise. Define budgets from user/business scenarios, test under representative workloads, and use profiling to explain bottlenecks before tuning.

## Required inputs
Critical user/system scenarios, expected concurrency and dataset size, architecture/dependency model, frontend/network characteristics, SLOs where defined, growth assumptions and release risk.

## Questions the Brain must answer
1. Which latency, throughput or resource metric matters to the user/business outcome?
2. What percentile/window and workload define acceptable behavior?
3. What dataset size and concurrency are representative?
4. Which dependencies dominate the budget?
5. What baseline exists before change?
6. Which stress/spike/soak conditions reflect credible risk?
7. What resource saturation signals explain degradation?
8. Which threshold should block or warn in CI/release?

## Workflow
1. **Define scenario budgets.** Use p50/p95/p99, throughput, error rate, frontend responsiveness or resource limits as appropriate.
2. **State workload assumptions.** Requests/sec, concurrent actors, dataset size, payload shape, cache state and dependency latency.
3. **Capture baseline.** Measure current system under a controlled environment before optimization claims.
4. **Run expected-load tests.** Verify normal operating budget.
5. **Run risk-specific tests.** Stress for limits, spike for sudden load, soak for leaks/slow degradation.
6. **Observe system internals.** CPU, memory, DB waits/locks, queue depth, downstream latency, network and browser rendering.
7. **Profile the bottleneck.** Tune based on evidence rather than intuition.
8. **Retest after change.** Compare distributions, not just averages.
9. **Define regression enforcement.** CI or scheduled tests where stable enough; production SLO/telemetry for environment-dependent behavior.
10. **Document capacity and switching thresholds.**

## Decision rules
- Average latency hides tail behavior and is insufficient for critical performance guarantees.
- Load tests without a realistic workload model produce weak evidence.
- A fast endpoint on an empty database is not evidence of production-scale performance.
- Caching changes correctness and invalidation behavior; performance benefit must justify that complexity.
- Optimize measured bottlenecks before micro-optimizing code.
- Performance budgets can vary by scenario; one global number rarely represents all flows.

## Evidence standard
Performance claims identify version, environment, workload, dataset and metric distribution. Material conclusions should be reproducible or corroborated by production telemetry.

## Canonical outputs
Performance Budget; workload model; baseline/results; bottleneck profile; capacity assumptions; regression thresholds; optimization ADRs and residual risks.

## Failure modes
Benchmark theater; testing only happy cached paths; averages only; synthetic workload unrelated to users; production tuning without baseline; “premature optimization” used to ignore explicit budgets; no soak testing for long-lived workers.

## Exit conditions
G8 performance scope is satisfied when critical scenarios meet budgets with representative evidence or the residual gap is explicitly accepted with mitigation and capacity limits.

## Handoff
Stage 18 may enforce stable budgets. Stage 19 uses rollout telemetry to confirm behavior. Stage 20 owns continuous SLO/performance signals.
