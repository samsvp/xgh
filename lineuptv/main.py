# %%
import json
import requests
from bs4 import BeautifulSoup, element

from typing import List, Dict

url = "https://lineup.tv.br/"

def save_cities(cities: Dict[str, Dict[str, Dict[str, str]]]):
    with open("cities.json", "w", encoding="utf8") as f:
        json.dump(cities, f, ensure_ascii=False, indent=4)

def get_page(url: str) -> BeautifulSoup:
    r = requests.get(url)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "lxml")
    return soup

def get_channels_tables(url: str) -> List[element.Tag]:
    soup = get_page(url)
    divs = soup.find_all("div", {"class": "text"})
    channels = {}
    for div in divs:
        t = div.find_all("div", {"class": "titulo"}) 
        if len(t) == 1 and t[0].text in ("TV Digital", "TV Analógica"):
            tr = div.find_all("tr")[1:]
            channels[t[0].text] = tr
    return channels

def get_channels_resources(channels: List[element.Tag]) -> Dict[str, List[str]]:
    channels_resources = {}
    for tv_type, tr in channels.items():
        channels_resources[tv_type] = {}
        for c in channels[tv_type]:
            tds = c.find_all("td")[1:3]
            try:
                channels_resources[tv_type][tds[0].find("a").text] = [imgs.get("src").split("/")[-1][:-4] 
                    for imgs in tds[1].find_all("img")]
            except AttributeError:
                channels_resources[tv_type][tds[0].find("div").text] = [imgs.get("src").split("/")[-1][:-4] 
                    for imgs in tds[1].find_all("img")]
    return channels_resources

def scrape_cities(soup: BeautifulSoup) -> Dict[str, Dict[str, Dict[str, str]]]:
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
    soup = get_page(url)
    states_cities_district = scrape_cities(soup)
    save_cities(states_cities_district)


if __name__ == "__main__":
    main()