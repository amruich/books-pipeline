from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='books_pipeline_daily',
    default_args={'owner': 'amruich', 'retries': 1},
    description='Запуск парсера книг',
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['books', 'etl'],
) as dag:

    # запуск парсера
    task_run_parser = BashOperator(
        task_id='run_parser_script',
        bash_command='cd /opt/airflow/scripts && python parse_books.py',
    )

    # запуск dbt
    task_run_dbt = BashOperator(
    task_id='run_dbt_models',
    bash_command='cd /opt/airflow/books_dbt && dbt run --profiles-dir .',
    )

    task_run_parser >> task_run_dbt
    