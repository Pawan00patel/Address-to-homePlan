import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_developer_links(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        developer_links = soup.find_all(class_='mb-srp__card__developer')
        for link in developer_links:
            href = link.find('a')['href']
            print(f"Developer Link: {href}")
        return [link.find('a')['href'] for link in developer_links]
    else:
        print(f"Failed to retrieve the page. Status Code: {response.status_code}")
        return []

def scrape_all_images(driver, href):
    print(f"\nProcessing Developer Link: {href}")
    driver.get(href)

    # Wait for the img-block class to be clickable
    class_selector='img-block'
    wait = WebDriverWait(driver, 10)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_selector)))
    element.click()
    time.sleep(5)
    # Click on the img-block class

    try:
        # Wait for the gallery-modal__nav class to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'gallery-modal__nav__item'))
        )

        # Find all images under gallery-modal__slider__img-wrap
        img_wraps = driver.find_elements(By.CLASS_NAME, 'gallery-modal__slider__img-wrap')

        for img_wrap in img_wraps:
            try:
                # Find the img element under gallery-modal__slider__img-wrap
                img_element = img_wrap.find_element(By.TAG_NAME, 'img')

                # Get the img_url from the src attribute
                img_url = img_element.get_attribute('src')

                # Check if the URL contains the string "Floor-Plan"
                if "Floor-Plan" in img_url:
                    print(f"Image URL with Floor-Plan: {img_url}")

            except NoSuchElementException:
                print("No img element found under gallery-modal__slider__img-wrap.")

    except TimeoutException:
        print("TimeoutException: Unable to locate the image container within the specified timeout.")


def main():
    base_url = 'https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName=Bangalore'
    developer_links = get_developer_links(base_url)

    if developer_links:
        driver = webdriver.Chrome()
        for link in developer_links:
            scrape_all_images(driver, link)
        driver.quit()

if __name__ == "__main__":
    main()
