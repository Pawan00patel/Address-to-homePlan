from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

def get_urls_from_class(url, class_name):
    try:
        # Set up Firefox options for headless browsing
        firefox_options = Options()
        firefox_options.add_argument('-headless')

        # Initialize the Firefox web driver
        driver = webdriver.Firefox(options=firefox_options)

        # Navigate to the URL
        driver.get(url)

        # Get the page source after waiting for a short period to ensure JavaScript content is loaded
        driver.implicitly_wait(10)  # Adjust the wait time as needed
        page_source = driver.page_source

        # Parse the HTML content of the page
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find all anchor tags with the specified class name
        anchor_tags = soup.find_all('a', class_=class_name)

        # Extract and return the href attribute of each anchor tag
        return [tag.get('href') for tag in anchor_tags if tag.get('href')]

    except Exception as e:
        print(f"Error: {e}")
        return []


    finally:
        # Close the web driver
        if 'driver' in locals():
            driver.quit()

# Example usage:
url_input = input("Enter the URL: ")
class_name_input = input("Enter the class name: ")

result_urls = get_urls_from_class(url_input, class_name_input)

if result_urls:
    print("Found URLs:")
    for url in result_urls:
        print(url)
else:
    print("No URLs found.")
