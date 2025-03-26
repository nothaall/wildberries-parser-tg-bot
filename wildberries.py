import requests
from urllib.parse import urlparse

def get_product_id_by_url(url):
    return int(urlparse(url).path.split("/")[2])

def get_product_by_id(id):
    vol = str(id)[0:4]
    part = str(id)[0:6]
    card_url = f"https://basket-15.wbbasket.ru/vol{vol}/part{part}/{id}/info/ru/card.json"

    response = requests.get(card_url).json()

    return {
        "name": response["imt_name"],
        "description": response["description"]
    }

def get_product_by_url(url):
    id = get_product_id_by_url(url)

    return get_product_by_id(id)
