from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from playwright.sync_api import sync_playwright
from rich import print

def scroll_and_handle_prompt(playwright_page):
    # Continuously scroll and check for the prompt
    while True:
        playwright_page.keyboard.press("End")
        time.sleep(1)

        # Check if the "Would you like CommonFloor to send matching property notifications?" prompt is visible
        if playwright_page.query_selector('text=Would you like CommonFloor to send matching property notifications?'):
            try:
                not_now_button = playwright_page.locator('text=NOT NOW')
                not_now_button.click()
                print("Clicked 'NOT NOW' on the prompt.")
            except:
                print("Failed to click 'NOT NOW'.")
            break  # Exit the loop if the prompt is handled

    # Continue scrolling after handling the prompt
    for x in range(1, 10):
        playwright_page.keyboard.press("End")
        print("Scrolling key press", x)
        time.sleep(1)

def scrape_property_details(base_url, class_name_to_find, max_scrolls):
    # Set up Firefox options to run in headless mode and disable notifications
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    # Set up Firefox driver with the configured options
    driver = webdriver.Firefox(options=options)

    # Open the base URL
    driver.get(base_url)

    # Call the Playwright function to handle the prompt
    with sync_playwright() as p:
        playwright_page = p.firefox.launch().new_page()
        playwright_page.goto(base_url)
        scroll_and_handle_prompt(playwright_page)
        playwright_page.close()

    property_data = []

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

    # Rest of your scraping code...


def scrape_listing_urls(base_url, class_name_to_click, max_scrolls):
    # Set up Firefox options to run in headless mode and disable notifications
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    # Set up Firefox driver with the configured options
    driver = webdriver.Firefox(options=options)

    # Open the base URL
    driver.get(base_url)

    # Call the Playwright function to handle the prompt
    with sync_playwright() as p:
        playwright_page = p.firefox.launch().new_page()
        playwright_page.goto(base_url)
        scroll_and_handle_prompt(playwright_page)
        playwright_page.close()

    # Rest of your scraping code for URLs...

def scrape_data_from_urls(url_list):
    # Create an empty list to store scraped data

    # Rest of your scraping code for data from URLs...

# Example usage in app.py
if __name__ == "__main__":
    base_url = 'https://www.commonfloor.com/listing-search?city=Mumbai&cg=Mumbai%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=70'
    class_name_to_find = 'impressionAd'
    max_scrolls = 1

    property_details_df = scrape_property_details(base_url, class_name_to_find, max_scrolls)

    # Print the scraped property details
    print(property_details_df.to_string())

    # Scrape URLs
    class_name_to_click = 'st_title'  # Replace with your desired class name
    max_scrolls = 1

    scraped_urls = scrape_listing_urls(base_url, class_name_to_click, max_scrolls)

    # Print the scraped URLs
    print(f"Total {len(scraped_urls)} URLs extracted:")
    for url in scraped_urls:
        print("Listing URL:", url)

    # Scrape data from the URLs
    floorplan = scrape_data_from_urls(scraped_urls)
    print(floorplan.to_string())
