#%%
import json
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Tuple
import multiprocessing


lock = multiprocessing.Lock()

def find_by_key(data: Dict[Any, Any], target: Any) -> Any:
    """
    Finds the target key given a nested dictionary
    """
    for key, value in data.items():
        if key == target:
            yield value
        if isinstance(value, dict):
            yield from find_by_key(value, target)
        elif isinstance(value, list):
            for v in value:
                if isinstance(v, dict):
                    yield from find_by_key(v, target)


def price_to_num(price: str) -> float:
    """
    Converts a price string (format-> "R$ 5.555,99") into a float
    """
    return float(price[3:].replace(".","").replace(",","."))


def get_xmls(url: str) -> Tuple[Tuple[str], Tuple[str]]:
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)

    xmls, dates = zip(*[(child[0].text, child[1].text) 
            for child in root if "product" in child[0].text
        ])
    return xmls, dates


def get_products_list(xmls: List[str]) -> List[List[str]]:
    prods_list = []
    for i, xml in enumerate(xmls):
        response = requests.get(xml)
        root = ElementTree.fromstring(response.content)
        prods = [(child[0].text, child[1].text) for child in root]
        prods_list.append(prods)
        print(f"{i} out of {len(xmls)} processed")
    return prods_list


def get_prices(soup: BeautifulSoup):
    # the prices are stored inside the script tags as a json
    script = next((s for s in soup.find_all("script") 
                    if s.string and "fullSellingPrice" in s.string), None)
    # start and end of json
    start, end = script.string.find("{"), script.string.rfind("}") + 1
    script_content = script.string[start:end]
    # json string to dict
    m_dict = json.loads(script_content)
    
    # finally get prices and format it to flot
    _price = find_by_key(m_dict, "fullSellingPrice").__next__()
    _list_price = find_by_key(m_dict, "listPriceFormated").__next__()
    price, list_price = price_to_num(_price), price_to_num(_list_price)
    
    return price, list_price


def get_gtin(soup: BeautifulSoup) -> int:
    if s:= (soup.find("meta", itemprop="ean") or 
            soup.find("meta", itemprop="gtin13")):
        return int(s["content"])
    

def load_json() -> Dict[Any, Any]:
    try:
        with open("data.json", "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}
    return history


def update_json(data: Dict[Any, Any], i: str) -> Dict[Any, Any]:
    lock.acquire()

    try:
        history = load_json()
        if i in history: history[i].update(data)
        else: history[i] = data

        with open("data.json", "w", encoding='utf-8') as data_file:
            json.dump(history, data_file, indent=True)
    finally:
        lock.release()    
    
    return history

def check_data(prods_list: Tuple[int, List[str]]) -> None:
    global history, data
    i, prods = prods_list
    
    if str(i) in history:
        if dates[i] == history[str(i)].get("last_mod", ""):
            return
        
    for prod, date in prods:
        if str(i) in history and date == history[str(i)].get(prod, {}).get("last_mod", None):
            continue

        response = requests.get(prod)
        soup = BeautifulSoup(response.content, "lxml")

        # get gtin and prices
        gtin = get_gtin(soup)
        price, list_price = get_prices(soup)

        data[prod] = {
            "price": price, "list_price": list_price,
            # when list_price is not 0 the product is on sale
            # it stores the price before the sale
            "promo": list_price > 0, 
            "last_mod": date, "GTIN": gtin
        }
        data["last_mod"] = date
        history = update_json(data, str(i))
        
        print(f"{prod} has been processed")


url = "https://www.drogariavenancio.com.br/sitemap.xml"
history = load_json() 

xmls, dates = get_xmls(url)
data = {}

if __name__ == "__main__":
    m_prods_list = get_products_list(xmls)

    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(check_data, list(enumerate(m_prods_list)))
    
