from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask import jsonify
from datetime import date as dt

from functions import get_weather_data, convert_temp


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
        
        weather_data = {
            'temp': temp,
            'unit': unit,
            'city': city,
            'date': date,
        }
        
        return jsonify(weather_data)

api.add_resource(Weather, '/weather')


if __name__ == '__main__':
     app.run(port='5002')
