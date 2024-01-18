import sqlite3

import pandas as pd
from flask import Flask, request, jsonify
from flask import render_template
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.webdriver import Chrome, WebDriver

from propertydetails import scrape_listing_urls, scrape_property_details, scrape_data_from_urls
from testing import scrape_magicbricks_data, get_developer_links, scrape_all_images

app = Flask(__name__)
driver: WebDriver = None
def get_properties_by_city(city: object):
    conn = sqlite3.connect('property_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE city_name=?", (city,))
    properties = cursor.fetchall()
    conn.close()
    return properties

# Function to create a SQLite database and table if they don't exist
def initialize_database():
    conn = sqlite3.connect('property_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY,
            title TEXT,
            city_name TEXT,
            price TEXT,
            area TEXT,
            image_url varchar(500)
        )
    ''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS magicbricks_properties (
                id INTEGER PRIMARY KEY,
                title TEXT,
                city_name TEXT,
                price TEXT,
                area TEXT,
                image_url varchar(500)
            )
        ''')

    # Create a new table for backup data
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_magicbricks_properties (
                id INTEGER PRIMARY KEY,
                title TEXT,
                city_name TEXT,
                price TEXT,
                area TEXT,
                image_url varchar(500)
            )
        ''')
    conn.commit()
    conn.close()

initialize_database()
def backup_magicbricks_data(data):
    try:
        conn = sqlite3.connect('property_data.db')
        cursor = conn.cursor()
        for item in data:
            cursor.execute('''
                INSERT INTO backup_magicbricks_properties (title, city_name, price, area, image_url)
                VALUES (?, ?, ?, ?, ?)
            ''', (str(item['Title']), str(item['City']), str(item['Price']), str(item['Area']),
                  str(item.get('Image_URL', '')))
                           )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while backing up Magicbricks data: {str(e)}")


def insert_magicbricks_data_into_database(data):
    try:
        with sqlite3.connect('property_data.db') as conn:
            cursor = conn.cursor()
            for item in data:
                cursor.execute('''
                    INSERT OR REPLACE INTO magicbricks_properties (id, title, city_name, price, area, image_url)
                    VALUES (
                        (SELECT id FROM magicbricks_properties WHERE title = ? AND city_name = ?),
                        ?, ?, ?, ?, ?
                    )
                ''', (
                    str(item['Title']),
                    str(item['City']),
                    str(item['Title']),
                    str(item['City']),
                    str(item['Price']),
                    str(item['Area']),
                    str(item.get('Image_URL', ''))
                ))

            # Backup the Magicbricks data before returning it to the client
            # backup_magicbricks_data(data)

        conn.commit()
        conn.close()

        return "Magicbricks data inserted successfully and backed up."
    except Exception as e:
        print(f"An error occurred while inserting Magicbricks data into the database: {str(e)}")
        return f"Error: {str(e)}"

# Call the function to initialize the database
initialize_database()
def insert_data_into_database(data):
    try:
        conn = sqlite3.connect('property_data.db')
        cursor = conn.cursor()
        for item in data:
            cursor.execute('''
                INSERT OR REPLACE INTO properties (id, title, city_name, price, area, image_url)
                VALUES ((SELECT id FROM properties WHERE title = ? AND city_name = ?), ?, ?, ?, ?, ?)
            ''', (str(item['Title']), str(item['City_name']), str(item['Title']), str(item['City_name']),
                  str(item['Price']), str(item['Area']), str(item.get('Image_URL', '')))
            )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while inserting data into the database: {str(e)}")



@app.route('/')
def index():
    return render_template('add_city.html')

@app.route('/homepage')
def homepage():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    city = request.form.get('city')
    print(f'Searching for city: {city}')

    # Retrieve properties from the database
    properties = get_properties_by_city(city)
    print(f'Properties found: {properties}')

    # Pass the properties to the template
    return render_template('results.html', city=city, properties=properties)




@app.route('/scrape', methods=['POST'])
def scrape():
    global scraped_data, city
    try:
        city = request.form['city']
        # start_time = time.time()
        scraped_urls = scrape_listing_urls(city, 'st_title', max_scrolls=1)
        scraped_data = scrape_property_details(city, 'impressionAd', max_scrolls=1)

        if scraped_data is not None and not scraped_data.empty:
            scraped_data['Image_URL'] = scrape_data_from_urls(scraped_urls)
            insert_data_into_database(scraped_data.to_dict('records'))
            result = {
                "message": f'Scraped and saved {len(scraped_data)} data entries for {city} successfully.',
                "data": scraped_data.to_dict(orient='split')  # Return as a Python dictionary
            }
        else:
            result = {"message": f'No data found for {city}.'}

    except Exception as e:
        # If an exception occurs, initialize scraped_data as an empty DataFrame
        scraped_data = pd.DataFrame()
        result = {"error": f'Error: {str(e)}'}

    # Replace NaN values with None in the scraped data
    scraped_data.replace({pd.NA: None}, inplace=True)

    # Return the data as a Python dictionary
    result = {
        "message": f'Scraped and saved {len(scraped_data)} data entries for {city} successfully.',
        "data": scraped_data.to_dict(orient='split')  # Return as a Python dictionary
    }
    print(f"Data sent to client: {result}")
    return result


@app.route('/scrapemagicbriks', methods=['POST'])
def main():
    try:
        # Your existing code for scraping Magicbricks data
        city = request.form['city']
        magicbricks_url = f"https://www.magicbricks.com/property-for-sale/residential-real-estate?bedroom=&proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa&cityName={city}"
        max_items =50
        result_df = scrape_magicbricks_data(magicbricks_url, max_items)

        # Initialize image_urls_list with empty lists
        image_urls_list = [[] for _ in range(len(result_df))]

        developer_links = get_developer_links(magicbricks_url, max_items)
        print(len(developer_links))
        print(developer_links)

        if developer_links:
            # Ensure you have the same number of developer links as the number of data extracted
            developer_links = developer_links[:max_items]
            try:
                drivers: Chrome = webdriver.Chrome()
            except Exception as e:
                print(f"Error: {str(e)}")

            for i, link in enumerate(developer_links, start=1):
                img_df = scrape_all_images(link)

                # Ensure the index is within the bounds of image_urls_list
                if i - 1 < len(image_urls_list):
                    # Assuming each img_df corresponds to a property listing, append the image URLs
                    # to the image_urls_list in the order they are scraped, up to a maximum of 4 URLs
                    if img_df is not None and not img_df.empty:
                        image_urls_list[i - 1] = img_df['Image_URL'].tolist()[:4]
                    else:
                        print(f"No images found for {link}")

            drivers.quit()

        # Ensure the lengths match by extending the result_df index
        result_df.index = range(len(result_df))

        # Add the image URLs to the result_df
        result_df['Image_URL'] = image_urls_list

        # Insert Magicbricks data into the database
        # initialize_database()  # Call this function if not already initialized
        insert_magicbricks_data_into_database(result_df.to_dict('records'))

        # Create the final data structure for the client
        final_data = {
            'message': f'Scraped and saved {len(result_df)} data entries for {city} successfully.',
            'data': {
                'index': result_df.index.tolist(),
                'columns': result_df.columns.tolist(),
                'data': result_df.values.tolist()
            }
        }
        print(f"Data sent to client: {final_data}")
        return jsonify(final_data)

    except Exception as e:
        error_message = f'Error: {str(e)}'
        print(error_message)
        return jsonify({'error': error_message})



@app.route('/add_city')
def add_city():
    return render_template('add_city.html')

@app.route('/view_data')
def view_data():
    conn = sqlite3.connect('property_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties')
    data = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
    driver.quit()
