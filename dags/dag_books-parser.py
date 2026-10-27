from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id='books_parcer_weekly',
    default_args={'owner': 'amruich', 'retries': 1},
    description='Запуск парсера книг',
    schedule_interval='@weekly',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['books', 'etl'],
) as dag:

    task_run_parser = BashOperator(
        task_id='run_parser_script',
        bash_command='cd /opt/airflow/scripts && python parse_books.py',
    )

    task_run_parser
    