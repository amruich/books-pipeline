from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


with DAG(
    dag_id='cbr_dbt_daily',
    default_args={'owner': 'amruich', 'retries': 1},
    description='Запуск парсера книг',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['books', 'etl'],
) as dag:

    task_run_fetch = BashOperator(
        task_id='run_fetch_script',
        bash_command='cd /opt/airflow/scripts && python fetch_cbr.py',
    )

    # запуск dbt
    task_run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /opt/airflow/books_dbt && dbt run --profiles-dir .',
    )

    task_run_fetch >> task_run_dbt
    