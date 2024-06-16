import requests
from urllib.parse import urlencode
from functools import lru_cache

from LxmlSoup import LxmlSoup
from geopy import Nominatim
from loguru import logger


logger.add("logs/locator.log", format="\n{time} {level} \n{message}\n",
           level="DEBUG", rotation="10 MB", compression="zip")


class Locator:
    POINT_TYPES = [
        "city",
        "town",
        "village",
        "state"
    ]

    @logger.catch
    def get_point_name(self, point: tuple) -> dict:
        """
        Get name of village/town/city/state

        Args:
            point[tuple]: coordinates of point

        Returns:
            name of point -> string
        """
        logger.debug(f"locator.py:22\nget_point_name()\n└ point: {point}")

        # Getting and formating point info
        latitude = point[0]
        longitude = point[1]
        coordinates = f'{latitude} {longitude}'

        # Getting geolocation by Nominatim
        nominatim_locator = Nominatim(user_agent='myencoder', timeout=10)
        location = nominatim_locator.reverse(coordinates, language='ru')

        # Getting the most accurate value
        raw_address = location.raw['address']
        for _type in self.POINT_TYPES:
            if _type in raw_address:
                return {
                    "name": raw_address[_type],
                    "type": _type
                }

    @staticmethod
    @logger.catch
    def get_coordinates(city_name: str) -> list:
        """
        Get coordinates of point

        Args:
            city_name[string]: point

        Returns:
            point coordinates -> list
        """
        logger.debug(f"locator.py:44\nget_coordinates()\n└ city_name: {city_name}")

        # Getting coordinates by Nominatim
        locator = Nominatim(user_agent='myencoder', timeout=10)
        location = locator.geocode(city_name, language='ru')

        return [location.latitude, location.longitude]

    @staticmethod
    @logger.catch
    @lru_cache
    def get_distance(point1: str, point2: str) -> dict[str, int | str]:
        """
        Get distance between 2 cities. The distance data is obtained by parsing the website avtodispetcher.ru

        Args:
            point1: name of first city
            point2: name of second city

        Returns:
            distance -> dict[str, int | str]
        """

        logger.debug(f"locator.py:61\nget_distance()\n└ point 1: {point1}\n└ point 2: {point2}")

        api_url: str = "https://www.avtodispetcher.ru/distance/?"
        params: str = urlencode({
            "to": point2,
            "from": point1
        })

        print(api_url + params)

        html: str = requests.get(api_url + params).text  # HTML code of page

        # Parsing list of steps
        soup = LxmlSoup(str(html))
        lengths = soup.find_all("td", class_="length")

        result = lengths[-1].text().split(" ")  # last item at list

        return {
            "value": int(result[0]),
            "unit": str(result[1])
        }
