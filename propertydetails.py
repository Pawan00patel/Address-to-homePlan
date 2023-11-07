from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


def scrape_property_details(base_url, class_name_to_find, max_scrolls):
    # Set up Firefox options to run in headless mode and disable notifications
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    # Set up Firefox driver with the configured options
    driver = webdriver.Firefox(options=options)

    # Open the base URL
    driver.get(base_url)

    property_data = []

    for _ in range(max_scrolls):
        # Wait for the elements to load
        wait = WebDriverWait(driver, 10)
        elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name_to_find)))

        for element in elements:
            # Find the <a> tag within the <h2> element
            title_element = element.find_element(By.CLASS_NAME, 'st_title')

            # Extract the title from the <a> tag
            title = title_element.text[:70]

            # Find the price within the element
            price_element = element.find_element(By.CLASS_NAME, 's_p')
            price = price_element.text

            # Find the area within the element
            area_element = element.find_element(By.CLASS_NAME, 'infodata')
            area = area_element.text

            property_data.append({'Title': title, 'Price': price, 'Area': area})

        # Scroll down to load more content
        driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
        time.sleep(2)  # Increase sleep time to ensure full page load


    # Close the browser when done
    driver.quit()

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(property_data)

    return df

def scrape_listing_urls(base_url, class_name_to_click, max_scrolls):
    # Set up Firefox options to run in headless mode and disable notifications
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    # Set up Firefox driver with the configured options
    driver = webdriver.Firefox(options=options)

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

# Example usage in app.py
if __name__ == "__main__":
    base_url = 'https://www.commonfloor.com/listing-search?city=Mumbai&cg=Mumbai%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=70'
    class_name_to_find = 'impressionAd'
    max_scrolls = 1

    property_details_df = scrape_property_details(base_url, class_name_to_find, max_scrolls)

    # Print the scraped property details
    print(property_details_df.to_string())

if __name__ == "__main__":
    base_url = 'https://www.commonfloor.com/listing-search?city=Mumbai&cg=Mumbai%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=70'
    class_name_to_click = 'st_title'  # Replace with your desired class name
    max_scrolls = 1

    scraped_urls = scrape_listing_urls(base_url, class_name_to_click, max_scrolls)

    # Print the scraped URLs
    print(f"Total {len(scraped_urls)} URLs extracted:")
    for url in scraped_urls:
        print("Listing URL:", url)



def scrape_data_from_urls(url_list):
    # Create an empty list to store scraped data
    scraped_data = []

    # Set up Firefox driver
    driver = webdriver.Firefox()

    # Loop through each URL
    for url in url_list:
        try:
            # Open the URL
            driver.get(url)

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

            # Filter img elements with URLs ending with .gif extension and extract their URLs
            gif_urls = []
            for element in elements:
                img_url = element.get_attribute("src")
                if img_url and img_url.endswith('.gif'):
                    gif_urls.append(img_url)

            # Store the scraped data in a dictionary
            scraped_data.append({ 'Floor plan URLs': gif_urls})
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Exception while processing URL {url}: {e}")

    # Close the browser when done
    driver.quit()

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(scraped_data)

    return df

floorplan=scrape_data_from_urls(scraped_urls)
print(floorplan.to_string())
