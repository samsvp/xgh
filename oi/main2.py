#%%
import re
import gzip
import json
import time
from math import isnan
import pandas as pd
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options


#%%
df = pd.read_excel("Controle Contratos Oi.xlsx")

contracts = df.iloc[3:,0]
hotels = df.iloc[3:,1]
cpf_cnpjs = df.iloc[3:,2]

data = {}
for i in range(3, hotels.size):
    hotel = hotels[i]
    cnpj = cpf_cnpjs[i]
    if type(hotel)==float or type(cnpj)==float:
        continue
    if hotel in data:
        data[hotel].append(cnpj)
    else:
        data[hotel] = [cnpj]
# %%
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)

url = "https://www.oi.com.br/negociacao/"
driver.get(url)

status = {}
errors = {}
for hotel, cnpjs in data.items():
    for cnpj in cnpjs:
        # dirty check to see if cnpj is valid
        try:
            x = re.sub('[^0-9]','', cnpj)
            if not x or len(x) < 6:
                continue
        except Exception as e:
            continue

        if url != driver.current_url:
            driver.get(url)

        def find_elements(counter=0, max_tries=5):
            driver.get(url)
            try:
                # go to elements page
                element = driver.find_element_by_name("cpfCnpj")
                print(cnpj)
                element.send_keys(cnpj)
                send_button = driver.find_element_by_css_selector(".Button__StyledButton-sc-7ql4na-0.ebixHH.gradient-btn")
                send_button.click()
            except Exception as e:
                return find_elements(counter+1) if counter < max_tries else False
            return True


        if not find_elements():
            print(f"error on {hotel},{cnpj}")
            if hotel in errors:
                errors[hotel].append(f"{cnpj} returned None")
            else:
                errors[hotel] = [f"{cnpj} returned None"]
            continue

        # try to get data from requests
        # returns a seleniumwire requests object
        # or None
        def try_get_data(counter=0, max_tries=5):
            # remove punctuation
            cnpj_digits = re.sub('[^0-9]','', cnpj)
            for request in driver.requests:
                if cnpj_digits in request.url:
                    if request.response is not None: # check if page loaded
                        return request.response.body
            else:
                time.sleep(1) # wait a sec for requests urls
                return try_get_data(counter + 1) if counter < max_tries else None

        body = try_get_data()
        if body is None: 
            print(f"error on {hotel}")
            if hotel in errors:
                errors[hotel].append(f"{cnpj} returned None")
            else:
                errors[hotel] = [f"{cnpj} returned None"]
        
        response = gzip.decompress(body).decode("utf8")
        if not response: continue
        json_data = json.loads(response)

        try:
            deal_statuses = {debt["dealCode"]:[invoice["status"]
                    for invoice in debt["invoices"]]
                for debt in json_data["debts"]}
        except KeyError as e:
            print(f"error on {hotel}; no key error")
            if hotel in errors:
                errors[hotel].append(e)
            else:
                errors[hotel] = [e]


        if hotel in status:
            status[hotel].update(deal_statuses)
        else:
            status[hotel] = deal_statuses

# %%
with open("data.json", "w") as file:
    json.dump(status, file)

with open("errors.txt", "w") as file:
    file.write(str(errors))

# %%
pend = {f"{key}-{i}":[k,"pendente"] for key, value in status.items()
 for i, (k, v) in enumerate(value.items()) if 'pending' == v[-1]}

pd.DataFrame(pend, index=["Contrato", "Situação"]).T.to_csv("pendente.csv")
# %%
overdue = {f"{key}-{i}":[k,"atrasado"] for key, value in status.items()
 for i, (k, v) in enumerate(value.items()) if 'overdue' == v[-1]}

pd.DataFrame(overdue, index=["Contrato", "Situação"]).T.to_csv("atrasado.csv")
# %%
paid = {key:[k,"pago"] for key, value in status.items()
 for k, v in value.items() if all(['paid'==k for k in v])}

pd.DataFrame(paid, index=["Contrato", "Situação"]).T.to_csv("pagos.csv")

# %%
with open("hotel_erros.txt", "w") as f:
    for key in errors:
        f.write(key+"\n")
# %%
