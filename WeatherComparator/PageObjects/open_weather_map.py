from PageBase.network_helper import NetworkHelper
import PageBase.custom_logger as cl
import logging


class WeatherAPI:

    log = cl.custom_logger(logging.INFO)

    def __init__(self):
        self.url = 'http://api.openweathermap.org/data/2.5/weather'
        self.api_key = '7fe67bf08c80ded756e598d6f8fedaea'
        # We should not keep API key in code, it should be fetched from Environment variable
        # of server on which script runs. For now, keeping it here

    def get_temperature(self, city_name):
        """
        To get current temperature of required city from api
        :param city_name: Name of city for which current temperature is required
        :return: Numeric value of current temperature or None if not found
        """
        current_temperature = None
        try:
            self.log.info(f'Getting temperature through Open weather API for city : {city_name}')
            helper = NetworkHelper(f'{self.url}?q={city_name}&appid={self.api_key}&units=metric')
            data = helper.get_data()
            if data:
                weather = data.get('main', None)
                if weather:
                    current_temperature = weather.get('temp', None)
                    self.log.info(f'Got temperature value - {current_temperature} for city - {city_name}')
        except Exception as e:
            self.log.error(f'Unable to get temperature from API due to exception - {e}')
        finally:
            return current_temperature

    def get_humidity(self, city_name):
        """
        To get current humidity of required city from api
        :param city_name: Name of city for which current humidity is required
        :return: Numeric value of current humidity or None if not found
        """
        current_humidity = None
        try:
            self.log.info(f'Getting humidity through Open weather API for city : {city_name}')
            helper = NetworkHelper(f'{self.url}?q={city_name}&appid={self.api_key}&units=metric')
            data = helper.get_data()
            if data:
                weather = data.get('main', None)
                if weather:
                    current_humidity = weather.get('humidity', None)
                    self.log.info(f'Got humidity value - {current_humidity} for city - {city_name}')
        except Exception as e:
            self.log.error(f'Unable to get humidity from API due to exception - {e}')
        finally:
            return current_humidity


