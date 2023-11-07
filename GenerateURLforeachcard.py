from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed

    # Close the browser when done
    driver.quit()

    return all_urls

# Example usage in app.py
if __name__ == "__main__":
    base_url = 'https://www.commonfloor.com/listing-search?city=Bangalore&cg=Bangalore%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=70'
    class_name_to_click = 'st_title'  # Replace with your desired class name
    max_scrolls = 2

    scraped_urls = scrape_listing_urls(base_url, class_name_to_click, max_scrolls)

    # Print the scraped URLs
    print(f"Total {len(scraped_urls)} URLs extracted:")
    for url in scraped_urls:
        print("Listing URL:", url)
