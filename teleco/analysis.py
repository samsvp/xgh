#%%
import json

technologies = ["TVC", "DTH", "FTTH"]

# Get the raw data and transform it into integers
with open("teleco_full_data.json", encoding='utf-8') as f:
    data = json.load(f)

# %%
with open("municipios.txt", "w", encoding="utf-8") as f:
    for state in data:
        for county in data[state]:
            t = f"{state} - {county}:\n\tEmpresas:\n"
            tec = False
            for i in range(len(data[state][county])):
                if not tec and data[state][county][i][0] in technologies:
                    t+="\n\tTecnologias:\n"
                    tec = True
                data[state][county][i][1] = int(data[state][county][i][1].replace(".",""))
                data[state][county][i][2] = float(data[state][county][i][2].split("%")[0])/100
                t += f"\t\t{data[state][county][i][0]} : {data[state][county][i][1]}\n"
            t+="\n"
            f.write(t)

#%%
# Get data per state
tvs = {}
techs = {}
for state in data:
    tvs[state] = {}
    techs[state] = {}
    for county in data[state]:
        for i in range(len(data[state][county])):
            if data[state][county][i][0] in technologies:
                tech = data[state][county][i][0]
                techs[state][tech] = techs[state].get(tech, 0) + int(data[state][county][i][1].replace(".",""))
                continue
            tv = data[state][county][i][0]
            tvs[state][tv] = tvs[state].get(tv, 0) + int(data[state][county][i][1].replace(".",""))

# %%
# Get states with only DTH tech
raw_dth_n = {}
total_n = {}
for state in data:
    raw_dth_n[state] = 0
    total_n[state] = 0
    for county in data[state]:
        total_n[state] += 1
        techs = [d[0] for d in data[state][county] if d[0] in technologies]
        if len(techs) == 1 and techs[0] == "DTH": raw_dth_n[state] += 1



#%%
tvs_list = list(set([v for dct in tvs.values() for v in dct]))
tvs_state = {}
for tv in tvs_list:
    tvs_state[tv] = {}
    for state in tvs:
        if tv not in tvs[state]:
            tvs_state[tv][state] = 0
            continue
        tvs_state[tv][state] = tvs[state][tv] / sum(tvs[state].values()) * 100

#%%
tvs_state_filter = {tv : tvs_state[tv] for tv in tvs_state 
    if sum(tvs_state[tv].values()) > 10}
print(tvs_state_filter)

#%%
import matplotlib.pyplot as plt

for tv in tvs_state_filter:
    plt.figure(figsize=(10, 3))
    for j in range(len(tvs_state_filter[tv])):
        plt.bar(j, list(tvs_state_filter[tv].values())[j], align="center")
    plt.xticks(range(len(tvs_state_filter[tv])), tvs_state_filter[tv].keys())
    title = f"{tv}: Market Share por estado"
    name = f"imgs/{tv}_state.png"
    plt.ylabel('Porcento')
    plt.title(title)
    plt.savefig(name)
    plt.close()

#%%
#print(tvs["AC"])
_tvs = {}

for state in tvs:
    _tvs[state] = {}
    total = 0
    for tv in tvs[state]:
        _tvs[state][tv] = tvs[state][tv]
        if tv == "OI": continue
        if tvs[state][tv] < 0.2 * max(tvs[state].values()):
            total += _tvs[state].pop(tv, 0)
    if total:
        _tvs[state]["Outros"] = total 

tvs = _tvs
#%%
import matplotlib.pyplot as plt

for i in [0, 1]:
    for state in tvs:
        data = [techs, tvs][i]
        data_sorted = dict(sorted(data[state].items(), key=lambda item: item[1], reverse=True))
        for j in (range(len(data_sorted))):
            plt.bar(j, list(data_sorted.values())[j], align="center", label=list(data_sorted.keys())[j])
        plt.xticks(range(len(data_sorted)), data_sorted.keys())
        title = f"{state}: Market Share de TV por empresa de telecom" if i \
            else f'{state}: Acessos de TV por Assinatura por Tecnologia'
        name = f"imgs/{state}_tv.png" if i else f"imgs/{state}_tecnologia.png"
        plt.ylabel('Milhares')
        plt.title(title)
        plt.legend()
        plt.savefig(name)
        plt.close()
