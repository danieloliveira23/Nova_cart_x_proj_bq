import pandas as pd
import numpy as np
import datetime

import Parametros

df = pd.read_csv(Parametros.cart_x_proj + "Leresse original bq.csv", low_memory=False)
mesatual = Parametros.mesatual
desc_mes_atual = Parametros.desc_mes_atual

ordensmi = pd.DataFrame(df)
ordensmi = ordensmi[["Documento_Tipo_Codigo", "Ordem", "Valor"]]
ordensmi = ordensmi.loc[ordensmi["Documento_Tipo_Codigo"] =="ZEXF"]

ordensmi.drop_duplicates(subset="Ordem",inplace=True)
ordensmi = ordensmi[["Ordem"]]
ordensmi.to_csv(Parametros.depara + "Pedidos ZEXF.csv", index=False)


df = df.loc[df["Deposito"] != 605]
df = df.loc[df["Deposito"] != 606]

df.drop("Deposito", axis=1, inplace=True)
tabeladatas = pd.DataFrame({'num_mes': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                'desc_mes': ['Jan', 'Fev', 'Mar', 'Abr','Mai','Jun','Jul','Ago','Set','Out','Nov','Dez']})

df["Data_Embarque"] = pd.to_datetime(df["Data_Embarque"]).dt.date
df["num_mes"] = pd.to_datetime(df["Data_Embarque"]).dt.month
df = pd.merge(df, tabeladatas, on="num_mes", how="left")
df["Mês"] = np.where(df["Data_Embarque"] <= mesatual, desc_mes_atual, df["desc_mes"])


df.drop("num_mes", axis=1, inplace=True)
df.drop("desc_mes", axis=1, inplace=True)

df.rename(columns={"Canal_Cod": "Can"}, inplace=True)
df.rename(columns={"Artigo": "Artigo"}, inplace=True)
df.rename(columns={"Tamanho": "Tamanho"}, inplace=True)
df.rename(columns={"Ordem": "Ordem"}, inplace=True)
df.rename(columns={"Documento_Tipo_Codigo": "Tipord"}, inplace=True)
df.rename(columns={"Escritorio_Cod": "Esc"}, inplace=True)
df.rename(columns={"Status_Resumo": "Sit"}, inplace=True)
df.rename(columns={"Data_Embarque": "Embarque"}, inplace=True)
df.rename(columns={"Estacao": "Colecao"}, inplace=True)
df.rename(columns={"Setor_Atividade": "Neg"}, inplace=True)
df.rename(columns={"Mês": "Mês"}, inplace=True)
df.rename(columns={"Pecas": "Pecas"}, inplace=True)
df.rename(columns={"Valor": "Valor"}, inplace=True)

df = df.loc[df["Tipord"] != "ZEXF"]
df = df.loc[:, ["Can","Artigo","Tamanho","Ordem","Tipord","Esc","Sit","Mês","Embarque","Colecao","Neg","Pecas","Valor"]]
df['Sit'] = df['Sit'].replace(['Cliente Fictício'], 'Suspenso Comercial')
df.to_csv(Parametros.cart_x_proj+"Leresse 1.csv", index=False)
