import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified class
    developer_links = soup.find_all(class_='mb-srp_card_developer')

    # Print all developer links first
    for link in developer_links:
        href = link.find('a')['href']
        print(f"Developer Link: {href}")

    # Initialize a Selenium WebDriver
    driver = webdriver.Chrome()

    # Iterate through the developer links and click them one by one
    for link in developer_links:
        href = link.find('a')['href']
        print(f"\nProcessing Developer Link: {href}")

        # Open the link using Selenium
        driver.get(href)

        # Wait for the img-block class to be clickable
        img_block = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'img-block'))
        )

        # Click on the img-block class
        img_block.click()

        # Wait for the gallery-modal__nav class to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gallery-modal__nav'))
        )

        # Find all elements with the specified class under gallery-modal_nav_item using XPath
        nav_items = driver.find_elements(By.CLASS_NAME, 'gallery-modal_nav_item')

        # Click on the first nav_item (assuming the first one is what you need)
        if nav_items:
            nav_items[4].click()

        # Wait for the gallery-modal_slider_img-wrap class to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gallery-modal_slider_img-wrap'))
        )

        # Find the element with the specified class under gallery-modal_slider_img-wrap
        img_wrap = driver.find_element_by_class_name('gallery-modal_slider_img-wrap')
        img_url = img_wrap.find_element_by_tag_name('img')['src']
        print(f"Floor Plan Image URL: {img_url}")

    # Close the WebDriver
    driver.quit()

else:
    print(f"Failed to retrieve the page. Status Code: {response.status_code}")