import pytest
import PageBase.custom_logger as cl
import logging
from PageObjects.weather import Weather
from PageObjects.open_weather_map import WeatherAPI
import Configuration.config as config

log = cl.custom_logger(logging.INFO)


@pytest.mark.usefixtures('setup', 'page_objects')
class TestComparator:
    @pytest.fixture(scope='class')
    def page_objects(self, request):
        weather = Weather(self.driver)
        weather_api = WeatherAPI()
        request.cls.weather = weather
        request.cls.weather_api = weather_api

    @pytest.mark.parametrize('city', config.cities)
    def test_temperature_variance(self, city):
        """
        Temperature variance - weather.com and openWeatherMap api for different cities:
        """
        self.report_city = city
        temperature_variance = config.acceptable_temperature_variance
        city_temperature_from_web = self.weather.get_temperature(city)
        city_temperature_from_api = self.weather_api.get_temperature(city)

        if not city_temperature_from_api:
            assert False, 'Unable to fetch value from api'
        if not city_temperature_from_web:
            assert False, 'Unable to fetch value from web'

        temperature_difference = abs(city_temperature_from_web - city_temperature_from_api)
        log.info(f'Absolute temperature difference between 2 sources - {temperature_difference}')
        assert (temperature_difference <= temperature_variance) is True, \
            f'Temperature difference - {temperature_difference} is out of acceptable range for {city}'

    @pytest.mark.parametrize('city', config.cities)
    def test_humidity_variance(self, city):
        """
        Humidity variance - weather.com and openWeatherMap api for different cities:
        """
        self.report_city = city
        humidity_variance = config.acceptable_humidity_variance
        city_humidity_from_web = self.weather.get_humidity(city)
        city_humidity_from_api = self.weather_api.get_humidity(city)

        if not city_humidity_from_api:
            assert False, 'Unable to fetch value from api'
        if not city_humidity_from_web:
            assert False, 'Unable to fetch value from web'

        humidity_difference = abs(city_humidity_from_web - city_humidity_from_api)
        log.info(f'Absolute humidity difference between 2 sources - {humidity_difference}')
        assert (humidity_difference <= humidity_variance) is True, \
            f'Temperature difference - {humidity_difference} is out of acceptable range for {city}'
