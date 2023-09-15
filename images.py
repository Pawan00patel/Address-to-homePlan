import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# URL of the webpage to scrape images from
url = 'https://www.magicbricks.com/propertyDetails/2-BHK-1161-Sq-ft-Multistorey-Apartment-FOR-Sale-Hosa-Road-in-Bangalore&id=4d423638323934343339'

# Initialize the Chrome driver
driver = webdriver.Chrome()

# Open the webpage
driver.get(url)

# Scroll down to load additional images (you may need to adjust this based on the webpage structure)
scroll_height = 0
while scroll_height < 5000:  # Adjust the value as needed
    driver.execute_script(f"window.scrollTo(0, {scroll_height});")
    scroll_height += 500  # Adjust the scroll increment as needed
    time.sleep(2)  # Give the page time to load

# Find all image elements using a CSS selector
img_elements = driver.find_elements(By.CSS_SELECTOR, 'img')

# Extract the 'src' attribute (image URL) from each image element
image_urls = [img.get_attribute('src') for img in img_elements]

# Filter the image URLs to include only valid image file extensions
valid_image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
filtered_image_urls = [url for url in image_urls if url.lower().endswith(valid_image_extensions)]

# Print the list of filtered image URLs
for image_url in filtered_image_urls:
    print(image_url)

# Close the browser
driver.quit()
