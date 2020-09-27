Pre-requisites:
1. Python3 should be installed
2. pip should be installed
3. Chrome version 85 should be installed
4. Firefox version 81 should be installed if you want to run script on firefox
5. Windows platform

Script configurations:
 - Below three variables have been made configurable in config.py file in Configuration folder - 
    acceptable_temperature_variance - Accepts numeric value, defines the permissible variance between temperatures 
    acceptable_humidity_variance = Accepts numeric value, defines the permissible variance between humidity
    cities = Accept list of valid cities

How to run automation script: 
1. Go to Folder WeatherComparator where readme file is located
2. Run command - "pip install -r requirements.txt" to install dependencies
3. Run below command to execute the suite on chrome browser
    py.test -B chrome --html=Reports/TestResults.html --self-contained-html
    (Replace chrome with firefox to execute script on Firefox browser)
4. Chrome browser will open up and script will start executing. 
5. On script completion, HTML report will be generated in Reports folder. 

Approach to problem: 

1. Created Parent classes having helper functions - PageBase.py and network_helper.py in PageBase folder
2. Created a Custom Logger class in PageBase folder to create logs in Logs folder.
3. Crated a WebDriver class in Webdriver.py to create driver objects
4. Created a Weather class in PageObjects/weather.py to fetch climate values from weather.com
5. Created another class in PageObjects/open_weather_map.py to fetch climate values from open weather map api
6. Created a test class in TestCases/test_comparator.py to check the variance between above two objects.
7. Kept chrome and firefox web drivers in WebDrivers folder, but they should not be kept in project structure and should be fetched from server machine.
8. Added a gitignore file for ignoring logs and report on git
9. Added conftest.py to add fixtures for creating driver objects, tearing down browser and generating custom html reports
10. Added a requirements.txt for installing dependencies
11. Have kept locators in separate Locators folder.


Why this framework - 

I have used py.test framework for this project as it is easy to write small tests and also support complex functionality testing for applications.
It supports a lot of fixtures which reduces a lot of coding efforts and even supports page object model.
Like in this project, it was very minimal effort to run same test case on multiple cities with the help of a simple parameterize fixture. Check test_comparator.py in TestCases for this.
Also, this framework supports parallel execution of test cases which eventually reduces execution time.



























