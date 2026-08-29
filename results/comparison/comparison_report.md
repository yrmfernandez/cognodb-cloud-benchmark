# Benchmark Comparison

Generated from `results/all_results.json` by `scripts/compare_benchmarks.py`.

## Average Latency

Lower latency is better.

| Rank | Database | Point Lookup | 1-Hop | 2-Hop | 3-Hop | Indexed Lookup |
|---:|---|---:|---:|---:|---:|---:|
| 1 | neo4j | 70.77 ms | 75.02 ms | 98.24 ms | 332.81 ms | 114.56 ms |
| 2 | falkordb | 113.35 ms | 117.38 ms | 122.60 ms | 156.46 ms | 131.80 ms |
| 3 | memgraph | 169.22 ms | 164.53 ms | 198.09 ms | 480.29 ms | 226.12 ms |
| 4 | arangodb | 217.85 ms | 216.74 ms | 254.70 ms | 2,065.94 ms | 229.32 ms |
| 5 | cognodb | 220.82 ms | 221.21 ms | 259.67 ms | 775.37 ms | 285.76 ms |

## Relative Performance

Percentage slower is calculated relative to the best result for each workload: `((database latency - best latency) / database latency) * 100`.

| Workload | Database | Average | Relative to best |
|---|---|---:|---:|
| 1-Hop Traversal | neo4j | 75.02 ms | Best |
| 1-Hop Traversal | falkordb | 117.38 ms | 36.08% |
| 1-Hop Traversal | memgraph | 164.53 ms | 54.40% |
| 1-Hop Traversal | arangodb | 216.74 ms | 65.39% |
| 1-Hop Traversal | cognodb | 221.21 ms | 66.09% |
| 2-Hop Traversal | neo4j | 98.24 ms | Best |
| 2-Hop Traversal | falkordb | 122.60 ms | 19.87% |
| 2-Hop Traversal | memgraph | 198.09 ms | 50.41% |
| 2-Hop Traversal | arangodb | 254.70 ms | 61.43% |
| 2-Hop Traversal | cognodb | 259.67 ms | 62.17% |
| 3-Hop Traversal | falkordb | 156.46 ms | Best |
| 3-Hop Traversal | neo4j | 332.81 ms | 52.99% |
| 3-Hop Traversal | memgraph | 480.29 ms | 67.42% |
| 3-Hop Traversal | cognodb | 775.37 ms | 79.82% |
| 3-Hop Traversal | arangodb | 2,065.94 ms | 92.43% |
| Indexed Lookup | neo4j | 114.56 ms | Best |
| Indexed Lookup | falkordb | 131.80 ms | 13.09% |
| Indexed Lookup | memgraph | 226.12 ms | 49.34% |
| Indexed Lookup | arangodb | 229.32 ms | 50.05% |
| Indexed Lookup | cognodb | 285.76 ms | 59.91% |
| Point Lookup | neo4j | 70.77 ms | Best |
| Point Lookup | falkordb | 113.35 ms | 37.56% |
| Point Lookup | memgraph | 169.22 ms | 58.17% |
| Point Lookup | arangodb | 217.85 ms | 67.51% |
| Point Lookup | cognodb | 220.82 ms | 67.95% |

## P95 Latency

| Workload | neo4j | falkordb | memgraph | arangodb | cognodb |
|---|---:|---:|---:|---:|---:|
| Point Lookup | 98.73 ms | 119.54 ms | 191.78 ms | 290.47 ms | 244.55 ms |
| 1-Hop Traversal | 115.54 ms | 131.44 ms | 173.24 ms | 282.40 ms | 231.03 ms |
| 2-Hop Traversal | 119.91 ms | 129.11 ms | 207.26 ms | 305.01 ms | 270.54 ms |
| 3-Hop Traversal | 502.12 ms | 165.59 ms | 516.91 ms | 2,362.40 ms | 937.43 ms |
| Indexed Lookup | 124.86 ms | 145.62 ms | 243.95 ms | 292.57 ms | 312.66 ms |
