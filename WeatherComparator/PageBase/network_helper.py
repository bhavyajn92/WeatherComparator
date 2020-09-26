import requests


class NetworkHelper:

    def __init__(self, url):
        self.url = url

    def get_data(self):
        """
        To get API response body
        :return: Dictionary of response data
        """
        response = requests.get(self.url)
        response_status = response.status_code
        if response_status == 200:
            data = response.json()
            return data
        else:
            print(response_status)
