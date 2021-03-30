# %%
import json
from collections import Counter
from typing import List, Dict, Any

# load data
with open("linuuptv_channel_data.json", encoding="utf8") as f:
    data = json.load(f)

# %%
# get channels in HD resolution
def get_inner_data(my_data: Dict[Any, Any], inner_data:Dict):
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
hd_count = {
    state: (sum([
        any("hd" in i for i in channel_resources) 
        for _, channel_resources in state_values.items()
        ]), len(state_values))
    for state, state_values in d_states.items()
    }

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
