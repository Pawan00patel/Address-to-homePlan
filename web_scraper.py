import requests
from bs4 import BeautifulSoup
import sqlite3

def insert_data_into_database(data):
    try:
        conn = sqlite3.connect('property_data.db')
        cursor = conn.cursor()

        for item in data:
            cursor.execute('''
                INSERT INTO properties (title, price, area, description)
                VALUES (?, ?, ?, ?)
            ''', item)

        conn.commit()
        conn.close()

    except Exception as e:
        print(f"An error occurred while inserting data into the database: {str(e)}")

def scrape_property_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        price_elements = soup.find_all(class_='mb-srp__card__price--amount')
        prices = [element.get_text(strip=True) for element in price_elements]

        title_elements = soup.find_all(class_='mb-srp__card--title')
        titles = [element.get_text(strip=True) for element in title_elements]

        area_elements = soup.find_all('div', class_='mb-srp__card__summary--value')
        areas = [element.find(string=True, recursive=False).strip() for element in area_elements if 'sqft' in element.text]

        description_elements = soup.find_all(class_='two-line-truncated')
        descriptions = [element.get_text(strip=True)[:100] + '...' for element in description_elements]

        data = list(zip(titles, prices, areas, descriptions))
        return data

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return []

# Example usage with the provided URL:
url = 'https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=50-Lacs&BudgetMax=1-Crores&cityName=bangalore'
property_data = scrape_property_data(url)
insert_data_into_database(property_data)
