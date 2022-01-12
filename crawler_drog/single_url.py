######################
# Used for test only #
######################

# %%
import requests
from bs4 import BeautifulSoup

from crawler import get_xmls, get_gtin, \
    get_products_list, get_prices, get_product_data

#%%
target_url = "https://www.farmaciaindiana.com.br/sitemap.xml"

xmls, dates = get_xmls(target_url)
products = get_products_list(xmls)
# %%
prod = products[0][0][0]
response = requests.get(prod)
soup = BeautifulSoup(response.content, "lxml")
gtin = get_gtin(soup)
prices = get_prices(soup)
print(gtin, prices)
# %%
