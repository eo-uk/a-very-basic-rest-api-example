from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from datetime import date as dt
from bs4 import BeautifulSoup
import requests



app = Flask(__name__)
api = Api(app)

class Weather(Resource):
    def get(self):
        unit = request.args.get('unit').title() if request.args.get('unit') else 'Celsius'
        city = request.args.get('city').title() if request.args.get('city') else 'London'
        temp = str(int(float(get_weather_data(city).replace('°', ''))))
        date = str(dt.today())

        #Conversion of temp based on unit
        if unit != 'Celsius':
            try:
                temp = convert_temp(temp, unit)
            except ValueError:
                unit = 'Celsius' #Default to Celsius if unit is unknown
        
        result = {
            'temp': temp,
            'unit': unit,
            'city': city,
            'date': date,
        }
        
        return jsonify(result)

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

#Weather route
api.add_resource(Weather, '/weather')


if __name__ == '__main__':
     app.run(port='5002')
