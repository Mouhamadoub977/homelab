"""Reference reconstruction of the manually validated S3 -> PostGIS script.

Runs on Ubuntu host, not in Airflow's Docker network. Uses bootstrap
credentials from local .env files; replace with service accounts before
integrating into orchestration.
"""
import json
from pathlib import Path
import boto3
import psycopg
from botocore.config import Config
from dotenv import dotenv_values

base = Path.home() / "homelab-services"
s3_env = dotenv_values(base / "silo" / ".env")
pg_env = dotenv_values(base / "postgis" / ".env")

s3_user = s3_env.get("S3_ROOT_USER")
s3_password = s3_env.get("S3_ROOT_PASSWORD")
pg_password = pg_env.get("POSTGRES_PASSWORD")
if not all((s3_user, s3_password, pg_password)):
    raise RuntimeError("Missing S3/PostgreSQL credentials")

s3 = boto3.client(
    "s3",
    endpoint_url="http://127.0.0.1:9000",
    aws_access_key_id=s3_user,
    aws_secret_access_key=s3_password,
    region_name="us-east-1",
    config=Config(s3={"addressing_style": "path"}),
)
obj = s3.get_object(Bucket="geodata-raw", Key="villes/villes.geojson")
payload = json.load(obj["Body"])
if payload.get("type") != "FeatureCollection":
    raise ValueError("Expected a GeoJSON FeatureCollection")
features = payload["features"]
print(f"EXTRACT: {len(features)} features read")

cities = []
for feature in features:
    props = feature["properties"]
    geom = feature["geometry"]
    if geom["type"] != "Point" or len(geom["coordinates"]) != 2:
        raise ValueError("Only 2D points are supported")
    lon, lat = geom["coordinates"]
    if not (-180 <= lon <= 180 and -90 <= lat <= 90):
        raise ValueError("Invalid lon/lat")
    cities.append((props["nom"], props["pays"], lon, lat))
print(f"TRANSFORM: {len(cities)} points validated")

with psycopg.connect(
    host="127.0.0.1", port=5433, dbname="geodata",
    user="geodata", password=pg_password,
) as conn:
    with conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS raw.villes (
                id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                nom TEXT NOT NULL,
                pays TEXT NOT NULL,
                geom GEOMETRY(Point,4326) NOT NULL,
                UNIQUE(nom,pays)
            )
        """)
        for nom, pays, lon, lat in cities:
            cur.execute("""
                INSERT INTO raw.villes (nom,pays,geom)
                VALUES (%s,%s,ST_SetSRID(ST_MakePoint(%s,%s),4326))
                ON CONFLICT(nom,pays)
                DO UPDATE SET geom=EXCLUDED.geom
            """, (nom, pays, lon, lat))
        cur.execute("SELECT COUNT(*) FROM raw.villes")
        count = cur.fetchone()[0]
print(f"LOAD: completed, {count} cities in PostGIS")
