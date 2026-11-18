# 05 — Docker Engine, Compose and spatial database

**Validated on Ubuntu Server 26.04.1 LTS.** Docker Engine 29.10.0 and Docker Compose v5.8.0 were installed using Docker's signed Ubuntu APT repository (`resolute`). `docker-compose` (legacy hyphenated form) was not installed; use `docker compose`.

## First checks

```bash
sudo systemctl is-active docker
sudo docker run --rm hello-world
sudo docker ps
```

The daemon reported `active` and `hello-world` succeeded. Unprivileged `docker ps` returned socket permission denied; `sudo docker` is used deliberately. The `docker` group carries root-equivalent risk.

## PostGIS service

Live directory on Ubuntu: `~/homelab-services/postgis`.

- Image used: `postgis/postgis:17-3.7`
- Container: `postgis-postgis-1`
- Port: `127.0.0.1:5433:5432` (host loopback → container 5432)
- Database/user: `geodata`
- Named volume: `postgis_postgis_data`
- Password comes from local `.env`; **not versioned**
- Result: `PostGIS_Version()` reported `3.7 USE_GEOS=1 USE_PROJ=1 USE_STATS=1`

An early launch loop was caused by a **zero-byte `.env`**: PostgreSQL declined to initialize without `POSTGRES_PASSWORD`. The secret was regenerated, Compose configuration checked, and container force-recreated **without deleting the named volume**.

The SQL exercise created `public.villes` (Paris, Lille, Dakar), using `ST_SetSRID(ST_MakePoint(lon, lat),4326)` and read with `ST_AsText(geom)`. A `docker compose restart postgis` retained all three rows.

Useful commands, run from the project directory:
```bash
sudo docker compose config --quiet
sudo docker compose ps
sudo docker compose logs --tail=50 postgis
sudo docker compose exec -T postgis psql -U geodata -d geodata -c "SELECT PostGIS_Version();"
sudo docker compose exec -T postgis psql -U geodata -d geodata -c "SELECT nom, ST_AsText(geom) FROM public.villes;"
```

`-T` disables pseudo-TTY allocation in **Compose exec** (useful in scripts). If the shell prints `>`, a quote or continuation may still be open; `Ctrl+C` cancels incomplete input.

## Persistence and safety

A named volume survives ordinary restart/recreation when retained. It does **not** replace off-host backups and recovery tests. Never run `docker compose down -v` on stateful workloads without an explicit data-loss decision. Bind sensitive application ports to loopback; Docker port publishing has firewall implications.

See `examples/postgis.compose.yaml` for a reviewed **reference**, not a copy of the live server file.
