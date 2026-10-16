import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import psycopg2
from psycopg2.extras import execute_values

def parse_books():
    url = 'https://books.toscrape.com/catalogue/page-1.html'
    books = []
    page_count = 0
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    while url and page_count < 2:
        page_count += 1 
        print(f'Страница: {page_count}, книг собрано: {len(books)}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find_all("article", class_="product_pod")

        for card in cards:
            href = card.find('h3').find('a')['href']
            book_url = urljoin(url, href)

            response = requests.get(book_url)
            book = BeautifulSoup(response.text, 'lxml')
            
            title = book.find('h1').text
            price = book.find(class_='price_color').text.replace('Â£', '').replace('£', '')
            rating = rating_map[book.find(class_='star-rating')['class'][1]]
            in_stock_status = book.find(class_='instock availability').text.strip()
            in_stock = 'In stock' in in_stock_status
            breadcrumb = book.find('ul', class_='breadcrumb')
            items = breadcrumb.find_all('li')
            category = items[2].text.strip()
            upc = book.find('td').text
            books.append({
                'title': title,
                'price': price,
                'rating': rating,
                'in_stock': in_stock,
                'category': category,
                'upc': upc
            })
            next_page = soup.find('li', class_='next')

            if next_page:
                href = next_page.find('a')['href']
                url = urljoin(url, href)
            else:
                url = None
            time.sleep(0.5)
    return books

def load_to_db(books):
    conn = psycopg2.connect(
        dbname='appdb',
        user='postgres',
        password='postgres',
        host='localhost',
        port=5432
    )
    cursor = conn.cursor()

    cursor.execute('' \
        'create table if not exists raw_books (' \
        'upc text primary key, ' \
        'title text, ' \
        'price numeric, ' \
        'rating smallint, ' \
        'in_stock boolean, ' \
        'category text,' \
        'parsed_at timestamp default now())'
    )
    values = [(book['upc'], book['title'], book['price'], book['rating'], book['in_stock'], book['category']) for book in books]
    
    execute_values(cursor, 
                   'insert into raw_books (upc, title, price, rating, in_stock, category) ' \
                    'VALUES %s on conflict (upc) do nothing', 
                    values)

    conn.commit()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    books = parse_books()
    load_to_db(books)