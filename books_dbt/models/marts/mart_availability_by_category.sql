select 
    count(case when in_stock is True then 1 end) as in_stock,
    count(case when in_stock is False then 1 end) as out_of_stock,
    category
from {{ ref('stg_books') }}
group by category
