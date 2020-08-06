"""Simple forecast module which uses OpenWeatherMap API
"""
import json
import os
from typing import List, Dict

import requests
from dateutil.parser import parse

API_KEY = os.getenv('OPEN_WEATHER_MAP_API_KEY')
if not API_KEY:
    with open('example-config.ini', mode='r') as config_file:
        config = config_file.readlines()
        for line in config:
            if not line.startswith('#') and line.startswith('API_KEY'):
                API_KEY = line.split(sep='=')[1].strip()
    if not API_KEY:
        print('Please set an API key in config.ini '
              'or set OPEN_WEATHER_MAP_API_KEY environment variable')
        exit(1)


class WeatherForecast:

    def __init__(self) -> None:
        self._city_cache = {}

    def get_forecast(self, city: str) -> List[Dict[str, str]]:
        if city in self._city_cache:
            print(f"Getting '{city}' forecast from cache")
            return self._city_cache[city]
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"q={city}&units=metric&appid={API_KEY}"
        print("Sending HTTP request")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        forecast_data = data["list"]
        forecast = [
            {
                "datetime": str(parse(daytime_data["dt_txt"])),
                "temp_max": str(daytime_data["main"]["temp_max"])
            }
            for daytime_data in forecast_data
        ]
        self._city_cache[city] = forecast
        return forecast


class CityInfo:

    def __init__(self,
                 city: str,
                 weather_forecast=WeatherForecast()) -> None:
        self.city = city
        self._weather_forecast = weather_forecast

    def weather_forecast(self) -> List[Dict[str, str]]:
        return self._weather_forecast.get_forecast(self.city)


def _main() -> None:
    cities = ["Moscow", "Saratov", "Kazan"]
    forecaster = WeatherForecast()
    forecast = {
        city: CityInfo(city, weather_forecast=forecaster).weather_forecast()
        for city in cities
    }

    with open("forecast.txt", "w") as f:
        f.write(json.dumps(forecast, indent=2))

    with open("forecast.txt", "r") as f:
        print(f.read())


if __name__ == "__main__":
    _main()
