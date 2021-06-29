# %%
import json
from collections import Counter
import matplotlib.pyplot as plt
from typing import List, Dict, Any

states_abb = {
        'Acre': 'AC', 'Alagoas': 'AL', 'Amapá': 'AP', 
        'Amazonas': 'AM', 'Bahia': 'BA', 'Ceará': 'CE', 
        'Distrito Federal': 'DF', 'Espirito Santo': 'ES', 
        'Goiás': 'GO', 'Maranhão': 'MA', 'Mato Grosso': 'MT', 
        'Mato Grosso do Sul': 'MS', 'Minas Gerais': 'MG', 
        'Pará': 'PA', 'Paraíba': 'PB', 'Paraná': 'PR', 
        'Pernambuco': 'PE', 'Piauí': 'PI', 'Roraima': 'RR', 
        'Rondônia': 'RO', 'Rio de Janeiro': 'RJ', 
        'Rio Grande do Norte': 'RN', 'Rio Grande do Sul': 'RS', 
        'Santa Catarina': 'SC', 'São Paulo': 'SP', 
        'Sergipe': 'SE', 'Tocantins': 'TO'
    }

# load data
with open("linuuptv_channel_data.json", encoding="utf8") as f:
    data = json.load(f)

# %%
# get channels in HD resolution
def get_inner_data(my_data: Dict[Any, Any], inner_data:Dict) -> Dict[Any, Any]:
    for key, value in my_data.items():
        if isinstance(value, dict):
            get_inner_data(value, inner_data)
        else:
            values = inner_data.get(key, [])
            values.append(value)
            inner_data[key] = values

# get channels by region and states
d_regions = {}
d_states = {}
for key, values in data.items():
    d_regions[key] = {}
    get_inner_data(values, d_regions[key])
    for state, state_values in values.items():
        d_states[state] = {}
        get_inner_data(state_values, d_states[state])

# %%
# count channels available in hd in each state
_hd_count = {
    state: (sum([
        any("hd" in i for i in channel_resources) 
        for _, channel_resources in state_values.items()
        ]), len(state_values))
    for state, state_values in d_states.items()
    }

channel_count = {key: value[1] for key, value in _hd_count.items()}
hd_count = {key: value[0] for key, value in _hd_count.items()}


# %%
# number of provinces without HD TV
no_hd_provinces = {
    state: (sum([sum([not any("hd" in v for key, values in tv_values.items() 
            for k, v in values.items())])
        for province, tv_values in province_values.items()]), len (province_values))
    for region, state_values in data.items() 
    for state, province_values in state_values.items()
}


# %%
# number of provinces with 3 or less HD TV channels
# wrong
three_hd_provinces = {
    state: (sum([sum(["hd" in v for key, values in tv_values.items() 
            for k, v in values.items()]) < 3
        for province, tv_values in province_values.items()]), len(province_values))
    for region, state_values in data.items() 
    for state, province_values in state_values.items()
}

# %%
# number of provinces without digital TV
no_dttv = {
    state: (sum(["TV Digital" not in tv_values.keys()
        for province, tv_values in province_values.items()]), len(province_values))
    for region, state_values in data.items() 
    for state, province_values in state_values.items()
}

# %%
def plot(data: Dict[Any, Any], title="", x_label="", y_label="", figsize=None, percentage=True):
    if figsize is not None: plt.figure(figsize=figsize)
    data_sorted = dict(sorted(data.items(), key=lambda item: item[0]))
    plt.bar(range(len(data)), [v[0]/v[1] if percentage else v[0] for v in data_sorted.values()], align="center")
    plt.xticks(range(len(data_sorted)), [states_abb[k] for k in data_sorted.keys()])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

plot(no_hd_provinces, "Porcentagem de cidades sem canais HD por estado", 
        "Estados", "Cidades sem HD(%)", (10.5, 4))

plot(three_hd_provinces, "Porcentagem de cidades com menos de 3 canais em HD por estado", 
        "Estados", "Cidades com menos de 3 canais em HD(%)", (10.5, 4))

plot(no_dttv, "Porcentagem de cidades sem TV digital", 
        "Estados", "Cidades sem TV digital(%)", (10.5, 4))
# %%
def stacked_plot(data1: Dict[Any, Any], data2: Dict[Any, Any], title="", x_label="", y_label="", figsize=None):
    if figsize is not None: plt.figure(figsize=figsize)
    data1_sorted = dict(sorted(data1.items(), key=lambda item: item[0]))
    data2_sorted = dict(sorted(data2.items(), key=lambda item: item[0]))
    plt.bar(range(len(data1)), [v for v in data2_sorted.values()], align="center", color="C1")
    plt.bar(range(len(data1)), [v for v in data1_sorted.values()], align="center", color="C0")
    plt.xticks(range(len(data1_sorted)), [states_abb[k] for k in data1_sorted.keys()])
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

stacked_plot(hd_count, channel_count, "Número de canais com HD por estado", 
        "Estados", "Azul - Canais com HD\nLaranja - total de canais", (10.5, 4))
# %%
