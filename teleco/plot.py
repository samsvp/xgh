#%%
import matplotlib.pyplot as plt

### Receita
### https://www.teleco.com.br/rtv_receita.asp
claro_r = [9243, 8477, 7865]
sky_r = [8914, 8691, 7909]
oi_r = [881, 977, 978]

### Market share
### https://www.teleco.com.br/optva.asp
# tv por assinatura porcentagem
claro_share = [49.1, 49.5, 49.7, 49, 47.5, 47.2, 47.2, 47.1]
sky_share = [30.2, 29.9, 29.9, 30.4, 30.8, 30.7, 30.5, 30.4]
oi_share = [8.9, 9.7, 9.9, 9.9, 10.6, 11.0, 11.2, 11.4]

# Adições Líquidas de acessos das Operadoras (Milhares)
claro_liq = [-472, -834, -776]

### Tecnologia
### https://www.teleco.com.br/rtv_tec.asp
# market share
claro_mkt_tech = {
    "DTH": [16.2, 15.0, 14, 13.3, 12.1, 11.6],
    "TVC": [95.4, 96.0, 96.8, 96.0, 96.4, 96.2],
    "FTTH": [0, 0, 0, 0, 0, 0]
}

sky_mkt_tech = {
    "DTH": [55.6, 58.3,	59.2, 60.9, 61.8, 61.3],
    "TVC": [0, 0, 0, 0, 0, 0],
    "FTTH": [0, 0, 0, 0, 0, 0]
}

oi_mkt_tech = {
    "DTH": [16.7, 18.1, 18.8, 18.7, 20.2, 21.7],
    "FTTH": [2.4, 7.6, 8.3, 8.1, 7.8, 8.3]
}

# quantidade
claro_qt_tech = {
    "DTH": [1543, 1206, 1076, 1002, 910, 854],
    "TVC": [7057, 6617, 6496, 6380, 6264, 6137],
    "FTTH": [0, 0, 0, 0, 0, 0]
}

# quantidade
sky_qt_tech = {
    "DTH": [5282, 4691,	4555, 4589,	4656, 4517],
    "TVC": [0, 0, 0, 0, 0, 0],
    "FTTH": [0, 0, 0, 0, 0, 0]
}

### mkt share
op = ["2018", "2019", "1T20", "2T20", "3T20", "Out/20", "Nov/20", "Dez/20"]
plt.figure(figsize=(7, 2))
for j in range(len(op)):
    b = plt.bar(j, claro_share[j], align="center", label=op[j])
plt.xticks(range(len(op)), op)
plt.title("Claro Market Share")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0, 100)
plt.savefig("imgs/ClaroMarketShare.png")
plt.close()
#%%
plt.figure(figsize=(7, 2))
for j in range(len(op)):
    plt.bar(j, sky_share[j], align="center", label=op[j])
plt.xticks(range(len(op)), op)
plt.title("Sky Market Share")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0, 100)
plt.savefig("imgs/SkyMarketShare.png")
plt.close()

op = ["2018", "2019", "1T20", "2T20", "3T20", "Out/20", "Nov/20", "Dez/20"]
plt.figure(figsize=(7, 2))
for j in range(len(op)):
    plt.bar(j, oi_share[j], align="center", label=op[j])
plt.xticks(range(len(op)), op)
plt.title("Oi Market Share")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0, 100)
plt.savefig("imgs/OiMarketShare.png")
plt.close()

### mkt tech
plt.figure(figsize=(5, 2))
for j in range(6):
    plt.bar(j, list(claro_mkt_tech.values())[0][j], align="center", label=["2018", "2019", "1T20", "2T20", "3T20", "4T20"][j])
plt.xticks(range(6), ["2018", "2019", "1T20", "2T20", "3T20", "4T20"])
plt.title("Claro Market Share DTH")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0, 100)
plt.savefig("imgs/ClaroMarketShareDTH.png")
plt.close()

plt.figure(figsize=(5, 2))
for j in range(6):
    plt.bar(j, list(claro_mkt_tech.values())[1][j], align="center", label=["2018", "2019", "1T20", "2T20", "3T20", "4T20"][j])
plt.xticks(range(6), ["2018", "2019", "1T20", "2T20", "3T20", "4T20"])
plt.title("Claro Market Share TVC")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0,100)
plt.savefig("imgs/ClaroMarketShareTVC.png")
plt.close()

plt.figure(figsize=(5, 2))
for j in range(6):
    plt.bar(j, list(sky_mkt_tech.values())[0][j], align="center", label=["2018", "2019", "1T20", "2T20", "3T20", "4T20"][j])
plt.xticks(range(6), ["2018", "2019", "1T20", "2T20", "3T20", "4T20"])
plt.title("Sky Market Share DTH")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0,100)
plt.savefig("imgs/SkyMarketShareDTH.png")
plt.close()

plt.figure(figsize=(5, 2))
for j in range(6):
    plt.bar(j, list(oi_mkt_tech.values())[0][j], align="center", label=["2018", "2019", "1T20", "2T20", "3T20", "4T20"][j])
plt.xticks(range(6), ["2018", "2019", "1T20", "2T20", "3T20", "4T20"])
plt.title("Oi Market Share DTH")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0,100)
plt.savefig("imgs/OiMarketShareDTH.png")
plt.close()

plt.figure(figsize=(5, 2))
for j in range(6):
    plt.bar(j, list(oi_mkt_tech.values())[1][j], align="center", label=["2018", "2019", "1T20", "2T20", "3T20", "4T20"][j])
plt.xticks(range(6), ["2018", "2019", "1T20", "2T20", "3T20", "4T20"])
plt.title("Oi Market Share FTTH")
plt.ylabel("Porcento")
plt.xlabel("Ano")
plt.ylim(0,100)
plt.savefig("imgs/OiMarketShareFTTH.png")
plt.close()


### receita
plt.figure(figsize=(6, 2))
plt.plot(range(3), claro_r)
plt.xticks(range(3), ["2017", "2018", "2019"])
plt.title("Claro Receita")
plt.ylabel("R$ Milhões")
plt.ylim(7000,10000)
plt.xlabel("Ano")
plt.savefig("imgs/ClaroR.png")
plt.close()

plt.figure(figsize=(6, 2))
plt.plot(range(3), sky_r)
plt.xticks(range(3), ["2017", "2018", "2019"])
plt.title("Sky Receita")
plt.ylabel("R$ Milhões")
plt.ylim(7000,10000)
plt.xlabel("Ano")
plt.savefig("imgs/SkyR.png")
plt.close()

plt.figure(figsize=(6, 2))
plt.plot(range(3), oi_r)
plt.xticks(range(3), ["2017", "2018", "2019"])
plt.title("Oi Receita")
plt.ylabel("R$ Milhões")
plt.ylim(700,1000)
plt.xlabel("Ano")
plt.savefig("imgs/OiR.png")
plt.close()