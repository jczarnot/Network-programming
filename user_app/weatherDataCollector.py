import requests
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError


class WeatherDataCollector:
    def __init__(self, url):
        self.url = url

    def get_all_recent_data(self):
        try:
            url = self.url + '/0/0'
            weather_data = requests.get(url, verify=False)
            weather_data.raise_for_status()

            return weather_data.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return -1
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            return -1
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')
            return -1

    def get_data_from_id_range(self, start_id, end_id):
        try:
            url = self.url + '/' + start_id + ':' + end_id + '/' + '0'
            weather_data = requests.get(url, verify=False)
            weather_data.raise_for_status()

            return weather_data.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return -1
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            return -1
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')
            return -1

    def get_data_from_date_range(self, start_date, end_date):
        try:
            url = self.url + '/0/' + start_date + ':' + end_date
            weather_data = requests.get(url, verify=False)
            weather_data.raise_for_status()

            return weather_data.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return -1
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            return -1
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')
            return -1

    def get_data_from_id_date_range(self, start_id, end_id, start_date, end_date):
        try:
            url = self.url + '/' + start_id + ':' + end_id + '/' + start_date + ':' + end_date
            weather_data = requests.get(url, verify=False)
            weather_data.raise_for_status()

            return weather_data.json()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return -1
        except ConnectionError as conn_err:
            print(f'Connection error occurred: {conn_err}')
            return -1
        except requests.exceptions.RequestException as e:
            print(f'Error occurred: {e}')
            return -1
