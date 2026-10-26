select 
    rating,
    round(avg(price), 2) as avg_price,
    count(upc) as count_books
from {{ ref('stg_books') }}
group by rating
