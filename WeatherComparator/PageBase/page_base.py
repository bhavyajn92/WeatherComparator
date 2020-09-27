from enum import Enum
import time
import PageBase.custom_logger as cl
import logging
from selenium.webdriver.common.by import By
from retry import retry
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains

class PageBase:

    log = cl.custom_logger(logging.INFO)

    def __init__(self, driver):
        self.driver = driver

    def open(self, url, wait_time=2):
        """
        Visit the url
        :param url: URL to be opened
        :param wait_time: time to wait till url opens
        :return:
        """
        self.driver.get(url)
        self.sleep_in_seconds(wait_time)

    @retry(StaleElementReferenceException, tries=5, delay=2)
    def click(self, locator):
        """
        Clicks the given element
        :param locator: Element locator strategy
        :return: element
        """
        element = None
        if isinstance(locator, str):
            element = self.find_element(locator)
        elif isinstance(locator, WebElement):
            element = locator
        if element is not None:
            element.click()
        else:
            raise Exception("Could not click on locator ")

    def get_text(self, locator):
        """
        Get  the inner text of given element
        :param locator: Element locator strategy
        :return: text
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.find_element(locator)
        return element.text

    @retry(NoSuchElementException, tries=2, delay=2)
    def find_element(self, locator):
        """
        Find and return element based on the given locator value
        E.g: draggableElement = ("xpath@@//div[@id='draggable']")
        :param locator: Element locator strategy
        :return: Element
        """
        return self.driver.find_element(*self.__get_by(locator_with_strategy=locator))

    def __get_by(self, locator_with_strategy):
        """
        Get and return By instance based on the locator strategy
        :param locator_with_strategy: Element locator strategy
        :return: By instance of the element
        """
        if "@@" not in locator_with_strategy:
            locator_with_strategy = Strategy.ID.value + "@@" + locator_with_strategy

        strategy_and_locator = str(locator_with_strategy).split("@@")
        strategy = strategy_and_locator[0]
        locator = strategy_and_locator[1]
        by = None
        if strategy == Strategy.XPATH.value:
            by = (By.XPATH, locator)
        elif strategy == Strategy.ID.value:
            by = (By.ID, locator)
        elif strategy == Strategy.CSS.value:
            by = (By.CSS_SELECTOR, locator)
        elif strategy == Strategy.TAGNAME.value:
            by = (By.TAG_NAME, locator)
        return by

    def sleep_in_seconds(self, seconds=1):
        """
        Method for hard wait as per given seconds
        :param seconds: time in seconds
        :return:
        """
        time.sleep(seconds)

    def send_keys(self, locator, *keys):
        """
        send keys to locator
        :param locator: element
        :param wait_time: time to wait
        :return:
        """
        element = self.wait_till_element_is_present(locator)
        try:
            element.send_keys(*keys)
        except Exception as e:
            raise e

    def wait_till_element_is_present(self, locator, timeout=5):
        """
        WebDriver Explicit wait till element is present
        :param locator: element to be checked
        :param timeout: timeout
        :return:
        """
        try:
            element = WebDriverWait(self.driver, timeout). \
                until(EC.presence_of_element_located(self.__get_by(locator)))
            return element
        except Exception as e:
            raise e

    def wait_till_element_is_clickable(self, locator, timeout=60):
        """
        WebDriver Explicit wait till element is clickable
        :param locator: element to be checked
        :param timeout: timeout
        :return:
        """
        try:
            element = WebDriverWait(self.driver, timeout). \
                until(EC.element_to_be_clickable(self.__get_by(locator)))
            return element
        except Exception as e:
            raise e

    def teardown_browser(self):
        """
        Close all browser instances
        :return:
        """
        self.driver.quit()

    def maximize_browser(self):
        """
        Maximize the browser
        :return:
        """
        self.driver.maximize_window()

    def back(self):
        """
        browser back button
        :return:
        """
        self.driver.back()

    def move_and_click(self, locator):
        """
        Move and click to the given element using
        selenium action class
        :param locator: Element locator strategy
        :return: element
        """
        if isinstance(locator, WebElement):
            element = locator
        else:
            element = self.find_element(locator)
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element).click().perform()
        except Exception as e:
            raise Exception("Could Not click locator {} due to {}".format(element, e))
        return element


class Strategy(Enum):
    """
    Locator Strategy Constants
    """
    XPATH = "xpath"
    ID = "id"
    CSS = "css"
    TAGNAME = "tag name"
