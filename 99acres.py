import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time



def scrape_99acres_listing_urls(url, class_name_to_click, max_scrolls):
    # Set up Chrome options to run in headless mode and disable notifications
    options = webdriver.ChromeOptions()
    options.add_argument('-headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up Chrome driver with the configured options
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Initialize a set to store unique URLs
    unique_urls = set()

    for _ in range(max_scrolls):
        try:
            # Find and click on elements with the specified class name
            wait = WebDriverWait(driver, 10)
            elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_name_to_click)))

            # Extract and add unique href attributes to the set
            for element in elements:
                try:
                    a_tag = element.find_element(By.TAG_NAME, 'a')
                    if a_tag:
                        link = a_tag.get_attribute('href')
                        if link:
                            unique_urls.add(link)
                except NoSuchElementException:
                    print("No 'a' tag found within the element.")
                    continue

            # Scroll down to load more content
            driver.execute_script("window.scrollTo(1, document.body.scrollHeight);")
            time.sleep(5)  # Adjust the sleep time as needed

        except NoSuchElementException:
            print("No elements with the specified class name found.")
            break  # Exit the loop if no elements found

    # Close the browser when done
    driver.quit()

    # Convert the set of unique URLs to a list before returning
    result_urls = list(unique_urls)
    result_urls.sort()  # Optional: Sort the list if needed

    return result_urls
def scrape_multiple_pages(base_url, class_name_to_click, start_page, end_page, max_scrolls):
    all_result_urls = []

    for page_number in range(start_page, end_page + 1):
        # Construct the complete URL for each page
        complete_url = f'{base_url}-page-{page_number}'

        # Call scrape_99acres_listing_urls function
        result_urls = scrape_99acres_listing_urls(complete_url, class_name_to_click, max_scrolls)
        all_result_urls.extend(result_urls)

        # Increment page number for the next iteration
        page_number += 1

    return all_result_urls


def scrape_property_data_from_urls(url_list):
    # Create an empty list to store scraped data
    scraped_data = []

    # Set up Chrome options for non-headless browsing
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Set up Chrome driver in non-headless mode
    driver = webdriver.Chrome(options=options)

    # Initialize a set to keep track of visited URLs
    visited_urls = set()

    # Set up WebDriverWait
    wait = WebDriverWait(driver, 30)

    # Loop through each URL
    for url in url_list:
        if url in visited_urls:
            continue  # Skip if the URL has already been visited

        try:
            # Open the URL
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

            # Add the URL to the visited set
            visited_urls.add(url)

            # Wait for all elements under the specified class to be present
            class_selector = 'ProjectDetailV2Desktop__mainWrapper'

            # Use a combination of expected conditions to wait for the presence of elements
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, class_selector)))

            # Scroll down to make sure all content is loaded (adjust the number of scrolls if needed)
            for _ in range(5):
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
                time.sleep(5)

            # Extract property details using explicit waits
            property_name = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ProjectInfo__imgBox1 title_bold'))).text
            city = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'caption_subdued_medium ProjectInfo__imgBox1SubTxt'))).text
            price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'list_header_semiBold configurationCards__configurationCardsHeading'))).text
            area = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'caption_subdued_medium configurationCards__cardAreaSubHeadingOne'))).text

            # Filter img elements with URLs ending with .gif extension and containing "plan" keyword
            gif_urls = []
            class_name_to_find = 'carousel__slidingBox'  # Replace with your desired class name
            elements = driver.find_elements(By.CLASS_NAME, class_name_to_find)
            for element in elements:
                img_url = element.get_attribute("src")
                if img_url and img_url.endswith('.gif'):
                    gif_urls.append(img_url)

            # Only store valid image URLs in the scraped data
            if gif_urls:
                property_details = {
                    'Property Name': property_name,
                    'City': city,
                    'Price': price,
                    'Area': area,
                    'Floor Plan URLs': gif_urls
                }
            else:
                property_details = {
                    'Property Name': property_name,
                    'City': city,
                    'Price': price,
                    'Area': area,
                    'Floor Plan URLs': ['No home plan for this property']
                }

            scraped_data.append(property_details)
        except Exception as e:
            print(f"Exception while processing URL {url}: {e}")

    # Close the browser when done
    driver.quit()

    # Create a Pandas DataFrame from the scraped data
    df = pd.DataFrame(scraped_data)

    return df
base_url_99acres = 'https://www.99acres.com/property-in-bangalore-ffid'
class_name_to_click_99acres = 'PseudoTupleRevamp__headNrating'  # Replace with the actual class name
start_page_99acres = 1
end_page_99acres = 1  # Adjust the end page as needed
max_scrolls_99acres = 5  # Adjust the number of scrolls as needed

result_urls_99acres = scrape_multiple_pages(base_url_99acres, class_name_to_click_99acres, start_page_99acres, end_page_99acres, max_scrolls_99acres)
print("Number of URLs extracted:", len(result_urls_99acres))
print(result_urls_99acres)

# Call the scrape_property_data_from_urls function to get property details
property_details_df = scrape_property_data_from_urls(result_urls_99acres)

# Print the extracted details


print(property_details_df)
