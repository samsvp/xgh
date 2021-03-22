# %%
import json
import requests
from bs4 import BeautifulSoup

from typing import Dict

url = "https://lineup.tv.br/"

def save_cities(cities: Dict[str, Dict[str, Dict[str, str]]]):
    with open("cities.json", "w", encoding="utf8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=4)

def get_page() -> BeautifulSoup:
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def scrape_for_cities(soup: BeautifulSoup) -> Dict[str, Dict[str, Dict[str, str]]]:
    menu = soup.find("ul", {"id": "menu"})
    regions_li = menu.find_all("li", {"class": "parent"})[2:7]
    regions_state_ul = {region.find("a").text: region.find("ul", {"class": "sub-menu"}) 
        for region in regions_li}
    
    districts_states_li = {
        region : {
            parent_li.find("a").text: parent_li.find("ul", {"class": "sub-menu2"})
            for parent_li in regions_state_ul[region].find_all("li", {"class": "parent2"})
        }
        for region in regions_state_ul    
    }

    states_cities_district = {
        region : {
            state : {
                district_li.find_all("a")[-1].text[2:] : # remove "- "
                    f"{url}{district_li.find_all('a')[-1].get('href')}"
                for district_li in sub_menu_2.find_all("li")
            }
            for state, sub_menu_2 in state_menus_2.items()
        }
        for region, state_menus_2 in districts_states_li.items()
    }

    return states_cities_district


def main():
    soup = get_page()
    states_cities_district = scrape_for_cities(soup)
    save_cities(states_cities_district)


if __name__ == "__main__":
    main()