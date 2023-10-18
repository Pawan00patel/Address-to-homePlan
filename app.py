# app.py
import time
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from web_scraper import scrape_property_data

app = Flask(__name__)

# Function to create a SQLite database and table if they don't exist
# ... (existing code)

def initialize_database():
    conn = sqlite3.connect('property_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price TEXT,
            area TEXT,
            description TEXT,
            highlight TEXT UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

initialize_database()

# ... (rest of your code)


# Function to insert data into the database
# Function to insert data into the database
def insert_data_into_database(data):
    try:
        conn = sqlite3.connect('property_data.db')
        cursor = conn.cursor()
        for item in data:
            try:
                # Check if a record with the same 'highlight' value exists
                cursor.execute('SELECT id FROM properties WHERE highlight = ?', (item[4],))
                existing_record = cursor.fetchone()
                if not existing_record:
                    cursor.execute('''
                        INSERT INTO properties (title, price, area, description, highlight)
                        VALUES (?, ?, ?, ?, ?)
                    ''', item)
            except sqlite3.IntegrityError:
                # Handle potential IntegrityError if you have constraints on the database
                pass
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while inserting data into the database: {str(e)}")

@app.route('/')
def index():
    return render_template('add_city.html')

# ... (existing code)

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        city = request.form['city']

        # Use a loop to scrape data from multiple pages or cities
        all_scraped_data = []

        for page in range(1, 10):  # Example: Scrape data from 5 pages
            city_url = f"https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=50-Lacs&BudgetMax=1-Crores&cityName={city}&page={page}"
            scraped_data = scrape_property_data(city_url)

            if not scraped_data:
                break

            all_scraped_data.extend(scraped_data)

        if all_scraped_data:
            insert_data_into_database(all_scraped_data)
            result = f'Scraped and saved {len(all_scraped_data)} data entries for {city} successfully.'
        else:
            result = f'No data found for {city} within the time limit.'

    except Exception as e:
        result = f'Error: {str(e)}'

    return render_template('index.html', result=result)

# ... (rest of your code)

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
