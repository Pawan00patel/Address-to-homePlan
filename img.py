from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_image_urls(base_url):
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    options.set_preference("dom.webnotifications.enabled", False)

    driver = webdriver.Firefox(options=options)
    driver.get(base_url)

    image_urls = []

    try:
        # Navigate to the specified structure
        popup_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'popup-tab')))
        floor_plans_tab = popup_tab.find_element(By.ID, 'floor_plans')
        serp_qv_content = floor_plans_tab.find_element(By.ID, 'serp-qv-content')
        gallery_tab = serp_qv_content.find_element(By.CLASS_NAME, 'galleryModalTab')
        slider = gallery_tab.find_element(By.CLASS_NAME, 'slider')
        slick_list = slider.find_element(By.CLASS_NAME, 'slick-list')
        slick_slide = slick_list.find_element(By.CLASS_NAME, 'slick-slide')

        # Find the floor plan images within the specified structure
        elements = slick_slide.find_elements(By.CLASS_NAME, 'cf-lazyload')

        for element in elements:
            img_url = element.get_attribute("src")
            if img_url:
                image_urls.append(img_url)

    except NoSuchElementException as e:
        print(f"Error while scraping image URLs: Element not found - {e}")
    except TimeoutException as e:
        print(f"Error while scraping image URLs: Timeout - {e}")
    except Exception as e:
        print(f"Error while scraping image URLs: {e}")

    driver.quit()
    return image_urls

# Example usage in app.py
if __name__ == "__main__":
    base_url = 'https://www.commonfloor.com/listing-search?city=Mumbai&cg=Mumbai%20division&iscg=&search_intent=sale&polygon=1&page=1&page_size=70'

    image_urls = scrape_image_urls(base_url)

    # Print the scraped image URLs
    for url in image_urls:
        print("Image URL:", url)

# from playwright.sync_api import sync_playwright
# import time
# from rich import print
#
#
# def scroll_and_handle_prompt():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         page = browser.new_page()
#         page.set_viewport_size(
#             {
#                 "width": 1280, "height": 1080
#             }
#         )
#         page.goto(
#             "https://www.commonfloor.com/listing-search?city=Bangalore&cg=Bangalore%20division&iscg=&search_intent=sale&property_location_filter%5B%5D=region_519bb3d82028e&prop_name%5B%5D=Bagaluru&polygon=1&page=1&page_size=10")
#         time.sleep(2)
#
#         # Continuously scroll and check for the prompt
#         while True:
#             page.keyboard.press("End")
#             time.sleep(1)
#
#             # Check if the "Would you like CommonFloor to send matching property notifications?" prompt is visible
#             if page.query_selector('text=Would you like CommonFloor to send matching property notifications?'):
#                 try:
#                     not_now_button = page.locator('text=NOT NOW')
#                     not_now_button.click()
#                     print("Clicked 'NOT NOW' on the prompt.")
#                 except:
#                     print("Failed to click 'NOT NOW'.")
#                 break  # Exit the loop if the prompt is handled
#
#         # Continue scrolling after handling the prompt
#         for x in range(1, 10):
#             page.keyboard.press("End")
#             print("Scrolling key press", x)
#             time.sleep(1)
#
#         browser.close()
#
#
# def main():
#     scroll_and_handle_prompt()
#
#
# if __name__ == "__main__":
#     main()


