# CognoDB Cloud Benchmark

A reproducible benchmark comparing CognoDB Cloud with other managed graph
database platforms using a common public graph dataset and equivalent
logical workloads.

## Benchmark Platforms

1. CognoDB Cloud
2. Neo4j AuraDB
3. Memgraph Cloud
4. ArangoDB ArangoGraph
5. FalkorDB Cloud

## Dataset

SNAP wiki-Vote

- Nodes: 7,115
- Relationships: 103,689
- Graph type: Directed
- Domain: Wikipedia administrator elections

The original dataset contains directed edges representing votes between
Wikipedia users.

## Benchmark Dataset Preparation

The original relationships are preserved.

A deterministic `user_type` property is added to nodes for the
indexed/filtered lookup workload:

`user_type = user_id % 10`

This property is synthetic and is clearly distinguished from the original
dataset attributes.

## Fairness

Each platform will use its lowest practical free or trial managed tier.
Because the platforms expose different resource limits, CPU, memory,
storage, and trial limitations will be documented and reported rather than
treated as identical.

## Planned Workloads

- Data ingestion
- 1-hop traversal
- 2-hop traversal
- 3-hop traversal
- Point lookup
- Indexed/filtered lookup
- Aggregation
- Mixed read/write workload
- Concurrency testing

## Benchmark Results

The benchmark evaluates five graph databases using the same dataset, workload definitions, and execution configuration.

### Benchmark Configuration

| Parameter | Value |
|---|---:|
| Databases | 5 |
| User nodes | 7,115 |
| `VOTED_FOR` relationships | 103,689 |
| Measured iterations | 100 |
| Warmup iterations | 30 |
| Starting user ID | 30 |
| Workloads | 6 |
| Failed iterations | 0 |

### Workloads

The following workloads were executed against each database:

1. **Point Lookup** — retrieves a single user by `user_id`.
2. **1-Hop Traversal** — retrieves users directly connected to the starting user.
3. **2-Hop Traversal** — retrieves users reachable through exactly two relationships.
4. **3-Hop Traversal** — retrieves users reachable through exactly three relationships.
5. **Indexed Lookup** — retrieves users matching a specific `user_type` value using the configured index.
6. **Aggregation** — counts users grouped by `user_type`.

### Average Latency Results

Lower latency indicates better performance.

| Workload | CognoDB (ms) | Neo4j (ms) | Memgraph (ms) | ArangoDB (ms) | FalkorDB (ms) | Fastest |
|---|---:|---:|---:|---:|---:|---|
| Point Lookup | 218.89 | **82.79** | 162.26 | 220.28 | 112.33 | **Neo4j** |
| 1-Hop Traversal | 217.96 | **65.37** | 162.24 | 221.10 | 112.72 | **Neo4j** |
| 2-Hop Traversal | 260.45 | **94.64** | 202.92 | 238.82 | 120.28 | **Neo4j** |
| 3-Hop Traversal | 728.09 | 267.36 | 488.22 | 2180.94 | **157.02** | **FalkorDB** |
| Indexed Lookup | 287.94 | **111.51** | 239.36 | 235.69 | 131.97 | **Neo4j** |
| Aggregation | 230.60 | **63.76** | 166.33 | 218.70 | 113.18 | **Neo4j** |

### Performance Advantage

The following shows how much faster the best-performing database was compared with the second-fastest database for each workload.

| Workload | Fastest | Second Fastest | Advantage |
|---|---|---|---:|
| Point Lookup | Neo4j | FalkorDB | **26.3%** |
| 1-Hop Traversal | Neo4j | FalkorDB | **42.0%** |
| 2-Hop Traversal | Neo4j | FalkorDB | **21.3%** |
| 3-Hop Traversal | FalkorDB | Neo4j | **41.3%** |
| Indexed Lookup | Neo4j | FalkorDB | **15.5%** |
| Aggregation | Neo4j | FalkorDB | **43.7%** |

Percentage advantage is calculated as:

```text
((second-fastest latency - fastest latency) / second-fastest latency) × 100
```

### Relative Performance by Workload

The following tables compare each database with the fastest database for that workload. The percentage is calculated as:

```text
((database latency - best latency) / database latency) × 100
```

#### Point Lookup

| Database | Average latency | Relative performance |
|---|---:|---:|
| **Neo4j** | **82.79 ms** | **Best** |
| FalkorDB | 112.33 ms | 26.29% slower |
| Memgraph | 162.26 ms | 48.98% slower |
| CognoDB | 218.89 ms | 62.18% slower |
| ArangoDB | 220.28 ms | 62.42% slower |

