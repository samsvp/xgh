#%%
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import *
from typing import *

import warnings
warnings.filterwarnings('ignore')

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(
    executable_path="./geckodriver", options=options)
driver.get("https://simmao.pmpas-bs.eco.br/panel")
# %%
def get_target_elements(driver):
    mclass = "leaflet-marker-icon leaflet-zoom-hide leaflet-interactive"
    elements = driver.find_elements_by_css_selector(
        f'.{mclass.replace(" ", ".")}')
    return elements

#click on glider/profiler
def click_on_img(driver, i: int) -> None:
    elements = get_target_elements(driver)
    elements[i].click()


def get_enabled(driver) -> Tuple[str, bool]:
    # get name
    id = "contained-modal-title-lg"
    title = driver.find_element_by_id(id).get_attribute(
        'innerHTML')
    # check if profile is available
    mclass = "nav nav-tabs"
    lst = driver.find_element_by_css_selector(
        f'.{mclass.replace(" ", ".")}')
    profile_ts = lst.find_elements_by_tag_name("li")[-1]
    return (
        title,
        profile_ts.get_attribute("class") != "disabled")
  
#click close button
def close(driver) -> None:
    mclass = "btn btn-default"
    elements = driver.find_elements_by_css_selector(
        f'.{mclass.replace(" ", ".")}')

    for element in elements:
        if element.get_attribute('innerHTML') == "Fechar":
            element.click()
            break

# %%
history = []
can_not_click = []
scroll_error = []
for i in range(len(get_target_elements(driver))):
    try:
        click_on_img(driver, i)
    except ElementClickInterceptedException:
        can_not_click.append((i,
            get_target_elements(driver)[i]))
        print("Intersected")
        continue
    except ElementNotInteractableException:
        scroll_error.append(i)
        print("can not scroll")
        continue
    while True:
        try:
            title, is_enabled = get_enabled(driver)
            history.append((title, is_enabled))
            break
        except:
            # wait for site to load
            sleep(1)
    close(driver)
    print(i)
    sleep(1)

can_not_click_idx = [v[0] for v in can_not_click]    
# %%

for i in range(len(get_target_elements(driver))):
    if i not in scroll_error and i not in can_not_click_idx:
        continue

    try:
        click_on_img(driver, i)
    except ElementClickInterceptedException:
        print("Intersected")
        continue
    except ElementNotInteractableException:
        print("can not scroll")
        continue
    while True:
        try:
            title, is_enabled = get_enabled(driver)
            history.append((title, is_enabled))
            break
        except:
            # wait for site to load
            sleep(1)
    close(driver)
    print(i)
    
    if i in can_not_click_idx:
        can_not_click_idx.remove(i)
    elif i in scroll_error:
        scroll_error.remove(i)
    
    sleep(1)
# %%
