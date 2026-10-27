import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import logging

from db_utils import load_data

logging.basicConfig(level=logging.INFO)

def parse_books():
    url = 'https://books.toscrape.com/catalogue/page-1.html'
    books = []
    page_count = 0
    rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    
    while url and page_count < 2: 
        page_count += 1 
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')

        cards = soup.find_all("article", class_="product_pod")

        for card in cards:
            href = card.find('h3').find('a')['href']
            book_url = urljoin(url, href)

            book_response = requests.get(book_url)
            book = BeautifulSoup(book_response.text, 'lxml')
            
            title = book.find('h1').text
            price = book.find(class_='price_color').text.replace('Â£', '').replace('£', '')
            rating = rating_map[book.find(class_='star-rating')['class'][1]]
            in_stock_status = book.find(class_='instock availability').text.strip()
            in_stock = 'In stock' in in_stock_status
            breadcrumb = book.find('ul', class_='breadcrumb')
            category = breadcrumb.find_all('li')[2].text.strip()
            upc = book.find('td').text
            
            books.append((upc, title, price, rating, in_stock, category))
            time.sleep(0.1)
        logging.info(f'Страница: {page_count}, книг собрано: {len(books)}')
        next_page = soup.find('li', class_='next')
        if next_page:
            href = next_page.find('a')['href']
            url = urljoin(url, href)
        else:
            url = None
            
    return books

def load_to_db(books):
    load_data(
        table_name='raw_books',
        columns=['upc', 'title', 'price', 'rating', 'in_stock', 'category'],
        data=books,
        conflict_target='upc'
    )

if __name__ == "__main__":
    parsed_books = parse_books()
    load_to_db(parsed_books)