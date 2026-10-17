Пайплайн книг 

1. Парсер
Данные собираются из https://books.toscrape.com/index.html (1000 книг - 50 страниц по 20 книг)
Для каждой книги: 
    title — название
    price — цена
    rating — рейтинг
    in_stock — есть ли в наличии
    category — категория
    upc — уникальный код товара

2. Загрузка в PostgreSQL
Создана таблица raw_books в PostgreSQL
Добавлена функция load_to_postgres(books), которая вставляет данные, обеспечена идемпотентность

3. Трансформация (dbt)
Созданы модели: 
    stg_books - очистка полей: цена, рейтинг, in_stock
    mart_avg_price_by_rating - средняя цена по рейтингу
    mart_top_expensive - топ-10 дорогих книг
    mart_stock_by_category - сколько книг в наличии по категориям
