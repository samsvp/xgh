import ast

from tkinter import *
from tkinter import ttk
from tkinter import filedialog

from pdf_reader import read_pdf


FILETYPES = (
    ("PDF", "*.pdf"),
    ("All files", "*")
)


gui = Tk()
gui.geometry("800x400")
gui.title("FC")


def get_file_path():
    file_selected = filedialog.askopenfilename(
        title="Select a File", filetypes=FILETYPES)
    file_path.set(file_selected)
    folder_path.set(file_selected)
    

def get_paths():
    files_selected = filedialog.askopenfilenames(
        title="Select a File", filetypes=FILETYPES)
    
    file_path.set(files_selected)
    folder_path.set(files_selected)


def doStuff():
    try:
        file = ast.literal_eval(file_path.get())
    except Exception:
        file = file_path.get()
    print("Doing stuff with folder", file)
    cnpj, nfe, name, value = read_pdf(file)
    cnpj_value.set(cnpj)
    nfe_value.set(nfe)
    name_value.set(name)
    value_value.set(value) 
    print(f"CNPJ: {cnpj}", f"Número NFe {nfe}", 
        f"Nome: {name}", f"Valor {value}", sep="\n")


### variables
file_path = StringVar()
folder_path = StringVar()

cnpj_value = StringVar()
nfe_value = StringVar()
name_value = StringVar()
value_value = StringVar()


### Folder name
a = Label(gui ,text="Enter name")
a.grid(row=0,column = 0)

E = Entry(gui,textvariable=folder_path)
E.grid(row=0,column=1)


### Buttons
btn_find_file = ttk.Button(gui, 
        text="Selecionar Arquivo",command=get_file_path)
btn_find_file.grid(row=0,column=2)


btn_find_folder = ttk.Button(gui, 
        text="Selecionar Pasta",command=get_paths)
btn_find_folder.grid(row=0,column=3)

c = ttk.Button(gui ,text="Processar", command=doStuff)
c.grid(row=4,column=0)


#### Data
cnpj = ttk.Label(gui, text="CNPJ")
cnpj.grid(row=5, column=0)
e_cnpj = Entry(gui,textvariable=cnpj_value)
e_cnpj.grid(row=5,column=1)

nfe = ttk.Label(gui, text="NFe")
nfe.grid(row=5, column=2)
e_nfe = Entry(gui,textvariable=nfe_value)
e_nfe.grid(row=5,column=3)

name = ttk.Label(gui, text="Nome/Razão Social")
name.grid(row=6, column=0)
e_value = Entry(gui,textvariable=name_value)
e_value.grid(row=6,column=1)

value = ttk.Label(gui, text="Valor")
value.grid(row=6, column=2)
e_value = Entry(gui,textvariable=value_value)
e_value.grid(row=6,column=3)


### mainloop
gui.mainloop()