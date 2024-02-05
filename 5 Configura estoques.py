import pandas as pd
import numpy as np
import datetime


import Parametros
dataestoque = datetime.date.today() - datetime.timedelta(days=1)

estoques = pd.read_csv(Parametros.saplimpar + "Estoque bq.csv", low_memory=False, usecols=["Qt_total","CDARTIGO", "CDTAMANH", "CDTIPCAL"])

estoques["CDTAMANH"] = estoques["CDTAMANH"].str.lstrip("0")
total = pd.DataFrame(estoques)
bloqueado = pd.DataFrame(estoques)

total = total.loc[estoques["CDTIPCAL"] == 1]
bloqueado = bloqueado.loc[bloqueado["CDTIPCAL"] == 55]

total["Chave"] = total["CDARTIGO"].astype(str) + total["CDTAMANH"].astype(str)
bloqueado["Chave"] = bloqueado["CDARTIGO"].astype(str) + bloqueado["CDTAMANH"].astype(str)

total = total.groupby(["Chave","CDARTIGO","CDTAMANH"], dropna=False)["Qt_total"].sum().reset_index()
bloqueado = bloqueado.groupby(["Chave","CDARTIGO","CDTAMANH"], dropna=False)["Qt_total"].sum().reset_index()

final = pd.merge(total, bloqueado, on="Chave", how="left")
final["Qt_total_y"] = final["Qt_total_y"].fillna(0)
final["Qt livre"] = final["Qt_total_x"] - final["Qt_total_y"]
final.rename(columns={"Qt_total_x":"Qt total"}, inplace=True)
final.rename(columns={"Qt_total_y":"Qt bloq"}, inplace=True)
final.drop("CDARTIGO_y", axis=1, inplace=True)
final.drop("CDTAMANH_y", axis=1, inplace=True)
final.drop("Chave",axis=1, inplace=True)
final.rename(columns={"CDARTIGO_x":"Artigo"}, inplace=True)
final.rename(columns={"CDTAMANH_x":"Tamanho"}, inplace=True)
final = final.loc[final["Qt total"] > 0]
final = final.loc[:, ["Artigo","Tamanho","Qt livre","Qt bloq","Qt total"]]
final["Tamanho"] = final["Tamanho"].astype(str)

estoque603 = pd.read_excel(Parametros.saplimpar + "Estoque 603.xlsx", skiprows=4)
estoque603=estoque603.rename(columns=lambda x: x.strip())
estoque603 = estoque603[["Material","VMz","Utiliz.livre PC","Bloqueado PC"]]

estoque603.dropna(
    axis=0,
    how='any',
    subset=["Material"],
    inplace=True
)
estoque603 = estoque603.loc[estoque603["Material"] != "Material"]
estoque603 = estoque603.rename(columns={"Utiliz.livre PC": "Qt livre"})
estoque603 = estoque603.rename(columns={"Bloqueado PC":"Qt bloq"})
estoque603["QTD"] = estoque603["Qt livre"] + estoque603["Qt bloq"]

estoque603["Origem"] = estoque603['Material'].str[-2:]
estoque603 = estoque603.loc[(estoque603["Origem"] == "SI") | (estoque603["Origem"] == "SN")]
estoque603 = estoque603.loc[:, ["Material","VMz","Qt livre","Qt bloq","QTD","Origem"]]
estoque603.drop("Origem", axis=1, inplace=True)

#########################################################################################################

estoqueemtransito = pd.read_excel(Parametros.saplimpar + "Estoque em transito.xlsx", skiprows=3)
estoqueemtransito=estoqueemtransito.rename(columns=lambda x: x.strip())
estoqueemtransito = estoqueemtransito[["Material","VMz","Qtd.NT"]]

estoqueemtransito.dropna(
    axis=0,
    how='any',
    subset=["Material"],
    inplace=True
)
estoqueemtransito = estoqueemtransito.loc[estoqueemtransito["Material"] != "Material"]

estoqueemtransito =estoqueemtransito.rename(columns={"Qtd.NT": "Qt bloq"})
estoqueemtransito["Qt livre"] = 0
estoqueemtransito["QTD"] = estoqueemtransito["Qt livre"] + estoqueemtransito["Qt bloq"]
estoqueemtransito = estoqueemtransito.loc[:, ["Material","VMz","Qt livre","Qt bloq","QTD"]]
compiladoestoque = pd.concat([estoque603,estoqueemtransito])

compiladoestoque.rename(columns={"Material": "Artigo"}, inplace=True)
compiladoestoque.rename(columns={"VMz": "Tamanho"}, inplace=True)
compiladoestoque.rename(columns={"QTD": "Qt total"}, inplace=True)
compiladoestoque = compiladoestoque.loc[compiladoestoque["Qt total"] > 0]
compiladoestoque["Tamanho"] = compiladoestoque["Tamanho"].astype(str)


estoqueunificado = pd.concat([final, compiladoestoque])
estoqueunificado["Data corte"] = dataestoque

livre = pd.DataFrame(estoqueunificado)
bloq = pd.DataFrame(estoqueunificado)
livre = livre[["Artigo","Tamanho","Qt livre","Data corte"]]
bloq = bloq[["Artigo","Tamanho","Qt total","Data corte"]]

livre.columns = ["ARTIGO","TAM","QTD","PRAZO"]
bloq.columns = ["ARTIGO","TAM","QTD","PRAZO"]

livre.to_excel(Parametros.cart_x_proj + "usarestoque livre.xlsx", index=False)
bloq.to_excel(Parametros.cart_x_proj + "usarestoque livre + bloq.xlsx", index=False)


#estoqueunificado.to_csv(gravar + "Estoque fisico.csv", index=False)

#compiladoestoque.to_excel(gravar + "Estoque transito + 603.xlsx", index=False)
