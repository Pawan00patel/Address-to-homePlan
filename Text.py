import pandas as pd
import requests
from bs4 import BeautifulSoup

url = 'https://www.magicbricks.com/property-for-sale/residential-commercial-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment,Residential-House,Villa,Residential-Plot,Commercial-Office-Space,Office-ITPark-SEZ,Commercial-Shop,Commercial-Showroom,Commercial-Land,Industrial-Land,Warehouse/Godown,Industrial-Building,Industrial-Shed&BudgetMin=50-Lacs&BudgetMax=1-Crores&cityName=bangalore'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

price_elements = soup.find_all(class_='mb-srp__card__price--amount')
prices = [element.get_text(strip=True) for element in price_elements]

title_elements = soup.find_all(class_='mb-srp__card--title')
titles = [element.get_text(strip=True) for element in title_elements]

area_elements = soup.find_all('div', class_='mb-srp__card__summary--value')
areas = [element.get_text(strip=True) for element in area_elements]

description_elements = soup.find_all(class_='two-line-truncated')
descriptions = [element.get_text(strip=True)[:100] + '...' for element in description_elements]  # Limiting description length to 100 characters

data = []
max_length = max(len(prices), len(titles), len(areas), len(descriptions))
for i in range(max_length):
    item = {
        'Title': titles[i] if i < len(titles) else None,
        'Price': prices[i] if i < len(prices) else None,
        'Area': areas[i] if i < len(areas) else None,
        'Floorplan': descriptions[i] if i < len(descriptions) else None
    }
    data.append(item)

df = pd.DataFrame(data)
output_file = 'data.xlsx'
df.to_excel(output_file, index=False)
print(f'Data saved to {output_file}')
