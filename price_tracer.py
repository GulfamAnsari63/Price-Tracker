import requests
from bs4 import BeautifulSoup
from Email_alert import alert_system
from threading import Timer
import logging

logging.basicConfig(level=logging.INFO)

class PriceChecker:
    def __init__(self, url, set_price):
        self.url = url
        self.set_price = set_price

    def get_page_content(self):
        try:
            page = requests.get(self.url, headers=headers)
            page.raise_for_status()
            return page.content
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page content: {e}")
            return None

    def extract_product_info(self, content):
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.select_one('.a-size-large.product-title-word-break').get_text().strip()
        price = soup.select_one('.a-price-whole').get_text()

        product_price = ''.join([letter for letter in price if letter.isnumeric() or letter == '.'])
        return title, float(product_price)

    def check_price(self):
        content = self.get_page_content()
        if content:
            title, product_price = self.extract_product_info(content)
            logging.info(f"Product: {title}, Price: {product_price}")

            if product_price <= self.set_price:
                alert_system(title, self.url)
                logging.info('Alert sent!')
            else:
                logging.info('Alert not sent.')

            Timer(60, self.check_price).start()

if __name__ == "__main__":
    URL = "https://www.amazon.in/God-Ragnarok-Launch-Game-PlayStation/dp/B0B68LNSRL/ref=sr_1_1?crid=3RI2K9FGZKPIK&keywords=god+of+war+ragnarok&qid=1668832831&qu=eyJxc2MiOiIyLjQ1IiwicXNhIjoiMS44MCIsInFzcCI6IjAuOTYifQ%3D%3D&s=videogames&sprefix=god+of+war%2Cvideogames%2C788&sr=1-1"
    set_price = 1000

    checker = PriceChecker(URL, set_price)
    checker.check_price()
