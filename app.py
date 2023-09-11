import sqlite3
import subprocess

from flask import Flask, render_template

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
            description TEXT,
            images TEXT
        )
    ''')

    conn.commit()
    conn.close()


initialize_database()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        subprocess.run(['python', 'text.py'])
        result = 'Script executed successfully.'
    except Exception as e:
        result = f'Error: {str(e)}'

    return render_template('index.html', result=result)
# @app.route('/run_image_script', methods=['POST'])
# def run_image_script():
#     try:
#         subprocess.run(['python', 'images.py'])
#         result = 'Image Script executed successfully.'
#     except Exception as e:
#         result = f'Error: {str(e)}'
#
#     return render_template('index.html', result=result)


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
