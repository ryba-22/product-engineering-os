# Performance Engineering Brain

## Start from a performance budget
Define user/business-relevant response measures before tuning. Examples: interaction latency, API p95/p99, error rate, throughput at expected load, job completion deadline, query budget, page weight/Core Web Vitals where applicable.

## Evidence ladder
1. baseline/smoke — test is valid and normal behavior is known;
2. expected-load test — meets budget under representative traffic/data;
3. stress/breakpoint — where degradation/failure starts;
4. spike — response to sudden surge;
5. soak — leaks/backlogs/degradation over time;
6. production telemetry — confirms synthetic assumptions.

Use the smallest set that covers the actual risk. Profile before optimizing. Do not report an average when tail latency or error amplification is the user-visible failure.

## Regression
Material budgets should become automated thresholds/fitness functions when cost-effective.
