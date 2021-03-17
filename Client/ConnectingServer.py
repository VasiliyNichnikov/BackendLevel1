import requests
import datetime
from requests.exceptions import HTTPError, ConnectionError


def date_time_encoder(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()


class ConnectingServer:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def connect_user(self, login, password):
        return self.__request_server(f'{self.url}/login_user', {'login': login, 'password': password})

    def register_user(self, login, password):
        return self.__request_server(f'{self.url}/register_user', {'login': login, 'password': password})

    def add_product(self, key_user, name_product, price_product, date_purchase):
        return self.__request_server(f'{self.url}/add_product', {'key_user': key_user,
                                                                 'date_purchase': date_time_encoder(date_purchase),
                                                                 'name_product': name_product,
                                                                 'price_product': price_product})

    def get_products(self, key_user):
        return self.__request_server(f'{self.url}/get_list_products', {'key_user': key_user})

    def remove_product(self, key_user, id_product):
        return self.__request_server(f'{self.url}/delete_product', {'key_user': key_user, 'id_product': id_product})

    def remove_user(self, key_user):
        return self.__request_server(f'{self.url}/delete_user', {'key_user': key_user})

    def edit_product(self, key_user, product_id, name_product, price_product, date_purchase):
        return self.__request_server(f'{self.url}/edit_product', {'key_user': key_user,
                                                                  'id_product': product_id,
                                                                  'date_purchase': date_time_encoder(date_purchase),
                                                                  'name_product': name_product,
                                                                  'price_product': price_product})

    def __request_server(self, source, json_sent):
        try:
            answer = self.session.get(source, json=json_sent)
            return {'condition': 'success', 'result': answer}
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        except ConnectionError as connection_error:
            print(f'Connection error: {connection_error}')
        return {'condition': 'error'}
