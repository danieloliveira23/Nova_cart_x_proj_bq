import pandas as pd
import numpy as np
from datetime import date, datetime
import datetime
from juntararquivos import juntatudo

import Parametros
# Ordem de alocação dos canais
MI = 1
KA = 2
MM = 3
FQ = 4
LP = 5
WEB = 6

export = pd.DataFrame()

dfdatas = pd.DataFrame([[1, 2, 2024],[15, 2, 2024],[20, 2, 2024],[29, 2, 2024],[15, 3, 2024]],columns = ['Day', 'Month', 'Year'])
dfdatas["Date-Time"] = pd.to_datetime(dfdatas)
dfdatas["Date-Time"] = pd.to_datetime(dfdatas["Date-Time"]).dt.date

#Reads necessários
pathgeral = Parametros.cart_x_proj
conclientes = pd.read_csv(pathgeral + "Cod_clientes_novo.csv", low_memory=False)
conartigos = pd.read_csv(pathgeral + "Cod art final.csv")
conembarques = pd.read_excel(pathgeral + "De_para_periodos.xlsx")
vendalivre = pd.read_csv(pathgeral + "Venda livre.csv", low_memory=False)
vendas = pd.read_csv(pathgeral + "Leresse 3.csv")
estoques = pd.read_excel(pathgeral + "usarestoque livre + bloq.xlsx")

#Tratamentos / conversões das bases
conembarques["Embarque"] = pd.to_datetime(conembarques["Embarque"]).dt.date

vendas['Sit'] = vendas['Sit'].replace(['FIT'], 'SU')
vendas["Tamanho"] = vendas["Tamanho"].astype(str)
vendas["Tamanho"] = vendas["Tamanho"].str.lstrip('0')
vendas["Tipord"] = np.where(((vendas["Esc"]  == 77) & (vendas["Tipord"]  == "ZNOR")),"ZLOP", vendas["Tipord"])
vendas["Tipord"] = np.where(((vendas["Esc"]  == 76) & (vendas["Tipord"]  == "ZNOR")),"ZLOP", vendas["Tipord"])
vendas["Embarque"] = pd.to_datetime(vendas["Embarque"]).dt.date
vendas["Chave canal"] = vendas['Esc'].astype(str) + vendas["Can"].astype(str)
vendas["chave"] = vendas['Artigo'].astype(str) + vendas['Tamanho'].astype(str)

estoques["TAM"] = estoques["TAM"].astype(str)
estoques["TAM"] = estoques["TAM"].str.lstrip('0')
estoques["chave"] = estoques['ARTIGO'].astype(str) + estoques['TAM'].astype(str)
estoques["PRAZO"] = pd.to_datetime(estoques["PRAZO"]).dt.date

#Agrupamento base vendas para rodar numpy contra base menor 
vendas = pd.merge(vendas, conartigos, on="Artigo", how="left")
vendas = pd.merge(vendas, conembarques, on="Embarque", how="left")
dbconfig = pd.merge(vendas, conclientes, on="Ordem", how="left")

vendas["Ordem art"] = vendas["Ordem"].astype(str) + vendas["Artigo"].astype(str)
vendas = pd.merge(vendas, vendalivre, on="Ordem art", how="left")
vendas.drop("Ordem art", axis=1, inplace=True)

indcanal = [

    (vendas['Chave canal'] == '50FQ'),
    (vendas['Chave canal'] == '50VJ'),
    (vendas['Chave canal'] == '61FQ'),
    (vendas['Chave canal'] == '62FQ'),
    (vendas['Chave canal'] == '63DG'),
    (vendas['Chave canal'] == '63FQ'),
    (vendas['Chave canal'] == '64FQ'),
    (vendas['Chave canal'] == '65VJ'),
    (vendas['Chave canal'] == '66VJ'),
    (vendas['Chave canal'] == '67VJ'),
    (vendas['Chave canal'] == '68VJ'),
    (vendas['Chave canal'] == '68FQ'),
    (vendas['Chave canal'] == '69FQ'),
    (vendas['Chave canal'] == '70VJ'),
    (vendas['Chave canal'] == '70DG'),
    (vendas['Chave canal'] == '73VJ'),
    (vendas['Chave canal'] == '75VJ'),
    (vendas['Chave canal'] == '76FQ'),
    (vendas['Chave canal'] == '77FQ'),
    (vendas['Chave canal'] == '78VJ'),
    (vendas['Chave canal'] == '78FQ'),
    (vendas['Chave canal'] == '79FQ'),
    (vendas['Chave canal'] == '80VJ'),
    (vendas['Chave canal'] == '97FQ'),
    (vendas['Chave canal'] == '98FQ'),
    (vendas['Chave canal'] == '98VJ'),
    (vendas['Chave canal'] == '99VJ'),
    (vendas['Chave canal'] == '99FQ'),
    (vendas['Chave canal'] == '50MM'),
    (vendas['Chave canal'] == '65MM'),
    (vendas['Chave canal'] == '66MM'),
    (vendas['Chave canal'] == '67MM'),
    (vendas['Chave canal'] == '68MM'),
    (vendas['Chave canal'] == '70MM'),
    (vendas['Chave canal'] == '73MM'),
    (vendas['Chave canal'] == '75MM'),
    (vendas['Chave canal'] == '78MM'),
    (vendas['Chave canal'] == '80MM'),
    (vendas['Chave canal'] == '98MM'),
    (vendas['Chave canal'] == '99MM'),
    (vendas['Chave canal'] == '58VJ'),
    (vendas['Chave canal'] == '75FQ'),
    (vendas['Chave canal'] == '81PL'),
    (vendas['Chave canal'] == '99TX'),
    (vendas['Chave canal'] == '98EX'),
    (vendas['Chave canal'] == '70KA'),
    (vendas['Chave canal'] == '77LP'),
    (vendas['Chave canal'] == '58MM'),
    (vendas['Chave canal'] == '77LJ'),

]

