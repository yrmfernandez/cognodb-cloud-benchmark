# Benchmark Comparison

Generated from `results/all_results.json` by `scripts/compare_benchmarks.py`.

## Average Latency

Lower latency is better.

| Rank | Database | Point Lookup | 1-Hop Traversal | 2-Hop Traversal | 3-Hop Traversal | Indexed Lookup | Aggregation |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | neo4j | 82.79 ms | 65.37 ms | 94.64 ms | 267.36 ms | 111.51 ms | 63.76 ms |
| 2 | falkordb | 112.33 ms | 112.72 ms | 120.28 ms | 157.02 ms | 131.97 ms | 113.18 ms |
| 3 | memgraph | 162.26 ms | 162.24 ms | 202.92 ms | 488.22 ms | 239.36 ms | 166.33 ms |
| 4 | cognodb | 218.89 ms | 217.96 ms | 260.45 ms | 728.09 ms | 287.94 ms | 230.60 ms |
| 5 | arangodb | 220.28 ms | 221.10 ms | 238.82 ms | 2,180.94 ms | 235.69 ms | 218.70 ms |

## Relative Performance

Percentage slower is calculated relative to the best result for each workload: `((database latency - best latency) / database latency) * 100`.

| Workload | Database | Average | Relative to best |
|---|---|---:|---:|
| Aggregation | neo4j | 63.76 ms | Best |
| Aggregation | falkordb | 113.18 ms | 43.67% |
| Aggregation | memgraph | 166.33 ms | 61.67% |
| Aggregation | arangodb | 218.70 ms | 70.85% |
| Aggregation | cognodb | 230.60 ms | 72.35% |
| 1-Hop Traversal | neo4j | 65.37 ms | Best |
| 1-Hop Traversal | falkordb | 112.72 ms | 42.01% |
| 1-Hop Traversal | memgraph | 162.24 ms | 59.71% |
| 1-Hop Traversal | cognodb | 217.96 ms | 70.01% |
| 1-Hop Traversal | arangodb | 221.10 ms | 70.44% |
| 2-Hop Traversal | neo4j | 94.64 ms | Best |
| 2-Hop Traversal | falkordb | 120.28 ms | 21.32% |
| 2-Hop Traversal | memgraph | 202.92 ms | 53.36% |
| 2-Hop Traversal | arangodb | 238.82 ms | 60.37% |
| 2-Hop Traversal | cognodb | 260.45 ms | 63.66% |
| 3-Hop Traversal | falkordb | 157.02 ms | Best |
| 3-Hop Traversal | neo4j | 267.36 ms | 41.27% |
| 3-Hop Traversal | memgraph | 488.22 ms | 67.84% |
| 3-Hop Traversal | cognodb | 728.09 ms | 78.43% |
| 3-Hop Traversal | arangodb | 2,180.94 ms | 92.80% |
| Indexed Lookup | neo4j | 111.51 ms | Best |
| Indexed Lookup | falkordb | 131.97 ms | 15.51% |
| Indexed Lookup | arangodb | 235.69 ms | 52.69% |
| Indexed Lookup | memgraph | 239.36 ms | 53.41% |
| Indexed Lookup | cognodb | 287.94 ms | 61.27% |
| Point Lookup | neo4j | 82.79 ms | Best |
| Point Lookup | falkordb | 112.33 ms | 26.29% |
| Point Lookup | memgraph | 162.26 ms | 48.98% |
| Point Lookup | cognodb | 218.89 ms | 62.18% |
| Point Lookup | arangodb | 220.28 ms | 62.42% |

## P95 Latency

| Workload | neo4j | falkordb | memgraph | cognodb | arangodb |
|---|---:|---:|---:|---:|---:|
| Point Lookup | 150.13 ms | 118.08 ms | 166.88 ms | 225.94 ms | 290.12 ms |
| 1-Hop Traversal | 71.62 ms | 121.81 ms | 166.78 ms | 223.16 ms | 282.99 ms |
| 2-Hop Traversal | 109.06 ms | 129.91 ms | 217.81 ms | 275.22 ms | 301.40 ms |
| 3-Hop Traversal | 320.14 ms | 177.52 ms | 542.65 ms | 810.12 ms | 3,223.45 ms |
| Indexed Lookup | 121.03 ms | 162.46 ms | 268.36 ms | 304.93 ms | 302.80 ms |
| Aggregation | 67.00 ms | 118.84 ms | 173.84 ms | 238.02 ms | 295.79 ms |
