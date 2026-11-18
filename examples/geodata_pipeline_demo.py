"""Learning-only DAG: not yet discovered by the live Airflow installation."""
from datetime import datetime
from airflow.sdk import dag, task

@dag(
    dag_id="geodata_pipeline_demo",
    start_date=datetime(2026, 11, 1),
    schedule=None,
    catchup=False,
    tags=["homelab", "geodata"],
)
def geodata_pipeline():
    @task
    def extract():
        print("EXTRACT: reading cities")
        return ["Paris", "Lille", "Dakar"]

    @task
    def transform(cities):
        valid_cities = [city for city in cities if city]
        print(f"TRANSFORM: {len(valid_cities)} validated")
        return valid_cities

    @task
    def load(cities):
        print(f"LOAD: {len(cities)} processed")
        return len(cities)

    load(transform(extract()))

geodata_pipeline()
