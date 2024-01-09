from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time

def scrape_99acres_listing_urls(url, class_name_to_click, max_scrolls):
    # base_url = f'https://www.99acres.com/property-in-bangalore-ffid-page-{pageno}'

    # Set up Firefox options to run in headless mode and disable notifications
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    # Set up Firefox driver with the configured options
    driver = webdriver.Firefox(options=options)
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
            time.sleep(2)  # Adjust the sleep time as needed

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
        complete_url = f"{base_url}-page-{page_number}"

        # Call scrape_99acres_listing_urls function
        result_urls = scrape_99acres_listing_urls(complete_url, class_name_to_click, max_scrolls)
        all_result_urls.extend(result_urls)

        # Increment page number for the next iteration
        page_number += 1

    return all_result_urls


# Example usage:
base_url_99acres = 'https://www.99acres.com/property-in-bangalore-ffid'
class_name_to_click_99acres = 'PseudoTupleRevamp__headNrating'  # Replace with the actual class name
start_page_99acres = 1
end_page_99acres = 3  # Adjust the end page as needed
max_scrolls_99acres = 5  # Adjust the number of scrolls as needed

result_urls_99acres = scrape_multiple_pages(base_url_99acres, class_name_to_click_99acres, start_page_99acres, end_page_99acres, max_scrolls_99acres)
print("Number of URLs extracted:", len(result_urls_99acres))
print(result_urls_99acres)
