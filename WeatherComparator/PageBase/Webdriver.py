from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os


class GetWebDriver:

    @staticmethod
    def get_web_driver(browser):
        if browser.lower() == 'firefox':
            return webdriver.Firefox(executable_path=os.path.join(os.path.abspath(__file__ + "/../../"),
                                                                  "WebDrivers\\geckodriver.exe"))

        elif browser.lower() == 'chrome':
            chrome_options = webdriver.ChromeOptions()
            preferences = {'safebrowsing.enabled': 'false'}
            desired_capabilities = DesiredCapabilities.CHROME
            desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}
            chrome_options.add_experimental_option("prefs", preferences)
            return webdriver.Chrome(os.path.join(os.path.abspath(__file__ + "/../../"), "WebDrivers\\chromedriver.exe"),
                                    chrome_options=chrome_options, desired_capabilities=desired_capabilities)
