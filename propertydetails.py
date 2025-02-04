from typing import List, Any

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def scrape_property_details(city, class_name_to_find, max_scrolls):
    # Set up Chrome options to run in headless mode and disable notifications
    base_url = f'https://www.commonfloor.com/listing-search?city={city}&cg={city}%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=10'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')

    # Set up Chrome driver with the configured options
    driver = webdriver.Chrome(options=options, service=ChromeService())

    # Open the base URL
    driver.get(base_url)

    property_data = []

    for _ in range(max_scrolls):
        # Wait for the elements to load
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name_to_find)))

        for element in elements:
            # Find the <a> tag within the <h2> element
            title_element = element.find_element(By.CLASS_NAME, 'snbSubH')

            # Extract the title from the <a> tag

            full_title = title_element.text

            # Find the index of 'Similar Properties' in the title
            index_of_similar_properties = full_title.find('Similar Properties')
            title = full_title[:index_of_similar_properties].strip() if index_of_similar_properties != -1 else full_title.strip()

            # Find the price within the element
            city_element = driver.find_element(By.ID, 'snb_cn_id')
            city_name = city_element.text

            # Find the price within the element
            price_element = element.find_element(By.CLASS_NAME, 's_p')
            price = price_element.text

            # Find the area within the element
            area_element = element.find_element(By.CLASS_NAME, 'infodata')
            area = area_element.text

            property_data.append({'Title': title,'City_name': city_name, 'Price': price, 'Area': area})

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
        time.sleep(2)  # Increase sleep time to ensure full page load

    # Close the browser when done
    driver.quit()

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(property_data)

    return df

def scrape_listing_urls(city, class_name_to_click, max_scrolls):
    # Set up Chrome options to run in headless mode and disable notifications
    base_url = f'https://www.commonfloor.com/listing-search?city={city}&cg={city}%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=10'

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-notifications')

    # Set up Chrome driver with the configured options
    driver = webdriver.Chrome(options=options, service=ChromeService())

    # Open the base URL
    driver.get(base_url)

    # Initialize a list to store the URLs
    all_urls = []

    for _ in range(max_scrolls):
        # Find and click on elements with the specified class name
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name_to_click)))

        # Extract and append the href attributes of these elements to the list
        for element in elements:
            a_tag = element.find_element(By.TAG_NAME, 'a')
            if a_tag:
                link = a_tag.get_attribute('href')
                if link:
                    all_urls.append(link)

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed

    # Close the browser when done
    driver.quit()

    # Sort the list of URLs before returning it
    all_urls.sort()

    return all_urls

def scrape_data_from_urls(url_list):
    # Create an empty list to store scraped data
    scraped_data = []

    # Set up Chrome driver
    driver = webdriver.Chrome()

    # Initialize a set to keep track of visited URLs
    visited_urls = set()

    # Loop through each URL
    for url in url_list:
        if url in visited_urls:
            continue  # Skip if the URL has already been visited

        try:
            # Open the URL
            driver.get(url)

            # Add the URL to the visited set
            visited_urls.add(url)

            # Wait for the element with the class name to become clickable
            class_selector = 'pnv-img-wraper'
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_selector)))

            # Click on the element to trigger the onclick function
            element.click()

            # Wait for the page to load (you can adjust the time as needed)
            time.sleep(5)

            # Find all elements with the specified class (e.g., 'your-class-name')
            class_name_to_find = 'cf-lazyload'  # Replace with your desired class name
            elements = driver.find_elements(By.CLASS_NAME, class_name_to_find)

            # Filter img elements with URLs ending with .gif extension and containing "plan" keyword
            gif_urls = []
            for element in elements:
                img_url = element.get_attribute("src")
                if img_url and img_url.endswith('.gif'):
                    gif_urls.append(img_url)

            # Only store valid image URLs in the scraped data
            if gif_urls:
                scraped_data.append({'Floor plan URLs': gif_urls})
            else:
                scraped_data.append({'Floor plan URLs': ['No home plan for this property']})
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Exception while processing URL {url}: {e}")

    # Close the browser when done
    driver.quit()

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(scraped_data)

    return df

# Example usage:
# df_property_details = scrape_property_details('your_city', 'your_class_name', 3)
# url_list = scrape_listing_urls('your_city', 'your_class_name_to_click', 3)
# df_scraped_data = scrape_data_from_urls(url_list)
