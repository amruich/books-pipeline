select 
    title,
    rating,
    price * c.value as price_rub,
    category
from {{ ref('stg_books') }}
join raw_cbr_currency c
    on c.rate_date = (select max(rate_date) from raw_cbr_currency) 
    and c.char_code = 'GBP'