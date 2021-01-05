import requests
from bs4 import BeautifulSoup

def get_weather_data(city):
    '''Extracts weather data from www.metoffice.gov.uk'''
    
    CITY_CODES = {
        'London': 'gcpvj0v07',
        'Edinburgh': 'gcvwr3zrw',
        'Belfast': 'gcey94cuf',
        'Cardiff': 'gcjszmp44',
    }
    
    URL = r'https://www.metoffice.gov.uk/weather/forecast/' + CITY_CODES[city]
    page = requests.get(URL)
    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        result = soup.select('.weather-day-values .tab-temp-high')[0].get_text()
        return result

def convert_temp(temp, unit):
    '''Converts given temp in celcius to the given unit ('Fahrenheit' or 'Kelvin')'''
    temp = int(float(temp))
    if unit.title() == 'Fahrenheit':
        return str(int(temp * (9/5) + 32))
    elif unit.title() == 'Kelvin':
        return str(int(temp + 273.15))
    else:
        raise ValueError('Unknown unit. Please try Fahrenheit or Kelvin.')
