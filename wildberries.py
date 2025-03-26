import requests
from urllib.parse import urlparse, urlencode

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

def get_products_by_search_query(query, page_number = 1):
    parameters = {
        "ab_testing": False,
        "appType": 1,
        "curr": "rub",
        "dest": -1257786,
        "hide_dtype": 10,
        "lang": "ru",
        "page": page_number,
        "query": query,
        "resultset": "catalog",
        "sort": "popular",
        "spp": 30,
        "suppressSpellcheck": False,
    }

    response = requests.get(f"https://search.wb.ru/exactmatch/ru/common/v9/search?{urlencode(parameters)}").json()
    
    return response["data"]["products"]

def get_product_position_by_query(id, query):
    page_number = 1

    while True:
        products = get_products_by_search_query(query, page_number)
        products_ids = [product["id"] for product in products]

        try:
            index = products_ids.index(id)

            product_position = ((page_number - 1) * 100) + (index + 1)
            return product_position
        except ValueError:
            page_number = page_number + 1
