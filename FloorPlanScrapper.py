from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Firefox driver
driver = webdriver.Firefox()

# Open the URL
url = 'https://www.commonfloor.com/listing/-2-bhk-apartment-for-sale-in-hennur-road-bangalore-at-kumar-prospera/nfri62wz6g3kawlg'
# url = 'https://www.commonfloor.com/listing/2bhk-apartment-for-sale-in-chikkagubbi-village-bangalore-at-dnr-parklink/jt4mtq0lnypr7ahm'
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

# Print the extracted GIF URLs
for url in gif_urls:
    print("GIF URL:", url)

# Close the browser when done
driver.quit()
