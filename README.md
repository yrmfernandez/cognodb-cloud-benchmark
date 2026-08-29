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
| Workloads | 5 |
| Failed iterations | 0 |

### Workloads

The following workloads were executed against each database:

1. **Point Lookup** — retrieves a single user by `user_id`.
2. **1-Hop Traversal** — retrieves users directly connected to the starting user.
3. **2-Hop Traversal** — retrieves users reachable through exactly two relationships.
4. **3-Hop Traversal** — retrieves users reachable through exactly three relationships.
5. **Indexed Lookup** — retrieves users matching a specific `user_type` value using the configured index.

### Average Latency Results

Lower latency indicates better performance.

| Workload | CognoDB (ms) | Neo4j (ms) | Memgraph (ms) | ArangoDB (ms) | FalkorDB (ms) | Fastest |
|---|---:|---:|---:|---:|---:|---|
| Point Lookup | 220.82 | **70.77** | 169.22 | 217.85 | 113.35 | **Neo4j** |
| 1-Hop Traversal | 221.21 | **75.02** | 164.53 | 216.74 | 117.38 | **Neo4j** |
| 2-Hop Traversal | 259.67 | **98.24** | 198.09 | 254.70 | 122.60 | **Neo4j** |
| 3-Hop Traversal | 775.37 | 332.81 | 480.29 | 2065.94 | **156.46** | **FalkorDB** |
| Indexed Lookup | 285.76 | **114.56** | 226.12 | 229.32 | 131.80 | **Neo4j** |

### Performance Advantage

The following shows how much faster the best-performing database was compared with the second-fastest database for each workload.

| Workload | Fastest | Second Fastest | Advantage |
|---|---|---|---:|
| Point Lookup | Neo4j | FalkorDB | **37.6%** |
| 1-Hop Traversal | Neo4j | FalkorDB | **36.0%** |
| 2-Hop Traversal | Neo4j | FalkorDB | **19.9%** |
| 3-Hop Traversal | FalkorDB | Neo4j | **53.0%** |
| Indexed Lookup | Neo4j | FalkorDB | **13.1%** |

Percentage advantage is calculated as:

```text
((second-fastest latency - fastest latency) / second-fastest latency) × 100
```

### P95 Latency

P95 represents the latency at which approximately 95% of measured operations completed faster.

| Workload | CognoDB (ms) | Neo4j (ms) | Memgraph (ms) | ArangoDB (ms) | FalkorDB (ms) |
|---|---:|---:|---:|---:|---:|
| Point Lookup | 244.55 | 98.73 | 191.78 | 290.47 | 119.54 |
| 1-Hop Traversal | 231.03 | 115.54 | 173.24 | 282.40 | 131.44 |
| 2-Hop Traversal | 270.54 | 119.91 | 207.26 | 305.01 | 129.11 |
| 3-Hop Traversal | 937.43 | 502.12 | 516.91 | 2,362.40 | 165.59 |
| Indexed Lookup | 312.66 | 124.86 | 243.95 | 292.57 | 145.62 |

### Results Analysis

The benchmark shows that Neo4j achieved the lowest average latency in four of the five workloads: point lookup, 1-hop traversal, 2-hop traversal, and indexed lookup.

Neo4j recorded an average point lookup latency of 70.77 ms, making it the fastest database for single-node retrieval. It also performed best for 1-hop and 2-hop traversals, with average latencies of 75.02 ms and 98.24 ms respectively.

FalkorDB performed best for the 3-hop traversal workload, recording an average latency of 156.46 ms. This was approximately 53.0% faster than the second-fastest database, Neo4j, which recorded 332.81 ms.

ArangoDB showed a significant increase in latency for the 3-hop traversal workload, reaching an average of 2,065.94 ms. This was substantially higher than the other databases tested.

CognoDB recorded average latencies of 220.82 ms, 221.21 ms, 259.67 ms, 775.37 ms, and 285.76 ms across the five workloads. In this benchmark configuration, its performance was generally slower than Neo4j and FalkorDB.

Overall, the results demonstrate that database performance varies depending on the workload. Neo4j provided the strongest overall performance across most workloads, while FalkorDB demonstrated particularly strong performance for deeper graph traversal.

### Benchmark Conclusion

Based on the measured workloads, Neo4j provided the best overall performance, achieving the lowest latency in four out of five tests. FalkorDB was the best-performing database for 3-hop traversal, demonstrating that workload characteristics can significantly influence graph database performance.

These results should be interpreted within the specific benchmark environment, dataset, query implementations, and network conditions used in this project.


### Benchmark Visualization

![Database Benchmark Comparison](results/charts/benchmark_comparison.png)