canalfila = ['FQ', 'MM', 'FQ', 'LP', 'WEB', 'WEB', 'FQ', 'MM', 'MM', 'MM', 'MM', 'MM', 'FQ', 'KA', 'KA', 'MM', 'MM',
             'LP', 'LP', 'MM', 'MM', 'FQ', 'MM', 'MI', 'MI', 'MI', 'MM', 'FQ', 'MM', 'MM', 'MM', 'MM', 'MM', 'KA', 'MM',
             'MM', 'MM', 'MM', 'MI', 'MM', 'MM', 'MM', 'MM', 'MM', 'MI', 'KA', 'LP', 'MM', 'LP']
vendas['Canal'] = np.select(indcanal, canalfila, default=vendas['Can'])

canais = [

    (vendas['Canal'] == 'MI'),
    (vendas['Canal'] == 'KA'),
    (vendas['Canal'] == 'MM'),
    (vendas['Canal'] == 'FQ'),
    (vendas['Canal'] == 'LP'),
    (vendas['Canal'] == 'WEB'),

]
canalind = [MI, KA, MM, FQ, LP, WEB]
vendas['Indice Canal'] = np.select(canais, canalind, default=1)

conditions = [
    (vendas['Tipord'] == 'ZBME') | (vendas['Tipord'] == 'ZBRI') | (vendas['Tipord'] == 'ZBRM') | (
    vendas['Tipord'] == 'ZBTM') | (vendas['Tipord'] == 'ZCO2') | (vendas['Tipord'] == 'ZLCM') | (
    vendas['Tipord'] == 'ZLWC') | (vendas['Tipord'] == 'ZMOT') | (vendas['Tipord'] == 'ZCO1'),
    (vendas['Tipord'] == 'ZEXF'),(vendas['Tipord'] == 'ZLOP') | (vendas['Tipord'] == 'ZREP') | (vendas['Tipord'] == 'ZAPL'),
    (vendas['Tipord'] == 'ZLWE') | (vendas['Tipord'] == 'ZAPW'),(vendas['Tipord'] == 'ZMAM') | (vendas['Tipord'] == 'ZMOS') | (vendas['Tipord'] == 'ZNOR') | (
    vendas['Tipord'] == 'ZKHD') | (vendas['Tipord'] == 'ZKIL') | (vendas['Tipord'] == 'ZAFQ'),
]
choices = [1, 2, 4, 5, 3]
vendas['Indice tipord'] = np.select(conditions, choices, default=1)

vendas["Est liq"] = 0
vendas["Cart acum"] = 0
vendas["Unit"] = 0
vendas["Pçs atende"] = 0
vendas["Pçs falta"] = 0
vendas["Vlr atende"] = 0
vendas["Vlr falta"] = 0

vendas = vendas.sort_values(by=['chave','Embarque', 'Sit','Indice tipord','Indice Canal','Ordem'])
vendas.to_csv(pathgeral + "Sem agrupamento teste sort.csv", index=False)

vendas = vendas.groupby(
    ["Artigo", "Tipord", "Colecao", "NEGOCIO", "Canal", "Posição", "GRUPO", "MATERIAL", "GENERO", "Tipo material",
     "Fabricação P/T", "Origem N/I", "LINHA", "Origem final", "Bloco", "Período", "Tamanho", "Sit",
     "Embarque", "Centro", "Neg gen", "Status entrada", "NR_PEDCLI", "Cond pgto", "Indice tipord", "Indice Canal"], dropna=False)[
    ["Pecas", "Valor", "Pçs atende", "Pçs falta", "Vlr atende", "Vlr falta"]].sum().reset_index()

vendas.to_csv(pathgeral + "Teste agrupado para numpy.csv", index=False)