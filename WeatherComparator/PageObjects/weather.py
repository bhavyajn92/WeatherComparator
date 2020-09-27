from PageBase.page_base import PageBase
from Locators import locators
from retry import retry
from selenium.common.exceptions import StaleElementReferenceException, ElementNotInteractableException


class Weather(PageBase):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @retry((ElementNotInteractableException, StaleElementReferenceException), tries=5, delay=1)
    def search_city(self, city_name):
        """
        To search city on weather.com website
        :param city_name: Name of city for which weather needs to be searched
        :return: True if able to find weather info, else return False
        """
        web_url = 'https://weather.com/en-IN/'
        self.log.info(f'Opening {web_url} website')
        self.open(web_url)
        self.log.info(f'Searching city name : {city_name}')
        self.send_keys(locators.search_box, city_name)
        # self.sleep_in_seconds(2)
        self.wait_till_element_is_present(locators.search_results)
        search_result = self.find_element(locators.select_search_result)
        self.log.info('Search result found')
        self.move_and_click(search_result)
        # self.click(search_result)
        self.wait_till_element_is_present(locators.current_weather)
        self.log.info(f'{city_name} found')
        return True

    def get_temperature(self, city_name):
        """
        To get current temperature of required city
        :param city_name: Name of city for which current temperature is required
        :return: Numeric value of current temperature or None if not found
        """
        current_temperature = None
        try:
            if self.search_city(city_name):
                current_temperature = self.get_text(locators.current_temperature)
                current_temperature = int(current_temperature.replace('°', ''))
                self.log.info(f'Got current temperature value as {current_temperature} for city - {city_name}')
        except Exception as e:
            self.log.error(f'Current temperature value not found for city - {city_name} with exception - {e}')
        finally:
            return current_temperature

    def get_humidity(self, city_name):
        """
        To get current humidity of required city
        :param city_name: Name of city for which current humidity is required
        :return: Numeric value of current humidity or None if not found
        """
        current_humidity = None
        try:
            if self.search_city(city_name):
                current_humidity = self.get_text(locators.current_humidity)
                current_humidity = int(current_humidity.replace('%', ''))
                self.log.info(f'Got current humidity value as {current_humidity} for city - {city_name}')
        except Exception as e:
            self.log.error(f'Current humidity value not found for city - {city_name} with exception - {e}')
        finally:
            return current_humidity


