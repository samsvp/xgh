# %%
import os
import re
import PyPDF2

def get_value(text: str) -> str:
    index = text.find("Valor total da conta:")
    text = text[index:index+100] # value will always come after this
    regex = r"\d*[\,]{1}\d{1,2}"
    return re.search(regex, text).group().replace(",",".")


def get_contract_number(text: str) -> str:
    regex = r"\d\d\d\d\d\d\d\d\w\w\w"
    for match in re.finditer(regex, text):
        num = match.group()
        if num.endswith("Mês"):
            return num[:-3]


def get_bar_code(text: str) -> str:
    # regex string to find bar code
    re_bar = r"\d\d\d\d\d\d\d\d\d\d\d\s\d\s\d\d\d\d\d\d\d\d\d\d\d\s\d\s\d\d\d\d\d\d\d\d\d\d\d\s\d\s\d\d\d\d\d\d\d\d\d\d\d\s\d"
    return re.search(re_bar, text).group()
    

# %%
pdfs_path = [f"pdfs/{pdf}" for pdf in os.listdir("pdfs")]

pdfs_text = {}

for pdf_path in pdfs_path:
    with open(pdf_path, "rb") as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        page = read_pdf.getPage(0)
        pdfs_text[pdf_path] = page.extractText()


query = "Conta em Débito Automático, favor não receber"
dont_pay_pdfs = {pdf_name: pdf_text 
    for pdf_name, pdf_text in pdfs_text.items() 
    if query in pdf_text
}


# %%
text_file = ""
for _, text in dont_pay_pdfs.items():
    contract_number = get_contract_number(text)
    value = get_value(text)
    bar_code = get_bar_code(text)
    text_file += f"{contract_number},{value},{bar_code}\n"

with open("contratos.csv", "w") as f:
    f.write(text_file)

# %%
