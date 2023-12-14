import time
import sqlite3
from flask import Flask, render_template, request
from propertydetails import scrape_listing_urls, scrape_property_details, scrape_data_from_urls


app = Flask(__name__)

def get_properties_by_city(city):
    conn = sqlite3.connect('property_data.db')  # Replace with your database name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties WHERE title LIKE ?", ('%' + city + '%',))
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
    conn.commit()
    conn.close()

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
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    city = request.form.get('city')
    print(f'Searching for city: {city}')

    properties = get_properties_by_city(city)
    print(f'Properties found: {properties}')

    return render_template('results.html', city=city, properties=properties)


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        city = request.form['city']
        start_time = time.time()
        scraped_urls = scrape_listing_urls(city, 'st_title', max_scrolls=1)
        scraped_data = scrape_property_details(city, 'impressionAd', max_scrolls=1)

        if scraped_data is not None and not scraped_data.empty:
            # Scrape image URLs
            scraped_data['Image_URL'] = scrape_data_from_urls(scraped_urls)
            insert_data_into_database(scraped_data.to_dict('records'))
            result = f'Scraped and saved {len(scraped_data)} data entries for {city} successfully.'
        else:
            result = f'No data found for {city}.'

    except Exception as e:
        result = f'Error: {str(e)}'

    return render_template('index.html', result=result)

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
