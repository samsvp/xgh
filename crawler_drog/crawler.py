#%%
import os
import json
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Tuple
import multiprocessing

import utils
import config

history = {}

xmls = ()
dates = ()
data = {}

filename = ""

def get_xmls(url: str) -> Tuple[Tuple[str], Tuple[str]]:
    """
    Get sitemap xml
    """
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)

    xmls, dates = zip(*[(child[0].text, child[1].text) 
            for child in root if "product" in child[0].text
        ]) # filter the products xml
    return xmls, dates


def get_products_list(xmls: List[str]) -> List[List[Tuple[str, str]]]:
    """
    Gets the list of products to crawl
    """
    prods_list = []
    for i, xml in enumerate(xmls):
        response = requests.get(xml)
        root = ElementTree.fromstring(response.content)
        prods = [(child[0].text, child[1].text) for child in root]
        prods_list.append(prods)
        print(f"{i} out of {len(xmls)} processed")
    return prods_list


def get_product_data(soup: BeautifulSoup, key: str) -> Dict[str, Any]:
    """
    Product data is stored in jsons inside script tags.
    This finds the script tag with the given key
    and returns the desired product info as a dict
    """
    product_data = {}

    script = next((s for s in soup.find_all("script") 
                    if s.string and key in s.string), None)
    if script:
        # start and end of json
        start, end = script.string.find("{"), script.string.rfind("}") + 1
        script_content = script.string[start:end]
        # json string to dict
        product_data = json.loads(script_content)

    return product_data


def get_prices(soup: BeautifulSoup) -> Tuple[float, float]:
    """
    Get the price of the product
    """
    # the prices are stored inside the script tags as a json
    price, list_price = 0, 0
    product_data = get_product_data(soup, "fullSellingPrice")
    if product_data:
        # finally get prices and format it to flot
        # if the product is not available a big number is returned
        _price = utils.find_by_key(product_data, "fullSellingPrice").__next__()
        _list_price = utils.find_by_key(product_data, "listPriceFormated").__next__()
        price, list_price = utils.price_to_num(_price), utils.price_to_num(_list_price)
    
    return price, list_price


def get_gtin(soup: BeautifulSoup) -> str:
    """
    Gets the grin
    """
    ean = None

    product_data = get_product_data(soup, "productEans")
    if product_data:
        eans = utils.find_by_key(product_data, "productEans").__next__()
        if eans: ean = eans[0]
    
    return ean


def check_data(prods_list: Tuple[int, List[str]]) -> None:
    global history, data
    
    i, prods = prods_list
    pid = multiprocessing.current_process().pid

    if str(i) in history:
        if dates[i] == history[str(i)].get("last_mod", ""):
            return
        
    for prod, date in prods:
        if str(i) in history and date == history[str(i)].get(prod, {}).get("last_mod", None):
            continue

        try:
            response = requests.get(prod)
        except Exception as e:
            print(e)
            with open(f".errors_{pid}.txt", 'a+') as f:
                f.write(f"{e}\n{'*' * 20}\n")
            continue

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
        history = utils.update_json(data, str(i), pid, filename)
        
        print(f"{prod} has been processed")


if __name__ == "__main__":
    for name in config.selected_names:
        print(f"Processing {name}")
        url = config.urls[name]
        filename = f"{name}_data.json"
        
        history = utils.load_json(filename)
        xmls, dates = get_xmls(url)

        m_prods_list = get_products_list(xmls)

        with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
            p.map(check_data, list(enumerate(m_prods_list)))
        
        # merge files
        # temp file names
        tmp_jsons_names = [f for f in os.listdir() if f.endswith(".tmp")]

        # merge all data
        all_data = {}
        for tmp in tmp_jsons_names:
            with open(tmp, "r") as file:
                m_data = (json.load(file))
            all_data.update(m_data)

        with open(filename, "w") as f:
            json.dump(all_data, f)

        # remove temp files
        for tmp in tmp_jsons_names: os.remove(tmp)

        # check for errors
        tmp_error_names = [f for f in os.listdir() if f.startswith(".errors")]
        error_string = ""
        
        for tmp_error in tmp_error_names:
            with open(tmp_error) as f:
                error_string += f.read() + "\n"
                
        with open("errors.txt", "w") as f:
            f.write(error_string)

        for tmp in tmp_error_names: os.remove(tmp)
        

