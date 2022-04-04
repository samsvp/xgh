#%%
from web_tracker import WebTracker


def main():
    file_sen = "senado.txt"
    url_sen = "https://www6g.senado.leg.br/busca/?portal=Atividade+Legislativa&q=ci%C3%AAncia+tecnologia+e+informa%C3%A7%C3%A3o"

    web_tracker_sen = WebTracker(file_sen, url_sen)
    web_tracker_sen("div", None, 
        "col-xs-12 col-md-12 sf-busca-resultados", 
        "Update senado", "Update no site www.senado.leg.br")


main()
# %%