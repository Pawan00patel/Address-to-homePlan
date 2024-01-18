
from prettytable import PrettyTable
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



def get_text_or_na(element, selector):
    try:
        return element.select_one(selector).get_text(strip=True)
    except AttributeError:
        return "N/A"

def scroll_down(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Adjust this sleep time based on your observations

def scrape_magicbricks_data(url, max_items, driver=None):
    driver.get(url)

    # Scroll down until the desired number of items are loaded
    while len(driver.find_elements(By.CSS_SELECTOR, '.mb-srp__card')) <= max_items:
        scroll_down(driver)

    # Parse the HTML content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract property details
    property_listings = soup.select('.mb-srp__card')

    scraped_data = []  # Use a list to store data

    serial_number = 1

    for listing in property_listings:
        # Use try-except block to handle potential NoneType
        try:
            title_highlight = get_text_or_na(listing, '.mb-srp__card__developer--name--highlight')
            title_society = get_text_or_na(listing, '.mb-srp__card__society')
            title = title_highlight if title_highlight != "N/A" else title_society
        except AttributeError:
            title = "N/A"

        city = get_text_or_na(listing, '.mb-srp__card--title')
        price = get_text_or_na(listing, '.mb-srp__card__price--amount')
        area = get_text_or_na(listing, '.mb-srp__card__summary--value')

        # Check for duplicate data
        if (title, city, price, area) not in scraped_data:
            scraped_data.append([serial_number, title, city, price, area])
            serial_number += 1

            if serial_number > max_items:
                break  # Stop when reaching the desired number of items

    # Create a DataFrame from the list
    columns = ["Serial No.", "Title", "City", "Price", "Area"]
    df = pd.DataFrame(scraped_data, columns=columns)

    return df

def get_developer_links(driver, url, max_items):
    developer_links = []
    driver.get(url)

    # Scroll down until the desired number of items are loaded
    while len(driver.find_elements(By.CSS_SELECTOR, '.mb-srp__card')) <= max_items:
        scroll_down(driver)

    # Wait for developer links to be present
    developer_links_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'mb-srp__card__developer'))

    try:
        developer_links = WebDriverWait(driver, 10).until(developer_links_present)
        developer_links = [link.find_element(By.TAG_NAME, 'a').get_attribute('href') for link in developer_links]

        # Return only the required number of links (max_items)
        return developer_links[:max_items]
    except Exception as e:
        print(f"Error: {e}")
        return developer_links

def scrape_all_images(driver, href):
    driver.get(href)

    # Wait for the img-block class to be clickable
    class_selector = 'img-block'
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_selector)))
    element.click()
    time.sleep(5)

    try:
        # Wait for the gallery-modal__nav class to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gallery-modal__nav__item'))
        )

        # Find all images under gallery-modal__slider__img-wrap
        img_wraps = driver.find_elements(By.CLASS_NAME, 'gallery-modal__slider__img-wrap')
        floor_plan_count = 0
        img_data = []

        for img_wrap in img_wraps:
            try:
                img_element = img_wrap.find_element(By.TAG_NAME, 'img')
                img_url = img_element.get_attribute('src')

                if "Floor-Plan" in img_url:
                    # print(f"Image URL with Floor-Plan: {img_url}")
                    floor_plan_count += 1
                    if floor_plan_count >= 4:
                        break
                    img_data.append(img_url)

            except NoSuchElementException:
                print("No img element found under gallery-modal__slider__img-wrap.")

        # Create a DataFrame with the scraped floor plan URLs
        columns = ["Image_URL"]
        img_df = pd.DataFrame(img_data, columns=columns)


        return img_df

    except TimeoutException:
        print("TimeoutException: Unable to locate the image container within the specified timeout.")
        return pd.DataFrame()
    finally:
        driver.quit()

# Inside the main() function

# Inside the main() function

