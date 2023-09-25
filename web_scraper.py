# web_scraper.py
import requests
from bs4 import BeautifulSoup

def scrape_property_data(city):
    url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?cityName={city}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape property data here

        # Example: Extracting property titles
        title_elements = soup.find_all(class_='mb-srp__card--title')
        titles = [element.get_text(strip=True) for element in title_elements]

        # Example: Extracting property prices
        price_elements = soup.find_all(class_='mb-srp__card__price--amount')
        prices = [element.get_text(strip=True) for element in price_elements]

        # Example: Extracting property areas
        area_elements = soup.find_all('div', class_='mb-srp__card__summary--value')
        areas = [element.find(string=True, recursive=False).strip() for element in area_elements if 'sqft' in element.text]

        # Example: Extracting property descriptions
        description_elements = soup.find_all(class_='two-line-truncated')
        descriptions = [element.get_text(strip=True)[:100] + '...' for element in description_elements]

        data = []
        for title, price, area, description in zip(titles, prices, areas, descriptions):
            data.append({"title": title, "price": price, "area": area, "description": description})

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return []
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return []
