# %%
import json
import requests
from bs4 import BeautifulSoup, element

from typing import List, Dict, Any

url = "https://lineup.tv.br/"

def save_json(name: str, data: Dict[Any, Any]):
    with open(name, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def save_cities(cities: Dict[str, Dict[str, Dict[str, str]]]):
    save_json("cities.json", cities)

def load_cities() -> Dict[str, Dict[str, Dict[str, str]]]:
    with open("cities.json", encoding="utf8") as f:
        data = json.load(f)
    return data

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

def scrape_channels(states_cities_district: Dict[str, Dict[str, Dict[str, str]]]) -> \
        Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, List[str]]]]]]:
    data = {
        region: {
            state: {
                district: get_channels_resources(get_channels_tables(url))
                for district, url in districts.items()
            }
            for state, districts in states.items()
        }
        for region, states in states_cities_district.items()
    }
    return data

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
    # get all links
    # soup = get_page(url)
    # states_cities_district = scrape_cities(soup)
    # save_cities(states_cities_district)

    # get channels and resources from link
    states_cities_district = load_cities()
    data = scrape_channels(states_cities_district)
    save_json("linuuptv_channel_data.json", data)

if __name__ == "__main__":
    main()
# %%
