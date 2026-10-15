import requests 
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# get-запрос к сайту
url = 'https://books.toscrape.com/catalogue/page-1.html'
books = []
page_count = 0
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
        rating = book.find(class_='star-rating')['class'][1]
        in_stock = book.find(class_='instock availability').text.strip()
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

print(books[0])