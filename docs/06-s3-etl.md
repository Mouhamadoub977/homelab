# 06 — S3-compatible object storage and first geospatial ETL

**Validated 2026-11-18.** The lab uses **PGSTY Silo**, an S3-compatible fork of MinIO, not the old archived MinIO Community image.

## Silo deployment

- Ubuntu project: `~/homelab-services/silo`
- Image tested: `docker.io/pgsty/silo:RELEASE.2026-11-09T00-00-00Z`
- Loopback-only S3 API and console ports: `9000` and `9001`
- Volume: `silo_silo_data`
- Health endpoint `http://127.0.0.1:9000/minio/health/live`: **HTTP 200**
- `mcli` client available in image (same release).

The bucket `geodata-raw` was created. A 623-byte GeoJSON with Paris, Lille, Dakar (Point EPSG:4326) was uploaded at `villes/villes.geojson` and read back:
```bash
cd ~/homelab-services/silo
sudo docker compose exec -T silo mcli ls local/geodata-raw/villes/
sudo docker compose exec -T silo mcli cat local/geodata-raw/villes/villes.geojson
```

The `local` alias was configured **inside the live container** with its environment credentials. An alias configured in a different container may not exist. Don't publish admin credentials or their `.env` file.

## Python ETL

Live directory: `~/homelab-services/pipelines` (separate from Docker Compose projects).

Python 3.14.4 virtualenv (needed `python3.14-venv`), dependencies `boto3`, `psycopg[binary]`, `python-dotenv`. These imports passed.

Script `s3_to_postgis.py` was created and manually executed twice. Each run reported:
```text
EXTRACT : 3 entités lues
TRANSFORM : 3 points validés
LOAD : terminé, 3 villes dans PostGIS
```

SQL subsequently confirmed `raw.villes` contains three spatial features, with `nom`, `pays` and `geom`. `ON CONFLICT (nom, pays) DO UPDATE` prevents duplicate rows in repeated runs for this dataset; unchanged rows may still be updated.

The script reads local `.env` secrets from the two service directories and currently uses high-privilege accounts. **Before Airflow integration**, replace those with dedicated least-privilege credentials and adapt endpoints from host `127.0.0.1` to service-to-service networking.

The on-host ETL is not automatically checked into this repository; `examples/s3_to_postgis.py` is a reviewed reconstruction from the tested logic.
