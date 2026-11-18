# 08 — Delivery roadmap, gaps and risk register

## Phases

| Phase | Target | State |
|---|---|---|
| A | Ubuntu/SSH/Tailscale, repository baseline | Validated |
| B | Ansible SSH inventory and read-only audit | Validated; deeper study deferred |
| C | Docker Engine/Compose, PostGIS | Validated |
| D | S3-compatible storage, manual geospatial ETL | Validated |
| E | Airflow and a working ETL DAG | Airflow UI online; DAG registration **blocked** |
| F | Spark/PySpark + Parquet + Iceberg + Trino + dbt | Planned |
| G | Kafka + CDC/Debezium + streaming | Planned |
| H | K3s/Kubernetes, Helm, GitOps/Argo CD, Ansible roles | Planned |
| I | Monitoring, recovery, infrastructure hardening | Incomplete |
| J | Optional Oracle / AWS RDS / Snowflake integrations | Planned; cloud costs to review |

**Target architecture:** sources (API/SIG files/databases/CDC) → Kafka or batch ingestion → S3-compatible raw/bronze → Spark silver → Iceberg/Trino/dbt gold → PostGIS/data marts/Snowflake/RDS → GIS/API/dashboards. Airflow orchestrates batch workflows across layers; it is not a streaming broker.

## Resource constraints

GMKtec M8, a single Ubuntu host, ~11.9 GiB usable RAM and 98 GiB root logical volume. Observed available RAM ~10 GiB and root free ~83 GiB before Airflow. Large Kafka/Spark/Airflow/Kubernetes stacks should not run unbounded simultaneously. Root LV occupies only part of the available VG; storage extension needs an explicit backup and space plan.

## Outstanding safeguards

1. **Rotate Airflow admin password** after accidental exposure in chat; do not disclose replacement.
2. UFW currently inactive. Rules and a rollback rehearsal were prepared; enable only with physical console/recovery access and test both LAN and Tailscale.
3. Create S3 and PostgreSQL service accounts for workloads instead of using root/superuser.
4. Build tested PostgreSQL logical/physical backups and S3 object backup/recovery; Docker volumes alone are insufficient.
5. Check pending OS updates and schedule reboot with SSH/Tailscale recovery plan.
6. Protect web interfaces with loopback binding and SSH tunnels; reconsider architecture before any LAN/public exposure.
7. Add versioned, reviewed configuration and tests; separate `.env` from committed examples.
8. Diagnose Airflow DAG discovery, then implement the ETL as a proper Airflow workflow.
9. Consider replacing standalone/SQLite with a dedicated Airflow metadata database when scaling.

## Documentation integrity

Only claim operations explicitly confirmed by terminal output. Repo examples are **representative**, not automatically exported from the running server. Never use GitHub as a backup for operational secrets or live databases.
