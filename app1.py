from selenium import webdriver

# Specify the path to your Chromedriver executable
chrome_driver_path = r"C:\chrome web driver\2\chromedriver-win64\chromedriver.exe"

# Create Chrome WebDriver options
options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')

# Specify the Chromedriver executable path and options
driver = webdriver.Chrome(options=options)
driver.maximize_window()

# Open the Magicbricks website
driver.get("https://www.magicbricks.com")

# Add your web automation code here

# Keep the Chrome window open until you explicitly close it
input("Press Enter to close the Chrome window...")  # Wait for user input
driver.quit()  # Close the WebDriver