#### 1-Hop Traversal

| Database | Average latency | Relative performance |
|---|---:|---:|
| **Neo4j** | **65.37 ms** | **Best** |
| FalkorDB | 112.72 ms | 42.01% slower |
| Memgraph | 162.24 ms | 59.71% slower |
| CognoDB | 217.96 ms | 70.01% slower |
| ArangoDB | 221.10 ms | 70.44% slower |

#### 2-Hop Traversal

| Database | Average latency | Relative performance |
|---|---:|---:|
| **Neo4j** | **94.64 ms** | **Best** |
| FalkorDB | 120.28 ms | 21.32% slower |
| Memgraph | 202.92 ms | 53.36% slower |
| ArangoDB | 238.82 ms | 60.37% slower |
| CognoDB | 260.45 ms | 63.66% slower |

#### 3-Hop Traversal

| Database | Average latency | Relative performance |
|---|---:|---:|
| **FalkorDB** | **157.02 ms** | **Best** |
| Neo4j | 267.36 ms | 41.27% slower |
| Memgraph | 488.22 ms | 67.84% slower |
| CognoDB | 728.09 ms | 78.43% slower |
| ArangoDB | 2,180.94 ms | 92.80% slower |

#### Indexed Lookup

| Database | Average latency | Relative performance |
|---|---:|---:|
| **Neo4j** | **111.51 ms** | **Best** |
| FalkorDB | 131.97 ms | 15.51% slower |
| ArangoDB | 235.69 ms | 52.69% slower |
| Memgraph | 239.36 ms | 53.41% slower |
| CognoDB | 287.94 ms | 61.27% slower |

#### Aggregation

| Database | Average latency | Relative performance |
|---|---:|---:|
| **Neo4j** | **63.76 ms** | **Best** |
| FalkorDB | 113.18 ms | 43.66% slower |
| Memgraph | 166.33 ms | 61.67% slower |
| ArangoDB | 218.70 ms | 70.84% slower |
| CognoDB | 230.60 ms | 72.35% slower |

### P95 Latency

P95 represents the latency at which approximately 95% of measured operations completed faster.

| Workload | CognoDB (ms) | Neo4j (ms) | Memgraph (ms) | ArangoDB (ms) | FalkorDB (ms) |
|---|---:|---:|---:|---:|---:|
| Point Lookup | 225.94 | 150.13 | 166.88 | 290.12 | 118.08 |
| 1-Hop Traversal | 223.16 | 71.62 | 166.78 | 282.99 | 121.81 |
| 2-Hop Traversal | 275.22 | 109.06 | 217.81 | 301.40 | 129.91 |
| 3-Hop Traversal | 810.12 | 320.14 | 542.65 | 3,223.45 | 177.52 |
| Indexed Lookup | 304.93 | 121.03 | 268.36 | 302.80 | 162.46 |
| Aggregation | 238.02 | 67.00 | 173.84 | 295.79 | 118.84 |

### Overall Ranking

Based on average latency across the six workloads:

1. **Neo4j** — fastest in 5 of 6 workloads.
2. **FalkorDB** — fastest for 3-hop traversal and second-fastest in the other five workloads.
3. **Memgraph** — generally middle-performing and substantially faster than CognoDB and ArangoDB for 3-hop traversal.
4. **ArangoDB** — reasonable for shallow queries but extremely slow for 3-hop traversal.
5. **CognoDB** — similar to ArangoDB on shallow workloads but slower than ArangoDB for 3-hop traversal.

### Results Analysis

All five databases completed 100 of 100 measured iterations for every workload, with zero failed operations. The comparison therefore reflects latency differences rather than different success rates.

#### Average Latency

Neo4j achieved the lowest average latency in five of the six workloads: point lookup, 1-hop traversal, 2-hop traversal, indexed lookup, and aggregation. Its average latencies were 82.79 ms, 65.37 ms, 94.64 ms, 111.51 ms, and 63.76 ms respectively. Neo4j was therefore the strongest general-purpose performer in this benchmark.

FalkorDB was the fastest database for 3-hop traversal at 157.02 ms and ranked second in the other five workloads. Its performance remained comparatively consistent as traversal depth increased, which made it the strongest option for the deeper traversal tested.

#### Tail Latency

