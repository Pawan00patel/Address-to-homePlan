# app.py
import sqlite3
import time

from flask import Flask, render_template, request

from web_scraper import scrape_property_data

app = Flask(__name__)


# Function to create a SQLite database and table if they don't exist
def initialize_database():
    conn = sqlite3.connect('property.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            id INTEGER PRIMARY KEY,
            title TEXT,
            price TEXT,
            area TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()


initialize_database()


# Function to insert data into the database
def insert_data_into_database(data):
    try:
        conn = sqlite3.connect('property.db')
        cursor = conn.cursor()
        for item in data:
            cursor.execute('''
                INSERT INTO properties (title, price, area, description)
                VALUES (?, ?, ?, ?)
            ''', item)  # item should be a tuple
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"An error occurred while inserting data into the database: {str(e)}")



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        city = request.form['city']
        start_time = time.time()
        scraped_data = []
        while time.time() - start_time < 80 and len(scraped_data) < 1000:
            new_data = scrape_property_data(city)
            if not new_data:
                break
            scraped_data.extend(new_data)

        if scraped_data:
            insert_data_into_database(scraped_data)
            result = f'Scraped and saved {len(scraped_data)} data entries for {city} successfully.'
        else:
            result = f'No data found for {city} within the time limit.'

    except Exception as e:
        result = f'Error: {str(e)}'

    return render_template('index.html', result=result)


@app.route('/add_city')
def add_city():
    return render_template('add_city.html')


@app.route('/view_data')
def view_data():
    conn = sqlite3.connect('property.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM properties')
    data = cursor.fetchall()
    conn.close()
    return render_template('view_data.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
