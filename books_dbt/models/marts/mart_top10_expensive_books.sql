select 
    title,
    price,
    rating,
    category
from {{ ref('stg_books') }}
order by price desc
limit 10