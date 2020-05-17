"""Simple forecast module which uses OpenWeatherMap API
"""

from typing import List, Dict
import json
import requests
from dateutil.parser import parse


class WeatherForecast:

    def __init__(self) -> None:
        self._city_cache = {}

    def get_forecast(self, city: str) -> List[Dict[str, str]]:
        if city in self._city_cache:
            print(f"Getting '{city}' forecast from cache")
            return self._city_cache[city]
        url = f"https://api.openweathermap.org/data/2.5/forecast?" \
              f"q={city}&units=metric&appid=967e0644610deec378355a38548a57ee"
        print("Sending HTTP request")
        data = requests.get(url).json()
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
