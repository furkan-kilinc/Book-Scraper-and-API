from sqlalchemy.orm import Session
from database import SessionLocal
from models import Book
import requests
from bs4 import BeautifulSoup

numbers_dict = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

def scrape_books():
    books = []
    
    for page in range(1, 6):
        url = f'https://books.toscrape.com/catalogue/page-{page}.html'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        book_elements = soup.find_all('article', {'class':'product_pod'})
        
        for book in book_elements:
            url_name = book.find('h3').a['href']
            book_url = f'https://books.toscrape.com/catalogue/{url_name}'
            response = requests.get(book_url)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            name = soup.find('h1').text
            price = soup.find('p', {'class':'price_color'}).text
            category = soup.find('ul', {'class':'breadcrumb'}).find_all('a')[2].text
            stars_element = soup.find('p', {'class':'star-rating'})
            stars = numbers_dict[stars_element['class'][1]]
            upc = soup.find('th', string='UPC').find_next_sibling().text
            availability = soup.find('th', string='Availability').find_next_sibling().text
            availability_number = int(availability.split('(')[1][0:2])  
            image_link = 'https://books.toscrape.com' + soup.find('div', {'class':'thumbnail'}).find('img')['src']
            
            books.append({
                'name': name,
                'price': price,
                'category': category,
                'stars': stars,
                'upc': upc,
                'availability': availability,
                'in_stock': availability_number,
                'image_link': image_link
            })
    
    return books

def save_books_to_db():
    db: Session = SessionLocal()  
    books = scrape_books()
    
    for book in books:
        db_book = Book(
            name=book["name"],
            price=book["price"],
            category=book["category"],
            stars=book["stars"],
            upc=book["upc"],
            availability=book["availability"],
            in_stock=book["in_stock"],
            image_link=book["image_link"]
        )
        db.add(db_book)
    
    db.commit()  
    db.close()   


save_books_to_db()
