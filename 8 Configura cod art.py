import pandas as pd
import numpy as np


import Parametros

codart = pd.read_csv(Parametros.depara + "Cod art bq.csv", low_memory=False)

codart.rename(columns={"ARTIGO_COR": "Artigo"}, inplace=True)
codart=codart.rename(columns=lambda x: x.strip())

#final["Neg gen"] = np.where((final["Setor Atividade"] == "Hering Adulto") & (final["Gênero"] == "Feminino"), "HA Fem", final["Neg gen"])
codart["Origem final"] = ""
codart["Origem final"] = np.where((codart["ORIGEM"] == "FABRICACAO PROPRIA"), "Fábrica", "")
codart["Origem final"] = np.where((codart["ORIGEM"] == "FABRICACAO DE TERCEIROS") & (codart["ORIGEM_MERCADO"] == "ESTRANGEIRA"), "SI", codart["Origem final"])
codart["Origem final"] = np.where((codart["ORIGEM"] == "FABRICACAO DE TERCEIROS") & (codart["ORIGEM_MERCADO"] == "NACIONAL"), "SN", codart["Origem final"])

codart["Neg gen"] = ""
codart["Neg gen"] = np.where((codart["NEGOCIO"] == "HERING ADULTO") & (codart["GENERO"] == "FEMININO"), "HA Fem", codart["Neg gen"])
codart["Neg gen"] = np.where((codart["NEGOCIO"] == "HERING ADULTO") & (codart["GENERO"] != "FEMININO"), "HA Masc", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["NEGOCIO"] == "DZARM", "DZARM", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["NEGOCIO"] == "HERING INTIMA", "Hering Intima", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["NEGOCIO"] == "HERING KIDS", "Hering Kids", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["NEGOCIO"] == "HERING SPORTS", "Hering Sports", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["Neg gen"] == "", "Outros", codart["Neg gen"])
codart["Neg gen"] = np.where(codart["Neg gen"].isnull(), "Outros", codart["Neg gen"])



blocos = pd.read_excel(Parametros.depara + "Blocos.xlsx")
artigocor = pd.DataFrame(blocos)
modelo = pd.DataFrame(blocos)

combloco = pd.merge(codart, artigocor, on="Artigo", how="left")
combloco.drop("Modelo", axis=1, inplace=True)
combloco["Modelo"] = combloco['Artigo'].str[:4]

modelo = modelo[["Modelo","BLOCO PCP"]]
modelo = modelo.drop_duplicates(subset="Modelo")

final = pd.merge(combloco, modelo, on="Modelo", how="left")

final["Bloco final"] = np.where(final["BLOCO PCP_x"].isnull(), final["BLOCO PCP_y"], final["BLOCO PCP_x"])
final["Bloco final"] = np.where((final["Origem final"] == "SI") | (final["Origem final"] == "SN"), "SOURCING", final["Bloco final"])
final.drop("BLOCO PCP_x", axis=1, inplace=True)
final.drop("BLOCO PCP_y", axis=1, inplace=True)
final.drop("Modelo", axis=1, inplace=True)
final = final.rename(columns={'Bloco final': 'Bloco'})
final.drop_duplicates(subset="Artigo", inplace=True)

vendas = pd.read_csv(Parametros.cart_x_proj + "leresse 3.csv")
vendas = vendas[["Artigo"]]
vendas.drop_duplicates(subset="Artigo", inplace=True)
vendas["Filtro"] = "Manter"

final = pd.merge(final, vendas, on="Artigo", how="left")
final = final.loc[final["Filtro"] == "Manter"]
final.drop("Filtro", axis=1, inplace=True)
final.rename(columns={"INMALTEC": "Tipo material"}, inplace=True)
final.rename(columns={"ORIGEM_MERCADO": "Origem N/I"}, inplace=True)
final.rename(columns={"ORIGEM": "Fabricação P/T"}, inplace=True)

final.to_csv(Parametros.cart_x_proj + "Cod art final.csv", index=False)