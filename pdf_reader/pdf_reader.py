# %%
import re
import pdf2image
import pytesseract


from typing import *

_BLINCAST_CNPJ = "31.952.078/0001-30"


def read_pdf(path: str) -> Tuple[str, str, str, str]:
    doc = pdf2image.convert_from_path(path)

    for page in doc:
        text = pytesseract.image_to_string(page)

    lines = [t for t in text.lower().split("\n") 
            if t and not t.isspace()]

    cnpj = get_cpjs(text)
    number = get_nfe_number(text)
    name = get_name(lines)
    value = get_value(lines)
    return (cnpj, number, name, value)
    # print(f"CNPJ: {cnpjs}", f"Número NFe {number}", 
    #     f"Nome: {name}", f"Valor {value}", sep="\n")


def get_cpjs(text: str) -> str:
    regex = r'\d{2}.\d{3}.\d{3}/\d{4}-\d{2}'
    cnpjs = re.findall(regex, text)
    for cnpj in cnpjs:
        if cnpj != _BLINCAST_CNPJ: return cnpj

def get_nfe_number(text: str) -> str:
    regex = r'\d{8}'
    return re.search(regex, text).group()


def get_name(lines: List[str]) -> str:
    if "santo andre" in lines[0]:
        target = "razao social/nome"
        offset = len(target) + 1
    else:
        target = "nome/razao social"
        offset = len(target) + 2
    
    name = next(
        (t[offset:] for t in lines
            if t.startswith(target) and 
            "blincast" not in t), 
        "")
    return name.upper()


def get_value(lines: List[str]) -> str:
    if "rio de janeiro" in lines[0]:
        target = "valor da nota"
    elif "sao paulo" in lines[0]:
        target = "valor total do servico"
    elif "santo andre" in lines[0]:
        target = "valor do servigo"
    else: return -1
        
    offset = len(target) + 3
    value = next(
        (t[offset:].split(" ")[1] for t in lines
            if t.startswith(target)), "")
    return value.upper()
    

# %%
