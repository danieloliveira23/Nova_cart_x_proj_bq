import pandas as pd
import numpy as np
from datetime import date, datetime
import datetime
from juntararquivos import juntatudo
#from Juntar_base_geral import junta_base_geral

import Parametros

dfdatas = pd.DataFrame([[1, 2, 2024],[15, 2, 2024],[20, 2, 2024],[29, 2, 2024],[15, 3, 2024]], columns=['Day', 'Month', 'Year'])
dfdatas["Date-Time"] = pd.to_datetime(dfdatas)
dfdatas["Date-Time"] = pd.to_datetime(dfdatas["Date-Time"]).dt.date

primeirocorte = datetime.date(2023, 11, 30)
segundocorte = datetime.date(2023, 12, 31)
terceirocorte = datetime.date(2024, 1, 31)

conclientes = pd.read_csv(Parametros.cart_x_proj + "Cod_clientes_novo.csv")
conartigos = pd.read_csv(Parametros.cart_x_proj + "Cod art final.csv")
conembarques = pd.read_excel(Parametros.cart_x_proj + "De_para_periodos.xlsx")
vendalivre = pd.read_csv(Parametros.cart_x_proj + "Venda livre.csv", low_memory=False)
conembarques["Embarque"] = pd.to_datetime(conembarques["Embarque"]).dt.date

# Ordem de alocação dos canais
MI = 1
KA = 2
MM = 3
FQ = 4
LP = 5
WEB = 6

df = pd.read_csv(Parametros.cart_x_proj + "Leresse 3.csv")

agrupado = pd.DataFrame(df)
agrupado['Sit'] = agrupado['Sit'].replace(['FIT'], 'SU')
agrupado["Tamanho"] = agrupado["Tamanho"].astype(str)
agrupado["Tamanho"] = agrupado["Tamanho"].str.lstrip('0')
agrupado["Tipord"] = np.where(((agrupado["Esc"] == 77) & (agrupado["Tipord"] == "ZNOR")), "ZLOP", agrupado["Tipord"])
agrupado["Tipord"] = np.where(((agrupado["Esc"] == 76) & (agrupado["Tipord"] == "ZNOR")), "ZLOP", agrupado["Tipord"])
agrupado["Embarque"] = pd.to_datetime(agrupado["Embarque"]).dt.date

