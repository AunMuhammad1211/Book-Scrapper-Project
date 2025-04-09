import requests
import pandas as pd
from bs4 import BeautifulSoup

url = 'https://books.toscrape.com/'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/122.0.0.0 Safari/537.36"
}

def get_response():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        else:
            print(f"Failed to access page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Access Denied! This occurred due to: {e}")
        return None

soup = get_response()

if soup:
    books = soup.find_all('article', class_='product_pod')

    map_rating = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    book_data = []

    for book in books:
        title = book.h3.a['title']
        price = book.find('p', class_='price_color').text
        rating_class = book.find('p', class_='star-rating')['class'][1]
        rating = map_rating.get(rating_class, 0)
        stock = book.find('p', class_='instock availability').text.strip()

        book_data.append({
            'Title': title,
            'Price': price,
            'Rating': rating,
            'Stock Availability': stock
        })

    df = pd.DataFrame(book_data)
    df.to_csv('Books_detail_Webscrapper.csv', index=False, encoding='utf-8-sig')
    print("CSV is created successfully!")



