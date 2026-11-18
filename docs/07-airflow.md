# 07 — Airflow 3: standalone deployment and DAG discovery blocker

**State observed 2026-11-18:** Airflow Web was opened over SSH tunnel and login succeeded. The demonstration DAG is **not yet registered**; CLI returned `No data found`. Do not mark task execution as validated.

## Deployment

- Ubuntu path: `~/homelab-services/airflow`
- Image: `apache/airflow:3.3.1`
- Docker Compose standalone, metadata managed by standalone mode (SQLite for this lab)
- Port: `127.0.0.1:8080:8080`
- `AIRFLOW__CORE__LOAD_EXAMPLES=false`
- `AIRFLOW__CORE__PARALLELISM=2`
- Bind mounts: `./data:/opt/airflow`, `./dags:/opt/airflow/dags` in observed deployment
- Measured usage after restart: approximately 894 MiB, 27 PIDs, 4.95% CPU snapshot
- Auth manager: `SimpleAuthManager`

SSH tunnel from Mac:
```bash
ssh -N -L 8080:127.0.0.1:8080 homelab
```
Then open `http://localhost:8080` on the Mac. Never publish the console directly.

## Demonstration DAG

File `dags/geodata_pipeline_demo.py` was created on Ubuntu with Airflow SDK `@dag` and three `@task` functions: extract → transform → load, using a simple list of city names. Syntax check passed on Ubuntu. However:
```text
airflow dags list
No data found
```

The issue is **unresolved**. Diagnostic sequence from `~/homelab-services/airflow`:
```bash
sudo docker compose exec -T airflow ls -l /opt/airflow/dags/
sudo docker compose exec -T airflow airflow config get-value core dags_folder
sudo docker compose exec -T airflow airflow dags list-import-errors
sudo docker compose logs --tail=80 airflow
```
Check bind mount, actual DAG path and parse errors before modifying Python. `py_compile` on the host alone does not validate Airflow imports inside the container.

## Critical operational actions

- **Rotate the Airflow admin password:** an initial admin credential was pasted into chat. Rotation was recommended but **not confirmed**. Never commit the generated `simple_auth_manager_passwords.json.generated` file or echo its contents into public logs.
- SimpleAuthManager + standalone are learning-only choices, not production identity, high availability or metadata architecture.
- Avoid keeping both `./data:/opt/airflow` and nested `./dags:/opt/airflow/dags` long term; evaluate narrower mounts and separate metadata persistence during refactoring.
- Airflow container `127.0.0.1` is not the Ubuntu host loopback. Cross-container Silo/PostGIS access requires deliberate Docker networking and application credentials.
- The Python ETL has **not** yet run under Airflow.

See `examples/geodata_pipeline_demo.py` for a reference DAG corresponding to the tutorial.