The P95 results reinforce the average-latency findings. Neo4j had the lowest P95 latency for point lookup, 1-hop traversal, 2-hop traversal, indexed lookup, and aggregation. FalkorDB had the lowest 3-hop P95 latency at 177.52 ms, compared with 320.14 ms for Neo4j.

The largest separation occurred at three hops. FalkorDB's 157.02 ms average was approximately 13.89 times faster than ArangoDB's 2,180.94 ms average. ArangoDB's P95 latency also rose to 3,223.45 ms, indicating that the deeper traversal affected both typical and slower operations.

#### CognoDB and Other Results

CognoDB recorded average latencies of 218.89 ms, 217.95 ms, 260.45 ms, 728.09 ms, 287.94 ms, and 230.60 ms across the six workloads. It was close to ArangoDB for point lookup, 1-hop traversal, 2-hop traversal, and aggregation, but it was faster than ArangoDB for 3-hop traversal. Memgraph generally occupied the middle of the rankings and outperformed both CognoDB and ArangoDB for 3-hop traversal.

These results show that there is no single winner for every graph workload. Neo4j provided the best overall latency across most tests, while FalkorDB showed a clear advantage for deeper traversal. The findings apply to this dataset, query implementation, managed service configuration, and network environment; they should not be treated as universal rankings for all graph workloads.

### Key Finding: 3-Hop Traversal

The 3-hop traversal produced the clearest performance difference:

| Database | Average latency |
|---|---:|
| **FalkorDB** | **157.02 ms** |
| Neo4j | 267.36 ms |
| Memgraph | 488.22 ms |
| CognoDB | 728.09 ms |
| ArangoDB | 2,180.94 ms |

FalkorDB was approximately **13.89× faster than ArangoDB** for this workload.

### Benchmark Conclusion

Based on the measured workloads, Neo4j provided the best overall performance, achieving the lowest latency in five out of six tests. FalkorDB was the best-performing database for 3-hop traversal, demonstrating that workload characteristics can significantly influence graph database performance.

These results should be interpreted within the specific benchmark environment, dataset, query implementations, and network conditions used in this project.
## Final Assignment Checklist

### Database Setup

| Requirement | Status |
|---|---|
| CognoDB, Memgraph, ArangoDB, FalkorDB, and Neo4j connected | Complete |
| Same dataset loaded into all five databases | Complete |
| 7,115 nodes verified | Complete |
| 103,689 `VOTED_FOR` relationships verified | Complete |

### Database Verification

| Requirement | Status |
|---|---|
| Node and relationship counts verified | Complete |
| Point lookup verified | Complete |
| 1-hop traversal verified | Complete |
| User-type lookup verified | Complete |
| Connection tests completed | Complete |

### Benchmarking

| Database | Point Lookup | 1-Hop | 2-Hop | 3-Hop | Indexed Lookup | Aggregation |
|---|---:|---:|---:|---:|---:|---:|
| CognoDB | Complete | Complete | Complete | Complete | Complete | Complete |
| Memgraph | Complete | Complete | Complete | Complete | Complete | Complete |
| ArangoDB | Complete | Complete | Complete | Complete | Complete | Complete |
| FalkorDB | Complete | Complete | Complete | Complete | Complete | Complete |
| Neo4j | Complete | Complete | Complete | Complete | Complete | Complete |

All five databases have 100 successful iterations for every executed workload, with zero failed iterations. The benchmark uses 100 measured iterations, 30 warmup iterations, the same dataset, and the same workload definitions.

Aggregation is included in the current benchmark configuration and has results for all five databases in `results/all_results.json`.

### Results Processing

Complete outputs are generated by `scripts/compare_benchmarks.py`:

- Average, median, minimum, maximum, P50, and P95 latency data are retained in the source JSON.
- Average-latency rankings and fastest databases are written to `results/comparison/average_latency.csv`.
- P95 comparisons are written to `results/comparison/p95_latency.csv`.
- Relative performance percentages are written to `results/comparison/relative_performance.csv`.
- A Markdown comparison report is written to `results/comparison/comparison_report.md`.
- The average-latency chart is stored in `results/charts/benchmark_average_latency.png`.

### Remaining Submission Tasks

- Complete a fresh-environment reproducibility run and verify dependencies before submission.
- Expand the written report with any required introduction, experimental setup, methodology, and database-system descriptions.
- Add any additional charts required by the assignment, such as P95 latency comparisons.


### Benchmark Visualization

![Database Benchmark Comparison](results/charts/benchmark_average_latency.png)

![P95 Database Benchmark Comparison](results/charts/benchmark_p95_latency.png)