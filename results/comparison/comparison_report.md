# Benchmark Comparison

Generated from `results/all_results.json` by `scripts/compare_benchmarks.py`.

## Average Latency

Lower latency is better.

| Rank | Database | Point Lookup | 1-Hop Traversal | 2-Hop Traversal | 3-Hop Traversal | Indexed Lookup | Aggregation | Mixed Read/Write | Concurrency |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | neo4j | 61.10 ms | 61.94 ms | 95.36 ms | 268.02 ms | 112.56 ms | 64.84 ms | 133.39 ms | 71.49 ms |
| 2 | falkordb | 114.64 ms | 116.58 ms | 120.67 ms | 154.99 ms | 130.79 ms | 114.76 ms | 230.65 ms | 120.81 ms |
| 3 | memgraph | 163.42 ms | 162.79 ms | 206.33 ms | 493.28 ms | 235.35 ms | 163.02 ms | 332.70 ms | 173.68 ms |
| 4 | cognodb | 228.97 ms | 218.48 ms | 262.51 ms | 765.53 ms | 287.49 ms | 229.13 ms | 798.66 ms | 228.71 ms |
| 5 | arangodb | 237.56 ms | 212.79 ms | 228.98 ms | 2,059.88 ms | 226.56 ms | 220.99 ms | 631.14 ms | 269.81 ms |

## Relative Performance

Percentage slower is calculated relative to the best result for each workload: `((database latency - best latency) / database latency) * 100`.

| Workload | Database | Average | Relative to best |
|---|---|---:|---:|
| Aggregation | neo4j | 64.84 ms | Best |
| Aggregation | falkordb | 114.76 ms | 43.50% |
| Aggregation | memgraph | 163.02 ms | 60.22% |
| Aggregation | arangodb | 220.99 ms | 70.66% |
| Aggregation | cognodb | 229.13 ms | 71.70% |
| Concurrency | neo4j | 71.49 ms | Best |
| Concurrency | falkordb | 120.81 ms | 40.82% |
| Concurrency | memgraph | 173.68 ms | 58.84% |
| Concurrency | cognodb | 228.71 ms | 68.74% |
| Concurrency | arangodb | 269.81 ms | 73.50% |
| 1-Hop Traversal | neo4j | 61.94 ms | Best |
| 1-Hop Traversal | falkordb | 116.58 ms | 46.87% |
| 1-Hop Traversal | memgraph | 162.79 ms | 61.95% |
| 1-Hop Traversal | arangodb | 212.79 ms | 70.89% |
| 1-Hop Traversal | cognodb | 218.48 ms | 71.65% |
| 2-Hop Traversal | neo4j | 95.36 ms | Best |
| 2-Hop Traversal | falkordb | 120.67 ms | 20.97% |
| 2-Hop Traversal | memgraph | 206.33 ms | 53.78% |
| 2-Hop Traversal | arangodb | 228.98 ms | 58.35% |
| 2-Hop Traversal | cognodb | 262.51 ms | 63.67% |
| 3-Hop Traversal | falkordb | 154.99 ms | Best |
| 3-Hop Traversal | neo4j | 268.02 ms | 42.17% |
| 3-Hop Traversal | memgraph | 493.28 ms | 68.58% |
| 3-Hop Traversal | cognodb | 765.53 ms | 79.75% |
| 3-Hop Traversal | arangodb | 2,059.88 ms | 92.48% |
| Indexed Lookup | neo4j | 112.56 ms | Best |
| Indexed Lookup | falkordb | 130.79 ms | 13.94% |
| Indexed Lookup | arangodb | 226.56 ms | 50.32% |
| Indexed Lookup | memgraph | 235.35 ms | 52.17% |
| Indexed Lookup | cognodb | 287.49 ms | 60.85% |
| Mixed Read/Write | neo4j | 133.39 ms | Best |
| Mixed Read/Write | falkordb | 230.65 ms | 42.17% |
| Mixed Read/Write | memgraph | 332.70 ms | 59.91% |
| Mixed Read/Write | arangodb | 631.14 ms | 78.87% |
| Mixed Read/Write | cognodb | 798.66 ms | 83.30% |
| Point Lookup | neo4j | 61.10 ms | Best |
| Point Lookup | falkordb | 114.64 ms | 46.70% |
| Point Lookup | memgraph | 163.42 ms | 62.61% |
| Point Lookup | cognodb | 228.97 ms | 73.32% |
| Point Lookup | arangodb | 237.56 ms | 74.28% |

## P95 Latency

| Workload | neo4j | falkordb | memgraph | cognodb | arangodb |
|---|---:|---:|---:|---:|---:|
| Point Lookup | 66.92 ms | 122.42 ms | 171.93 ms | 272.72 ms | 290.51 ms |
| 1-Hop Traversal | 67.68 ms | 131.72 ms | 168.53 ms | 224.77 ms | 250.67 ms |
| 2-Hop Traversal | 103.20 ms | 130.93 ms | 218.14 ms | 281.34 ms | 298.58 ms |
| 3-Hop Traversal | 321.05 ms | 175.29 ms | 544.86 ms | 862.06 ms | 2,301.51 ms |
| Indexed Lookup | 124.18 ms | 143.15 ms | 254.63 ms | 307.68 ms | 292.60 ms |
| Aggregation | 71.52 ms | 120.31 ms | 169.08 ms | 249.25 ms | 289.23 ms |
| Mixed Read/Write | 139.57 ms | 247.50 ms | 363.12 ms | 879.73 ms | 687.43 ms |
| Concurrency | 79.35 ms | 124.95 ms | 189.14 ms | 237.43 ms | 398.35 ms |