for i in range(len(dfdatas)):
    print(dfdatas.loc[i, "Date-Time"])

    final = pd.DataFrame(agrupado)
    final["chave"] = final['Artigo'].astype(str) + final['Tamanho'].astype(str)
    final["Chave canal"] = final['Esc'].astype(str) + final["Can"].astype(str)

    final["Est liq"] = 0
    final["Cart acum"] = 0
    final["Unit"] = 0
    final["Pçs atende"] = 0
    final["Pçs falta"] = 0
    final["Vlr atende"] = 0
    final["Vlr falta"] = 0

    dfest = pd.read_excel(Parametros.cart_x_proj + "usarestoque livre + bloq.xlsx")
    dfestoque = pd.DataFrame(dfest)
    dfestoque["TAM"] = dfestoque["TAM"].astype(str)
    dfestoque["TAM"] = dfestoque["TAM"].str.lstrip('0')
    dfestoque["chave"] = dfestoque['ARTIGO'].astype(str) + dfestoque['TAM'].astype(str)
    dfestoque["PRAZO"] = pd.to_datetime(dfestoque["PRAZO"]).dt.date
    dfestoque = dfestoque.loc[dfestoque['PRAZO'] <= dfdatas.loc[i, "Date-Time"]]
    dfestoque = dfestoque.groupby(['chave'], dropna=False)['QTD'].sum()

    left_join = pd.merge(final, dfestoque, on='chave', how='left')
    basefinal = pd.DataFrame(left_join)

    conditions = [
        (basefinal['Tipord'] == 'ZBME') | (basefinal['Tipord'] == 'ZBRI') | (basefinal['Tipord'] == 'ZBRM') | (
                    basefinal['Tipord'] == 'ZBTM') | (basefinal['Tipord'] == 'ZCO2') | (
                    basefinal['Tipord'] == 'ZLCM') | (basefinal['Tipord'] == 'ZLWC') | (
                    basefinal['Tipord'] == 'ZMOT') | (basefinal['Tipord'] == 'ZCO1'),
        (basefinal['Tipord'] == 'ZEXF'),
        (basefinal['Tipord'] == 'ZLOP') | (basefinal['Tipord'] == 'ZREP') | (basefinal['Tipord'] == 'ZAPL'),
        (basefinal['Tipord'] == 'ZLWE') | (basefinal['Tipord'] == 'ZAPW'),
        (basefinal['Tipord'] == 'ZMAM') | (basefinal['Tipord'] == 'ZMOS') | (basefinal['Tipord'] == 'ZNOR') | (
                    basefinal['Tipord'] == 'ZKHD') | (basefinal['Tipord'] == 'ZKIL') | (basefinal['Tipord'] == 'ZAFQ'),
    ]
    choices = [1, 2, 4, 5, 3]
    basefinal['Indice tipord'] = np.select(conditions, choices, default=1)

    indcanal = [

        (basefinal['Chave canal'] == '50FQ'),
        (basefinal['Chave canal'] == '50VJ'),
        (basefinal['Chave canal'] == '61FQ'),
        (basefinal['Chave canal'] == '62FQ'),
        (basefinal['Chave canal'] == '63DG'),
        (basefinal['Chave canal'] == '63FQ'),
        (basefinal['Chave canal'] == '64FQ'),
        (basefinal['Chave canal'] == '65VJ'),
        (basefinal['Chave canal'] == '66VJ'),
        (basefinal['Chave canal'] == '67VJ'),
        (basefinal['Chave canal'] == '68VJ'),
        (basefinal['Chave canal'] == '68FQ'),
        (basefinal['Chave canal'] == '69FQ'),
        (basefinal['Chave canal'] == '70VJ'),
        (basefinal['Chave canal'] == '70DG'),
        (basefinal['Chave canal'] == '73VJ'),
        (basefinal['Chave canal'] == '75VJ'),
        (basefinal['Chave canal'] == '76FQ'),
        (basefinal['Chave canal'] == '77FQ'),
        (basefinal['Chave canal'] == '78VJ'),
        (basefinal['Chave canal'] == '78FQ'),
        (basefinal['Chave canal'] == '79FQ'),
        (basefinal['Chave canal'] == '80VJ'),
        (basefinal['Chave canal'] == '97FQ'),
        (basefinal['Chave canal'] == '98FQ'),
        (basefinal['Chave canal'] == '98VJ'),
        (basefinal['Chave canal'] == '99VJ'),
        (basefinal['Chave canal'] == '99FQ'),
        (basefinal['Chave canal'] == '50MM'),
        (basefinal['Chave canal'] == '65MM'),
        (basefinal['Chave canal'] == '66MM'),
        (basefinal['Chave canal'] == '67MM'),
        (basefinal['Chave canal'] == '68MM'),
        (basefinal['Chave canal'] == '70MM'),
        (basefinal['Chave canal'] == '73MM'),
        (basefinal['Chave canal'] == '75MM'),
        (basefinal['Chave canal'] == '78MM'),
        (basefinal['Chave canal'] == '80MM'),
        (basefinal['Chave canal'] == '98MM'),
        (basefinal['Chave canal'] == '99MM'),
        (basefinal['Chave canal'] == '58VJ'),
        (basefinal['Chave canal'] == '75FQ'),
        (basefinal['Chave canal'] == '81PL'),
        (basefinal['Chave canal'] == '99TX'),
        (basefinal['Chave canal'] == '98EX'),
        (basefinal['Chave canal'] == '70KA'),
        (basefinal['Chave canal'] == '77LP'),
        (basefinal['Chave canal'] == '58MM'),
        (basefinal['Chave canal'] == '77LJ'),

    ]

    canalfila = ['FQ', 'MM', 'FQ', 'LP', 'WEB', 'WEB', 'FQ', 'MM', 'MM', 'MM', 'MM', 'MM', 'FQ', 'KA', 'KA', 'MM', 'MM',
                 'LP', 'LP', 'MM', 'MM', 'FQ', 'MM', 'MI', 'MI', 'MI', 'MM', 'FQ', 'MM', 'MM', 'MM', 'MM', 'MM', 'KA',
                 'MM', 'MM', 'MM', 'MM', 'MI', 'MM', 'MM', 'MM', 'MM', 'MM', 'MI', 'KA', 'LP', 'MM', 'LP']
    basefinal['Canal'] = np.select(indcanal, canalfila, default=basefinal['Can'])

    canais = [

        (basefinal['Canal'] == 'MI'),
        (basefinal['Canal'] == 'KA'),
        (basefinal['Canal'] == 'MM'),
        (basefinal['Canal'] == 'FQ'),
        (basefinal['Canal'] == 'LP'),
        (basefinal['Canal'] == 'WEB'),

    ]
    canalind = [MI, KA, MM, FQ, LP, WEB]
    basefinal['Indice Canal'] = np.select(canais, canalind, default=1)

    var2 = basefinal.sort_values(by=['chave', 'Embarque', 'Sit', 'Indice tipord', 'Indice Canal', 'Ordem'])

    dfarray = pd.DataFrame(var2)

    dados = dfarray.to_numpy()

    lin, col = dados.shape
    z = lin
    b = 1

    dados[0, 16] = 0
    while b < z:
        if dados[b, 13] == dados[b - 1, 13]:
            dados[b, 16] = dados[b - 1, 16] + dados[b - 1, 11]
        else:
            dados[b, 16] = 0

        dados[b, 15] = dados[b, 22] - dados[b, 16]

        try:
            dados[b, 17] = dados[b, 12] / dados[b, 11]
        except:
            dados[b, 17] = 0

        b = b + 1

    a = 0
    while a < z:
        if dados[a, 15] > 0 and dados[a, 15] >= dados[a, 11]:
            dados[a, 18] = dados[a, 11]
        elif dados[a, 15] > 0 and dados[a, 15] < dados[a, 11]:
            dados[a, 18] = dados[a, 15]
        else:
            dados[a, 18] = 0

        dados[a, 20] = dados[a, 18] * dados[a, 17]
        dados[a, 19] = dados[a, 11] - dados[a, 18]
        dados[a, 21] = dados[a, 12] - dados[a, 20]
        a = a + 1

    dbconfig = pd.DataFrame(dados)
    dbconfig.columns = ["Can", "Artigo", "Tamanho", "Ordem", "Tipord", "Esc", "Sit", "Mês", "Embarque", "Colecao",
                        "Neg", "Pecas", "Valor", "chave", "Chave canal", "Est liq", "Cart acum", "Unit", "Pçs atende",
                        "Pçs falta", "Vlr atende", "Vlr falta", "QTD", "Indice tipord", "Canal", "Indice Canal"]

    dbconfig.drop("Can", axis=1, inplace=True)
    dbconfig.drop("chave", axis=1, inplace=True)
    dbconfig.drop("Chave canal", axis=1, inplace=True)
    dbconfig.drop("Est liq", axis=1, inplace=True)
    dbconfig.drop("Cart acum", axis=1, inplace=True)
    dbconfig.drop("Unit", axis=1, inplace=True)
    dbconfig.drop("QTD", axis=1, inplace=True)
    dbconfig.drop("Indice tipord", axis=1, inplace=True)
    dbconfig.drop("Indice Canal", axis=1, inplace=True)

    dbconfig["Posição"] = dfdatas.loc[i, "Date-Time"]
    teste = dfdatas.loc[i, "Date-Time"].strftime("%d%m%y")

    #geral = pd.merge(dbconfig, conartigos, left_on=["Artigo"], right_on=["Artigo"], how="left").merge(conembarques, on="Embarque", how="left").merge(conclientes, on="Ordem", how="left")

    dbconfig = pd.merge(dbconfig, conartigos, on="Artigo", how="left")
    dbconfig = pd.merge(dbconfig, conembarques, on="Embarque", how="left")
    dbconfig = pd.merge(dbconfig, conclientes, on="Ordem", how="left")

    dbconfig["Ordem art"] = dbconfig["Ordem"].astype(str) + dbconfig["Artigo"].astype(str)
    dbconfig = pd.merge(dbconfig, vendalivre, on="Ordem art", how="left")
    dbconfig.drop("Ordem art", axis=1, inplace=True)

    # geral = geral.loc[geral["Embarque"] <= datetime.date(2024, 1, 31)]
    # geral = geral.loc[geral["Canal"] == "MI"]
    # geral.to_csv(pathgeral + "Geralzasso " + teste + ".csv", index=False)

    # ka = pd.DataFrame(geral)
    # ka = ka.loc[ka["Canal"] == "KA"]
    # ka.to_csv(pathgeral + "KA " + teste + ".csv")

    # fq1 = pd.DataFrame(geral)
    # fq2 = pd.DataFrame(geral)
    # fq3 = pd.DataFrame(geral)

    # fq1 = fq1.loc[(fq1['Canal'] == "FQ") & (fq1['Embarque'] <= primeirocorte)]
    # fq2 = fq2.loc[(fq2['Canal'] == "FQ") & (fq2['Embarque'] > primeirocorte) & (fq2['Embarque'] <= segundocorte)]
    # fq3 = fq3.loc[(fq3['Canal'] == "FQ") & (fq3['Embarque'] > segundocorte) & (fq3['Embarque'] <= terceirocorte)]

    # fq1.to_csv(pathgeral + "FQ1 " + teste + ".csv")
    # fq2.to_csv(pathgeral + "FQ2 " + teste + ".csv")
    # fq3.to_csv(pathgeral + "FQ3 " + teste + ".csv")

    # mm1 = pd.DataFrame(geral)
    # mm2 = pd.DataFrame(geral)
    # mm3 = pd.DataFrame(geral)

    # mm1 = mm1.loc[(mm1['Canal'] == "MM") & (mm1['Embarque'] <= primeirocorte)]
    # mm2 = mm2.loc[(mm2['Canal'] == "MM") & (mm2['Embarque'] > primeirocorte) & (mm2['Embarque'] <= segundocorte)]
    # mm3 = mm3.loc[(mm3['Canal'] == "MM") & (mm3['Embarque'] > segundocorte) & (mm3['Embarque'] <= terceirocorte)]
    # mm1.to_csv(pathgeral + "MM1 " + teste + ".csv")
    # mm2.to_csv(pathgeral + "MM2 " + teste + ".csv")
    # mm3.to_csv(pathgeral + "MM3 " + teste + ".csv")

    # Usar essa extração pra desgraça dos pedidos suspensos com estoque
    # geral = geral.groupby(["Ordem","Cliente CNPJ","Cliente Cód","Cliente","Estado", "Tipord", "Colecao", "Neg", "Canal", "Posição", "Grupo", "LINX Tipo", "Gênero", "Tipo Material","Produção (P/T)", "Origem (N/I)", "Linha", "Origem", "Bloco", "Período", "Status final","Sit","Embarque","Centro Cód","NR_PEDCLI","Neg gen","Cond pgto","Status entrada"], dropna=False)["Pecas", "Valor", "Pçs atende", "Pçs falta", "Vlr atende", "Vlr falta"].sum().reset_index()

    # Versao caaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    # geral = geral.groupby(
    #    [ "Tipord", "Colecao", "Neg", "Canal", "Posição", "Grupo", "LINX Tipo", "Gênero", "Tipo Material",
    #     "Produção (P/T)", "Origem (N/I)", "Linha", "Origem", "Bloco", "Período", "Status final", "Sit",
    #     "Embarque", "Centro Cód", "NR_PEDCLI", "Neg gen", "Cond pgto", "Status entrada"], dropna=False)[
    #    "Pecas", "Valor", "Pçs atende", "Pçs falta", "Vlr atende", "Vlr falta"].sum().reset_index()

    dbconfig = dbconfig.groupby(
        ["Artigo", "Tipord", "Colecao", "NEGOCIO", "Canal", "Posição", "GRUPO", "MATERIAL", "GENERO", "Tipo material",
         "Fabricação P/T", "Origem N/I", "LINHA", "Origem final", "Bloco", "Período", "Tamanho", "Sit",
         "Embarque", "Centro", "Neg gen", "Status entrada","NR_PEDCLI","Cond pgto"], dropna=False)[[
        "Pecas", "Valor", "Pçs atende", "Pçs falta", "Vlr atende", "Vlr falta"]].sum().reset_index()
    dbconfig.to_csv(Parametros.cart_x_proj + "Resumo novo" + teste + ".csv", index=False)

juntatudo()
# junta_base_geral()