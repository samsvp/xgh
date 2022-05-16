#%%
import os
import json
import requests
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from typing import Any, Dict, List, Tuple
import multiprocessing

import utils

history = {}

xmls = ()
dates = ()
data = {}


def get_xmls(url: str, get_all=False) -> \
        Tuple[Tuple[str], Tuple[str]]:
    """
    Get sitemap xml
    """
    response = requests.get(url)
    root = ElementTree.fromstring(response.content)

    xmls, dates = zip(*[(child[0].text, child[1].text) 
            for child in root 
            if get_all or "product" in child[0].text
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
        try:
            product_data = json.loads(script_content)
        except:
            pass

    return product_data



def get_prices(soup: BeautifulSoup) -> Tuple[float, float]:
    """
    Get the price of the product
    """
    # the prices are stored inside the script tags as a json
    price, list_price = -1, -1
    product_data = get_product_data(soup, "fullSellingPrice")
    if product_data:
        # finally get prices and format it to flot
        # if the product is not available a big number is returned
        _price = utils.find_by_key(product_data, "fullSellingPrice").__next__()
        _list_price = utils.find_by_key(product_data, "listPriceFormated").__next__()
        price, list_price = utils.price_to_num(_price), utils.price_to_num(_list_price)

        return price, list_price
    
    # try to find with another key
    product_data = get_product_data(soup, "price")
    if product_data:
        _price = utils.find_by_key(product_data, "price").__next__()
        price = float(_price)
        list_price = price
    
    return price, list_price


def get_gtin(soup: BeautifulSoup) -> int:
    """
    Gets the gtin
    """
    ean = None

    product_data = get_product_data(soup, "productEans")
    if product_data:
        eans = utils.find_by_key(product_data, "productEans").__next__()
        if eans: 
            try:
                ean = int(eans[0])
            except ValueError:
                ean = 0
        return ean

    # second case
    product_data = get_product_data(soup, "gtin13")
    if product_data:
        eans = utils.find_by_key(product_data, "gtin13").__next__()
        try:
            ean = int(eans)
        except ValueError:
            ean = -1
        return ean
    
    return ean
    

def load_json(filename: str) -> Dict[Any, Any]:
    """
    Loads a json with the given file name.
    If no file is found then an empty dict is returned.
    """
    try:
        with open(filename, "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}
    return history


def load_json_tmp(pid: int) -> Dict[Any, Any]:
    try:
        with open(f"data_{pid}.json.tmp", "r", encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = {}
    return history


def update_json(data: Dict[Any, Any], i: str, pid: int) -> Dict[Any, Any]:
    filename = f"data_{pid}.json.tmp"
    history = load_json(filename)
    try:
        if i in history: history[i].update(data)
        else: history[i] = data

        with open(filename, "w", encoding='utf-8') as data_file:
            json.dump(history, data_file, indent=True)
    except Exception as e:
        print(e)

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

        try:
            response = requests.get(prod)
        except Exception as e:
            print(e)
            continue
        
        soup = BeautifulSoup(response.content, "lxml")

        # get gtin and prices
        gtin = get_gtin(soup)
        price, list_price = get_prices(soup)

        # failure cases
        if gtin is None: continue
        if gtin == -1 and price == -1: continue

        data[prod] = {
            "price": price, "list_price": list_price,
            # when list_price is not 0 the product is on sale
            # it stores the price before the sale
            "promo": list_price > 0, 
            "last_mod": date, "GTIN": gtin
        }
        data["last_mod"] = date
        history = update_json(data, str(i), multiprocessing.current_process().pid)
        
        print(f"{prod} has been processed")


if __name__ == "__main__":
    import config

    for name in config.selected_names:
        url = config.urls[name]
        filename = f"{name}_data.json"
        
        history = load_json(filename)

        try:
            xmls, dates = get_xmls(url)
            m_prods_list = get_products_list(xmls)
        except Exception:
            _site, dates = get_xmls(url, True)
            _plist = list(zip(_site, dates))
            step = len(_plist) // 16
            m_prods_list = [_plist[x:x+step] for x in range(0, len(_plist), step)]

        with multiprocessing.Pool(multiprocessing.cpu_count() * 4) as p:
            p.map(check_data, list(enumerate(m_prods_list)))
        
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

