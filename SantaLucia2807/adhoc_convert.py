# %%
import pandas as pd

df_og = pd.read_excel("ADHOC_RJ_RIO_BONITO_202107.xlsx",sheet_name='Venda')

# %%
df = df_og.copy()
df.columns = df.iloc[0]
df = df.iloc[1:]
# %%
df1 = df.melt(id_vars=[c for c in df.columns if "unidade" not in c.lower()], 
        var_name="MES", 
        value_name="Unidade")

df2 = df.melt(id_vars=[c for c in df.columns if "cpp" not in c.lower()], 
        var_name="MES", 
        value_name="CPP")
# %%
df1 = df1.drop(columns=[c for c in df1.columns if "cpp" in c.lower()])
df2 = df2.drop(columns=[c for c in df2.columns if "unidade" in c.lower()])
# %%
df1["CPP"] = df2["CPP"]
df1['MES'] = df1['MES'].apply(lambda x: x.split("_")[0])
df1.to_csv("adhoc.csv")
# %%
