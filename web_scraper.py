# web_scraper.py
import requests
from bs4 import BeautifulSoup

<<<<<<< HEAD
def scrape_property_data(city):
    url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?cityName={city}"
=======
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
>>>>>>> 138456523de7f04270de0a721299d1ef050db8e6
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape property data here

        # Example: Extracting property titles
        title_elements = soup.find_all(class_='mb-srp__card--title')
        titles = [element.get_text(strip=True) for element in title_elements]

<<<<<<< HEAD
        # Example: Extracting property prices
        price_elements = soup.find_all(class_='mb-srp__card__price--amount')
        prices = [element.get_text(strip=True) for element in price_elements]
=======
        area_elements = soup.find_all('div', class_='mb-srp__card__summary--value')
        areas = [element.find(string=True, recursive=False).strip() for element in area_elements if 'sqft' in element.text]
>>>>>>> 138456523de7f04270de0a721299d1ef050db8e6

        # Example: Extracting property areas
        area_elements = soup.find_all('div', class_='mb-srp__card__summary--value')
        areas = [element.find(string=True, recursive=False).strip() for element in area_elements if 'sqft' in element.text]

        # Example: Extracting property descriptions
        description_elements = soup.find_all(class_='two-line-truncated')
        descriptions = [element.get_text(strip=True)[:100] + '...' for element in description_elements]

        data = list(zip(titles, prices, areas, descriptions))
        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return []
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []
<<<<<<< HEAD
=======

# Example usage with the provided URL:
url = 'https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=50-Lacs&BudgetMax=1-Crores&cityName=bangalore'
property_data = scrape_property_data(url)
insert_data_into_database(property_data)
>>>>>>> 138456523de7f04270de0a721299d1ef050db8e6
