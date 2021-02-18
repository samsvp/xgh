from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from time import sleep

driver = webdriver.Chrome("C:/Users/Raisa/Desktop/chromedriver")
driver.get("https://www.teleco.com.br/rtv.asp")

print(driver.execute_script("return window.name"))

# get the states dropdown
states_select = Select(driver.find_element_by_id('estado_tva'))

#%%
states_dict = {}
for _state in states_select.options:
    # loop through every state
    state = _state.text
    if (len(state) > 2): continue
    states_dict[state] = {}
    print(state)
    sleep(0.1)
    states_select.select_by_visible_text(state)
    sleep(1) # wait for the site to update
    county_select = Select(driver.find_element_by_id('cidades_tva'))
    for i in range(len(county_select.options)):
        # loop through every county
        try:
            count_text = county_select.options[i].text
            print(count_text)
            states_dict[state][count_text] = []
            county_select.select_by_index(i)
            driver.find_elements_by_name("Submit")[1].click()

            # must switch windows to get the the data
            driver.switch_to.window(driver.window_handles[1])
            # get all table rows
            rows = driver.find_elements_by_tag_name("tr")
            # find the table row containing "OI"
            for row in rows:
                col = row.find_elements_by_tag_name("td")
                if (len(col) != 3): continue
                states_dict[state][count_text].append([c.text for c in col])
            driver.switch_to.window(driver.window_handles[0])
            # for some reason it needs to run once with both break statements
            # and then again without it
            # break
        except:
            continue
    # break
    print()
    #states_select.select_by_value(state.text)
