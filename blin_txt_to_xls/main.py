#%%
import os
import re
import pandas as pd
from colorama import Fore
from datetime import datetime


log_content = ""
log_filename = "output.log"
files = [f for f in os.listdir(".") if f.endswith(".CT")]
if len(files) == 0:
    print("Nenhum arquivo encontrado")
    exit(0)


for file in files:
    with open(file, encoding="latin-1") as f:
        # ignore the first and last lines as well as empty lines
        lines = [line for line in f.readlines()[1:-1] if line.split()] 

    # data should a number of lines which is a multiple of 3
    if len(lines) % 3 != 0:
        warning_msg = "WARNING: Número de linhas não é múltiplo de 3\n"
        warning_msg += "Verifique se o arquivo está correto\n"
        log_content += warning_msg
        print(Fore.YELLOW + warning_msg)

    # parse file
    # one excel row will use three lines of the file
    # we need to get the date, debit and credit number, value and history
    data = []
    date_format = "%Y%m%d"
    i = 0
    while i < len(lines):
        # get date
        date_str = lines[i].split()[0][5:-1]
        # try to convert date to the desired format
        try:
            date_str = datetime.strptime(date_str, "%Y%m%d").strftime("%d/%m/%Y")
        # something went wrong on this line, issue a warning and ignore it
        except ValueError as e:
            print(e)
            error_msg = f"ERROR (linha {i}): Linha mal formatada Seguindo para próxima linha\n"
            error_msg += f"(linha {i}): valor de data inválido: valor = {date_str}\n"
            log_content += error_msg
            print(Fore.RED + error_msg)

            i += 1
            continue

        # get debit and credit number as well as values
        debit_number = lines[i+1].split()[1]
        credit_number = lines[i+2].split()[1]

        # check if values are right
        value_debit = lines[i+1].split()[-1]
        value_credit = lines[i+2].split()[-1]
        # issue a warning if values are not the same
        if value_credit != value_debit:
            warning_msg = f"WARNING (linha {i}): Valores de crédito e débito não são iguais\n"
            warning_msg += "Será utilizado o valor de crédito\n"
            log_content += warning_msg
            print(Fore.YELLOW + warning_msg)
        
        # get the name
        # split on more than one whitespaca
        name = re.split(r'\s{2,}', lines[i+2])[-2]

        # append data and convert types
        try:
            d = {
                "Data": date_str, "conta debito": int(debit_number),
                "conta credito": int(credit_number), "valor": float(value_credit),
                "cod historico padrao": "", "historico": name
            }
        except ValueError as e:
            print(e)
            error_msg = f"ERRO (linha {i}): Dados não foram convertidos de forma correta\n"
            error_msg += "Valor será ignorado\n"
            log_content += error_msg
            print(Fore.RED + error_msg)

            i += 1
            continue

        data.append(d)

        i += 3

    # finally, save excel
    file_name = "".join(file.split(".")[:-1])
    pd.DataFrame(data).to_excel(f"{file_name}.xlsx")

    # save log as well
    with open(log_filename, "w") as f:
        f.writelines(log_content)
    # %%
