import requests
from bs4 import BeautifulSoup
import mysql.connector

# Replace these with your MySQL database credentials
DB_HOST = "your_db_host"
DB_USER = "your_db_user"
DB_PASS = "your_db_password"
DB_NAME = "your_db_name"

# Replace this with the URL of the website you want to scrape
URL_TO_SCRAPE = "https://example.com/products"

# Function to scrape data from the website
def scrape_website():
    response = requests.get(URL_TO_SCRAPE)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        products = soup.find_all('div', class_='product')
        scraped_data = []

        for product in products:
            sku = product.find('span', class_='sku').text.strip()
            price = product.find('span', class_='price').text.strip()
            description = product.find('h2').text.strip()
            web_link = product.find('a')['href'].strip()

            # Append the scraped data to the list
            scraped_data.append((sku, price, description, web_link))

        return scraped_data
    else:
        print("Failed to fetch data from the website.")
        return []

# Function to insert data into the MySQL table
def insert_into_mysql(data):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
        )
        cursor = connection.cursor()

        insert_query = "INSERT INTO products (sku, price, description, web_link) VALUES (%s, %s, %s, %s)"
        cursor.executemany(insert_query, data)
        connection.commit()

        print(f"{len(data)} records inserted into the MySQL table.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    scraped_data = scrape_website()
    if scraped_data:
        insert_into_mysql(scraped_data)
