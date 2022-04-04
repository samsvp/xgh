#%%
from web_tracker import WebTracker


def main():
    file_cam = "camera.txt"
    url_cam = "https://www.camara.leg.br/busca-portal?contextoBusca=BuscaNoticias&pagina=1&order=relevancia&abaEspecifica=true&filtros=%5B%7B%22temaPortal%22%3A%22Ci%C3%AAncia,%20Tecnologia%20e%20Comunica%C3%A7%C3%B5es%22%7D%5D"

    web_tracker_cam = WebTracker(file_cam, url_cam)
    web_tracker_cam("div", "lista-resultados", None, 
        "Update camera", "Update no site www.camara.leg.br")


main()
# %%
