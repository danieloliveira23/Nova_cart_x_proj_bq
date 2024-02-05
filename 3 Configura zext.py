import pandas as pd
import numpy as np
import datetime

import Parametros

mesatual = Parametros.mesatual
desc_mes_atual = Parametros.desc_mes_atual

tabeladatas = pd.DataFrame({'num_mes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'desc_mes': ['Jan', 'Fev', 'Mar', 'Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']})

basezext = pd.read_excel(Parametros.saplimpar + "ZEXT para configurar.xlsx", skiprows=6)
basezext=basezext.rename(columns=lambda x: x.strip())
basezext = basezext[["CDst","Material","VMz","Doc.venda","TpDV","EscrV","DtDesjRem.","Est","Rc","Qtd.ordem","qt_faturado","Valor"]]
basezext.dropna(
    axis=0,
    how='any',
    subset=["Doc.venda"],
    inplace=True
)

basezext = basezext.loc[basezext["CDst"] != "CDst"]
#basezext["Qtd.ordem"] = basezext["Qtd.ordem"].astype(int)
basezext["Pecas"] = basezext["Qtd.ordem"] - basezext["qt_faturado"]
basezext = basezext.loc[basezext["Pecas"] > 0 ]

basezext.drop("Qtd.ordem", axis=1, inplace=True)
basezext.drop("qt_faturado", axis=1, inplace=True)
basezext = basezext.loc[basezext["Rc"].isnull()]
basezext['TpDV'] = basezext['TpDV'].str.replace('ZEXT', 'ZEXF')
basezext["DtDesjRem."] = basezext["DtDesjRem."].str.replace('.','/')
basezext.drop("Rc", axis=1, inplace=True)
basezext["Sit"] = "Pendente"


precos = pd.DataFrame(basezext)
precos = precos[["Material", "Pecas", "Valor"]]
precos["Valor total"] = precos["Pecas"] * precos["Valor"]
precos = precos.groupby(["Material"], dropna=False)[["Pecas", "Valor total"]].sum().reset_index()
#geral = geral.groupby(["Artigo", "Tipord", "Colecao", "Neg", "Canal", "Posição", "Grupo", "LINX Tipo", "Gênero", "Tipo Material","Produção (P/T)", "Origem (N/I)", "Linha", "Origem", "Bloco", "Período", "Status final","Tamanho","Sit","Embarque","Centro Cód","NR_PEDCLI","Neg gen","Cond pgto","Status entrada"], dropna=False)["Pecas", "Valor", "Pçs atende", "Pçs falta", "Vlr atende", "Vlr falta"].sum().reset_index()
precos["Unitário"] = precos["Valor total"] / precos["Pecas"]
precos = precos[["Material", "Unitário"]]
precos.rename(columns={"Material" : "Artigo"}, inplace=True)
precos.drop_duplicates(subset="Artigo", inplace=True)

cod_art = pd.read_csv(Parametros.depara + "Cod art bq.csv", low_memory=False)
cod_art = cod_art[["ARTIGO_COR","NEGOCIO"]]
cod_art.drop_duplicates(subset="ARTIGO_COR", inplace=True)
cod_art.rename(columns={"ARTIGO_COR" : "Artigo"}, inplace=True)

basezext.rename(columns={"Material" : "Artigo"}, inplace=True)
basezext = pd.merge(basezext, precos, on="Artigo", how="left")
basezext = pd.merge(basezext, cod_art, on="Artigo", how="left")

basezext["Valor"] = basezext["Unitário"] * basezext["Pecas"]
basezext.drop("Unitário", axis=1, inplace=True)

basecotas = pd.read_excel(Parametros.depara + "Cotas.xlsx", usecols=["Est","Coleção"])
basezext = pd.merge(basezext, basecotas, on="Est", how="left")
basezext.drop("Est", axis=1, inplace=True)
basezext.rename(columns={"DtDesjRem.": "Embarque"}, inplace=True)
basezext.to_excel("Teste nome colunas.xlsx", index=False)
basezext["num_mes"] = pd.to_datetime(basezext["Embarque"], dayfirst=True).dt.month
basezext = pd.merge(basezext, tabeladatas, on="num_mes", how="left")

basezext["Embarque"] = pd.to_datetime(basezext["Embarque"], dayfirst=True).dt.date
basezext["Mês"] = np.where(basezext["Embarque"] <= mesatual, desc_mes_atual, basezext["desc_mes"])
#basezext.drop("Check data", axis=1, inplace=True)
basezext.drop("num_mes", axis=1, inplace=True)
basezext.drop("desc_mes", axis=1, inplace=True)

basezext.rename(columns={"CDst": "Can"}, inplace=True)
basezext.rename(columns={"VMz": "Tamanho"}, inplace=True)
basezext.rename(columns={"Doc.venda": "Ordem"}, inplace=True)
basezext.rename(columns={"TpDV": "Tipord"}, inplace=True)
basezext.rename(columns={"EscrV": "Esc"}, inplace=True)
basezext.rename(columns={"NEGOCIO": "Neg"}, inplace=True)
basezext.rename(columns={"Coleção": "Colecao"}, inplace=True)


basezext = basezext.loc[:, ["Can","Artigo","Tamanho","Ordem","Tipord","Esc","Sit","Mês","Embarque","Colecao","Neg","Pecas","Valor"]]


basezext.to_excel(Parametros.depara + "ZEXT para subir leresse.xlsx", index=False)