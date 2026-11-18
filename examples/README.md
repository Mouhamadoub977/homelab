# Reference configurations (not automatic snapshots)

These files document the **observed functional designs**. They were reconstructed from the terminal session, not copied verbatim from the live Ubuntu filesystem. Update differences deliberately, test with `docker compose config --quiet`, and never blindly overwrite on-host services.

Files:
- `postgis.compose.yaml`: PostgreSQL 17 + PostGIS 3.7, loopback port, named volume
- `silo.compose.yaml`: PGSTY Silo, S3 and console bound to loopback
- `airflow.compose.yaml`: standalone development Airflow 3.3.1, restricted task parallelism
- `geodata_pipeline_demo.py`: **unverified by Airflow** demo DAG; syntax verified on the Ubuntu host
- `s3_to_postgis.py`: reconstructed ETL; live on-host script ran successfully twice

Secrets belong in host-local `.env` files (never commit), with dedicated limited-permission service accounts for future production-style workflows. The live server's Compose files were not modified by this GitHub documentation commit.
