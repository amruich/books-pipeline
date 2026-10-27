import psycopg2
from psycopg2.extras import execute_values
import logging


def load_data(table_name, columns, data, conflict_target=None):
    if not data:
        logging.warning(f"Нет данных для загрузки в таблицу {table_name}")
        return

    cols_str = ', '.join(columns)
    query = f"INSERT INTO {table_name} ({cols_str}) VALUES %s"
    
    if conflict_target:
        query += f" ON CONFLICT ({conflict_target}) DO NOTHING"
    print(query)
    conn = None
    try:
        conn = psycopg2.connect( 
            dbname="appdb",
            user="postgres",
            password="postgres",
            host="postgres",
            port=5432)
        cursor = conn.cursor()
        
        execute_values(cursor, query, data)
        
        conn.commit()
        logging.info(f"Успешно загружено {len(data)} строк в {table_name}")
        
    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Ошибка при загрузке в {table_name}: {e}")
        raise
    finally:
        if conn:
            conn.close()