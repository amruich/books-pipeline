select 
    upc, 
    title, 
    replace(price, 'Â£', '')::numeric as price,
    case rating
        when 'One' then 1
        when 'Two' then 2
        when 'Three' then 3
        when 'Four' then 4
        when 'Five' then 5
    end as rating,
    in_stock like 'In stock%' as in_stock,
    regexp_replace(in_stock, '\D', '', 'g') as stock_count,
    category
from raw_books
where price is not null