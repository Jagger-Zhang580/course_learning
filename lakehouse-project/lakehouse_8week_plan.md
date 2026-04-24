# Lakehouse 8‑Week Learning Plan

A hands‑on curriculum to go from fundamentals to production‑ready lakehouse pipelines using Delta Lake, Apache Iceberg, or Hudi on Spark/Databricks/AWS/GCP.

---

## Weekly Breakdown

| Week | Topic & Goals | Hands‑On Demo |
|------|---------------|---------------|
| **1** | **Lakehouse Foundations** – concept, benefits vs. data warehouse & data lake; architecture (storage, compute, metadata). | Spin up a local Spark session; create a Delta table on disk; insert, read, and show ACID guarantees (concurrent writes). |
| **2** | **Storage Formats Deep Dive** – Parquet layout, transaction log, checkpointing, vacuum, time‑travel. | Load a CSV into a Delta table; run `DESCRIBE HISTORY`; query older version; perform `VACUUM` and observe file retention. |
| **3** | **Upserts, Merge & Change Data Flow** – `MERGE INTO`, CDC patterns, handling slowly changing dimensions. | Simulate a nightly load: stage new/updated records in a temp Delta table; use `MERGE` to upsert into a fact table; verify SCD Type 2 behavior. |
| **4** | **Schema Evolution & Enforcement** – adding/dropping columns, data type changes, schema validation. | Alter a Delta table schema (add column, rename); write data with missing/new columns; observe automatic schema merging or failure based on mode. |
| **5** | **Performance & Optimization** – Z‑Ordering, clustering, file size tuning, bloom filters, caching. | Generate a large dataset (>10M rows); apply `OPTIMIZE` and `ZORDER BY`; benchmark query latency before/after. |
| **6** | **Streaming Ingestion** – Structured Streaming with Delta Lake as sink & source; exactly‑once guarantees. | Set up a Kafka (or socket) source; write streaming aggregates to a Delta table; trigger a manual stop‑restart and verify no duplicates. |
| **7** | **BI & ML Integration** – querying lakehouse from SQL endpoints (Databricks SQL, Trino, Presto); feature engineering for MLflow. | Register a Delta table as a external table in Trino/Spark SQL; run a BI query (e.g., monthly sales); pull features into a Spark ML pipeline and log model with MLflow. |
| **8** **Production & Operations** – CI/CD for lakehouse code (dbt‑lakehouse or Delta Live Tables), monitoring (event logs, alerts), cost optimization, multi‑cloud/GitOps. | Deploy a Delta Live Table pipeline via Docker/Kubernetes; set up a webhook that posts job failures to Slack; export pipeline definition to Git and demonstrate a pull‑request update. |

---

## Suggested Tools & Environment
- **Runtime**: Docker‑based Spark (spark‑standalone) or Databricks Community Edition.
- **Storage**: Local disk or MinIO (S3‑compatible) for object storage.
- **Metadata**: Delta Lake (default) – optional labs with Apache Iceberg (`iceberg-spark-runtime`) or Hudi.
- **Streaming**: Kafka (docker‑compose) or Netcat socket source.
- **BI/ML**: Trino/Presto, Spark MLlib, MLflow, Superset/Metabase.
- **Orchestration**: Docker Compose, optionally Kubernetes or Airflow for week 8 demo.
- **Version Control**: Git repo for notebooks / SQL / DLT definitions.

---

## Resources
- **Delta Lake**: https://delta.io/ (docs, quickstart)
- **Apache Iceberg**: https://iceberg.apache.org/
- **Hudi**: https://hudi.apache.org/
- **Databricks Lakehouse**: https://www.databricks.com/product/lakehouse
- **MinIO (S3 mock)**: https://min.io/
- **Trino**: https://trino.io/
- **MLflow**: https://mlflow.org/
- **dbt‑lakehouse**: https://docs.getdbt.com/docs/building-a-dbt-project/building-with-delta-lake

---

*Follow each week’s demo, then extend it (e.g., change partition strategy, add streaming triggers, integrate with a BI tool) to solidify the concepts.* 
