import sqlite3

from flask import Flask, render_template, redirect, url_for, request
from web_scraper import scrape_property_data, insert_data_into_database

app = Flask(__name__)

# Function to create a SQLite database and table if they don't exist
def initialize_database():
    conn = sqlite3.connect('property_data.db')
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

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        city = request.form['city']
        city_url = f"https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=50-Lacs&BudgetMax=1-Crores&cityName={city}"

        scraped_data = scrape_property_data(city_url)
        if scraped_data:
            insert_data_into_database(scraped_data)
            result = f'Scraped and saved data for {city} successfully.'
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
