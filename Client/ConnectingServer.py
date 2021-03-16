import requests
import datetime
import json
from json import JSONEncoder


# Преобразовать в json
class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class ConnectingServer:
    def __init__(self, url):
        self.url = url
        self.session = requests.Session()

    def connect_user(self, login, password):
        answer = self.session.get(f'{self.url}/login_user', json={'login': login, 'password': password})
        return answer

    def register_user(self, login, password):
        answer = self.session.get(f'{self.url}/register_user', json={'login': login, 'password': password})
        return answer

    def add_product(self, key_user, name_product, price_product, data_purchase):
        json_sent = json.dumps({'key_user': key_user,
                                'date_purchase': data_purchase,
                                'name_product': name_product,
                                'price_product': price_product}, indent=4, cls=DateTimeEncoder)
        answer = self.session.get(f'{self.url}/add_product', json=json_sent)
        return answer

    def get_products(self, key_user):
        answer = self.session.get(f'{self.url}/get_list_products', json={'key_user': key_user})
        return answer

    def remove_product(self, key_user, id_product):
        answer = self.session.get(f'{self.url}/delete_product', json={'key_user': key_user, 'id_product': id_product})
        return answer

    def remove_user(self, key_user):
        answer = self.session.get(f'{self.url}/delete_user', json={'key_user': key_user})
        return answer

    def edit_product(self, key_user, product_id, name_product, price_product, data_purchase):
        json_sent = json.dumps({'key_user': key_user,
                                'id_product': product_id,
                                'date_purchase': data_purchase,
                                'name_product': name_product,
                                'price_product': price_product}, indent=4, cls=DateTimeEncoder)
        answer = self.session.get(f'{self.url}/edit_product', json=json_sent)
        return answer

