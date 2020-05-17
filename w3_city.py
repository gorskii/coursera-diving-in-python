"""Simple forecast module which uses OpenWeatherMap API
"""

import pprint
import requests
from dateutil.parser import parse


class WeatherForecast:

    def __init__(self):
        self._city_cache = {}

    def get(self, city):
        if city in self._city_cache:
            return self._city_cache[city]
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"q={city}&units=metric&appid=967e0644610deec378355a38548a57ee"
        print("Sending HTTP request")
        data = requests.get(url).json()
        forecast_data = data["list"]
        forecast = []
        for daytime_data in forecast_data:
            forecast.append({
                "datetime": parse(daytime_data["dt_txt"]),
                "high_temp": daytime_data["main"]["temp_max"]
            })
        self._city_cache[city] = forecast
        return forecast


class CityInfo:

    def __init__(self, city: str, weather_forecast=None):
        self.city = city
        self._weather_forecast = weather_forecast or WeatherForecast()

    def weather_forecast(self):
        return self._weather_forecast.get(self.city)


def _main():
    forecast = {}
    weather_forecast = WeatherForecast()
    for city in ["Moscow", "Saratov", "Kazan"]:
        for _ in range(5):
            city_info = CityInfo(city, weather_forecast=weather_forecast)
            forecast[city] = city_info.weather_forecast()

    with open("forecast.txt", "w") as f:
        for key, value in forecast.items():
            f.write(str(key) + ": " + str(value))  # TODO fix file output format

    with open("forecast.txt", "r") as f:
        pprint.pprint(f.read())


if __name__ == "__main__":
    _main()
