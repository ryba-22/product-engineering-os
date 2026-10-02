# Performance Engineering Brain

Use with `STAGE-17-PERFORMANCE.md`. Performance engineering starts from user/business scenarios and explicit budgets, then uses workload evidence and profiling to explain behavior.

## Budget first

For each critical scenario define:
- metric: latency percentile, throughput, error rate, frontend interaction metric or resource limit;
- threshold;
- workload;
- dataset size;
- cache/warmup state;
- environment;
- observation window.

A statement like “API should be fast” is not testable. A p95 target with an unrealistic empty dataset is also weak.

## Workload model

Model:
- request/job mix;
- concurrency;
- burstiness;
- payload size;
- read/write ratio;
- hot/cold key distribution;
- background jobs;
- dependency latency/error behavior;
- realistic data cardinality.

If the workload is estimated, state the source and switching threshold.

## Evidence ladder

1. **Baseline** — current version under controlled conditions.
2. **Expected load** — normal workload and budget.
3. **Stress** — find saturation/throughput limit.
4. **Spike** — sudden load and queue/autoscaling behavior.
5. **Soak** — slow leaks, fragmentation, queue growth and degradation.
6. **Production telemetry** — validate environmental reality.

Different tests answer different questions; do not treat one as a universal benchmark.

## Diagnosis

Collect signals around:
- CPU and scheduler;
- memory/GC;
- database query time, locks, waits and pool saturation;
- cache hit/miss;
- queue depth and consumer lag;
- downstream calls;
- network/TLS;
- browser rendering/main-thread work;
- file/storage I/O.

Profile the measured bottleneck before optimizing.

## Regression policy

Stable micro/endpoint budgets may run in CI. Noisy environment-dependent tests may run scheduled or at release. Production SLOs remain the final signal for real conditions.

Choose blocking thresholds carefully: too tight creates noise; too loose permits gradual regression. Track trend as well as absolute limit.

## Optimization trade-offs

Every optimization can change another quality:
- cache → invalidation/staleness;
- batching → latency/partial failure;
- async queue → eventual consistency;
- denormalization → write complexity;
- client caching → freshness;
- aggressive retries → load amplification.

Record these as architecture/data decisions when material.

## Reporting

A trustworthy performance result names commit/artifact, environment, dataset/workload, duration, percentile distribution, errors and relevant resource signals. Do not compare results from materially different setups without qualification.

The goal is not the fastest benchmark. The goal is predictable performance within the budget at acceptable complexity and cost.
