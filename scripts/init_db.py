import psycopg2

conn = psycopg2.connect(
        dbname='appdb',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
cursor = conn.cursor()

cursor.execute(""" 
    create table if not exists raw_books (
    upc text primary key,
    title text,
    price text,
    rating text,
    in_stock text,
    category text,
    parsed_at timestamp default now()
    )
""")

cursor.execute(""" \
    create table if not exists raw_cbr_currency ( 
    rate_date date,
    char_code text, 
    nominal int,
    name text, 
    value numeric,
    parsed_at timestamp default now(),
    primary key (char_code, rate_date)
    )
""")

conn.commit()

cursor.close()
conn.close()