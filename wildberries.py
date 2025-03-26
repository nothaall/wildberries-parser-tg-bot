import requests
from urllib.parse import urlparse, urlencode

def get_product_id_by_url(url):
    return int(urlparse(url).path.split("/")[2])

basket_steps = [143, 287, 431, 719, 1007, 1061, 1115, 1169, 1313, 1601, 1655, 1919, 2045]

def get_basket_number_by_vol(vol):
    basket_number = 1

    for step in basket_steps:
        if vol >= step + 1:
            basket_number = basket_number + 1
        else:
            break
    
    return basket_number

def get_product_by_id(id):
    vol = int(str(id)[0:4])
    part = int(str(id)[0:6])
    basket_number = get_basket_number_by_vol(vol)
    formatted_basket_number = str(basket_number)

    if basket_number < 10:
        formatted_basket_number = f"0{formatted_basket_number}"

    card_url = f"https://basket-{formatted_basket_number}.wbbasket.ru/vol{vol}/part{part}/{id}/info/ru/card.json"

    response = requests.get(card_url).json()

    return {
        "id": id,
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
