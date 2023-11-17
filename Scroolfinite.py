from playwright.sync_api import sync_playwright
from rich import print
import time
from propertydetails import scrape_property_details

def scroll_and_gather_urls(city):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_viewport_size({"width": 1280, "height": 1080})
        base_url = f"https://www.commonfloor.com/listing-search?city=Bangalore&cg=Bangalore%20division&iscg=&search_intent=sale&property_location_filter%5B%5D=region_519bb3d82028e&polygon=1&page=1&page_size=10"
        page.goto(base_url)
        time.sleep(2)

        property_urls = []

        while True:
            page.keyboard.press("End")
            time.sleep(1)

            # Check if the "Would you like CommonFloor to send matching property notifications?" prompt is visible
            if page.query_selector('text=Would you like CommonFloor to send matching property notifications?'):
                try:
                    not_now_button = page.locator('text=NOT NOW')
                    not_now_button.click()
                    print("Clicked 'NOT NOW' on the prompt.")
                except:
                    print("Failed to click 'NOT NOW'.")
                break  # Exit the loop if the prompt is handled

            # Find and store property URLs
            property_elements = page.locator('css=a.property-listing-card')
            for property_element in property_elements:
                url = property_element.get_attribute("href")
                if url:
                    property_urls.append(url)

        browser.close()

        return property_urls

def main():
    city = "Bangalore"  # Replace with your desired city
    max_scrolls = 5  # Adjust the number of scrolls as needed

    # Scroll and gather property URLs
    property_urls = scroll_and_gather_urls(city)

    # Now you can pass the gathered property URLs to your scraping function
    property_details_df = scrape_property_details(city, 'impressionAd', max_scrolls)

    # Print the scraped property details
    print(property_details_df.to_string())

if __name__ == "__main__":
    main()
