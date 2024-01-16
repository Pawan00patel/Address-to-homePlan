import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from prettytable import PrettyTable

# def scrape_image_url(property_url):
    # Add code to scrape image URL from the property page
    # pass

def get_text_or_na(element, selector):
    try:
        return element.select_one(selector).get_text(strip=True)
    except AttributeError:
        return "N/A"

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust this sleep time based on your observations

def scrape_magicbricks_data(url, max_items=100):
    # Set up the webdriver for scrolling
    driver = webdriver.Chrome()
    driver.get(url)

    # Scroll down until the desired number of items are loaded
    while len(driver.find_elements(By.CSS_SELECTOR, '.mb-srp__card')) < max_items:
        scroll_down(driver)

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Close the webdriver
    driver.quit()

    # Extract property details
    property_listings = soup.select('.mb-srp__card')

    scraped_data = set()  # Use a set to store unique data

    # Create a PrettyTable instance
    table = PrettyTable()
    table.field_names = ["Serial No.", "Title", "City", "Price", "Area"]

    serial_number = 1

    for listing in property_listings:
        # Use try-except block to handle potential NoneType
        try:
            title_highlight = get_text_or_na(listing, '.mb-srp_card_developer--name--highlight')
            title_society = get_text_or_na(listing, '.mb-srp_card_society')
            title = title_highlight if title_highlight != "N/A" else title_society
        except AttributeError:
            title = "N/A"

        city = get_text_or_na(listing, '.mb-srp__card--title')
        price = get_text_or_na(listing, '.mb-srp_card_price--amount')
        area = get_text_or_na(listing, '.mb-srp_card_summary--value')
        # image_url = scrape_image_url(listing.select_one('.mb-srp__link')['href'])

        # Check for duplicate data
        if (title, city, price, area) not in scraped_data:
            scraped_data.add((title, city, price, area))
            # Add data to PrettyTable with serial number
            table.add_row([serial_number, title, city, price, area])
            serial_number += 1

            if serial_number >= max_items:
                break  # Stop when reaching the desired number of items

    # Print the table
    print(table)

if __name__ == "__main__":
    magicbricks_url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore"
    scrape_magicbricks_data(magicbricks_url, max_items=500)  # Set max_items to the desired number