import pandas as pd
import numpy as np
import datetime

import Parametros

mesatual = Parametros.mesatual
desc_mes_atual = Parametros.desc_mes_atual

tabeladatas = pd.DataFrame({'num_mes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'desc_mes': ['Jan', 'Fev', 'Mar', 'Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']})

saldocontrato = pd.read_excel(Parametros.saplimpar + "Saldo contrato para configurar.xlsx",skiprows=6)
saldocontrato = saldocontrato.rename(columns=lambda  x: x.strip())
saldocontrato = saldocontrato.loc[saldocontrato["Doc.venda"] != "Doc.venda"]

saldocontrato.dropna(
    axis=0,
    how='any',
    subset=["Doc.venda"],
    inplace=True
)

saldocontrato = saldocontrato[["Doc.venda","Material","VMz","TpDV","DtDesjRem.","QTD_PENDENTE"]]
saldocontrato.columns = ["Ordem","Artigo","Tamanho","Tipord","Embarque","Pecas"]
saldocontrato["Embarque"].str.replace('.','/')
saldocontrato["Embarque"] = pd.to_datetime(saldocontrato["Embarque"], dayfirst=True).dt.date
saldocontrato["Sit"] = "Contrato"
saldocontrato["num_mes"] = pd.to_datetime(saldocontrato["Embarque"]).dt.month

finalcommes = pd.merge(saldocontrato, tabeladatas, on="num_mes", how="left")
finalcommes["Mês"] = np.where(finalcommes["Embarque"] <= mesatual, desc_mes_atual, finalcommes["desc_mes"])
finalcommes.drop("num_mes", axis=1, inplace=True)
finalcommes.drop("desc_mes", axis=1, inplace=True)
finalcommes = finalcommes.loc[finalcommes["Pecas"] > 0]

cod_ordens = pd.read_csv(Parametros.depara + "Contratos.csv")
precos = pd.DataFrame(cod_ordens)
cota = pd.DataFrame(cod_ordens)
cod_ordens = cod_ordens.rename(columns=lambda x: x.strip())
cod_ordens = cod_ordens[["Ordem","Canal_Cod","Escritorio_Cod"]]
cod_ordens = cod_ordens.drop_duplicates(subset="Ordem")
#cod_ordens.to_excel(gravar + "Base chave.xlsx", index=False)

juncao = pd.merge(finalcommes, cod_ordens, on="Ordem", how="left")


cod_art = pd.read_csv(Parametros.depara + "Cod art bq.csv", low_memory=False)
cod_art = cod_art[["ARTIGO_COR","NEGOCIO"]]
cod_art.drop_duplicates(subset="ARTIGO_COR", inplace=True)
cod_art.rename(columns={"ARTIGO_COR" : "Artigo"}, inplace=True)
juncaoartigos = pd.merge(juncao, cod_art, on="Artigo", how="left")

precos  = precos.rename(columns=lambda x: x.strip())
precos = precos[["Artigo", "Ordem_Valor","Ordem_Pcs"]]
precos = precos.groupby(["Artigo"], dropna=False)[["Ordem_Valor", "Ordem_Pcs"]].sum().reset_index()
precos["Unitário"] = precos["Ordem_Valor"] / precos["Ordem_Pcs"]


comprecos = pd.merge(juncaoartigos, precos, on="Artigo", how="left")
comprecos["Valor"] = comprecos["Unitário"] * comprecos["Pecas"]
comprecos.drop("Ordem_Valor", axis=1, inplace=True)
comprecos.drop("Ordem_Pcs", axis=1, inplace=True)
comprecos.drop("Unitário", axis=1, inplace=True)

cota = cota.rename(columns=lambda x: x.strip())
cota = cota[["Ordem","Artigo","Estacao"]]
cota["Ordem"] = cota["Ordem"].astype(str)
cota['Ordem'] = cota['Ordem'].str.split('.').str[0]
cota["Ordem art"] = cota["Ordem"].astype(str) + cota["Artigo"].astype(str)
cota = cota.drop_duplicates(subset="Ordem art")
cota = cota[["Ordem art","Estacao"]]
#cota.to_excel("teste agrupamento colecao.xlsx", index=False)

comprecos["Ordem"] = comprecos["Ordem"].astype(str)
comprecos['Ordem'] = comprecos['Ordem'].str.split('.').str[0]
comprecos["Ordem art"] = comprecos["Ordem"].astype(str) + comprecos["Artigo"].astype(str)

finalcomprecos = pd.merge(comprecos, cota, on="Ordem art", how="left")
finalcomprecos.drop("Ordem art", axis=1, inplace=True)
finalcomprecos.to_csv(Parametros.cart_x_proj + "teste.csv", index=False)
finalcomprecos.rename(columns={"Canal_Cod": "Canal Cód"}, inplace=True)
finalcomprecos.rename(columns={"Escritorio_Cod": "Escritório Cód"}, inplace=True)
finalcomprecos.rename(columns={"Estacao": "Estação"}, inplace=True)
finalcomprecos.rename(columns={"NEGOCIO": "Setor Atividade"}, inplace=True)

finalcomprecos = finalcomprecos.loc[:, ["Canal Cód","Artigo","Tamanho","Ordem","Tipord","Escritório Cód","Sit","Mês","Embarque","Estação","Setor Atividade","Pecas","Valor"]]
finalcomprecos.columns = ["Can","Artigo","Tamanho","Ordem","Tipord","Esc","Sit","Mês","Embarque","Colecao","Neg","Pecas","Valor"]
finalcomprecos.to_excel(Parametros.depara + "teste contratos.xlsx", index=False)

