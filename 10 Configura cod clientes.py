import pandas as pd
import numpy as np

import Parametros

ordens = pd.read_csv(Parametros.cart_x_proj + "Leresse 3.csv", low_memory=False)

nacional = pd.read_csv(Parametros.cart_x_proj + "Leresse original bq.csv", low_memory=False)
nacional["Cliente_CNPJ"] = nacional["Cliente_CNPJ"].astype(str)
nacional["Cliente_CNPJ"] = str("00000000000000") + nacional["Cliente_CNPJ"].astype(str)
nacional["Cliente_CNPJ"] = nacional["Cliente_CNPJ"].str[-16:]
nacional["Cliente_CNPJ"] = nacional["Cliente_CNPJ"].str[:14]


nacional = nacional[["Ordem", "Centro","Cliente_CNPJ"]]
nacional["Ordem"] = nacional["Ordem"].astype(str)
nacional.drop_duplicates(subset="Ordem", inplace=True)

ordens = ordens[["Ordem"]]
ordens["Ordem"] = ordens["Ordem"].astype(str)
ordens.drop_duplicates(subset="Ordem", inplace=True)
ordens = pd.merge(ordens, nacional, on="Ordem", how="left")

##############################################################################################



basezext = pd.read_excel(Parametros.saplimpar + "ZEXT para configurar.xlsx", skiprows=6)
basezext=basezext.rename(columns=lambda x: x.strip())

basezext.dropna(
    axis=0,
    how='any',
    subset=["Doc.venda"],
    inplace=True
)
basezext = basezext.loc[basezext["CDst"] != "CDst"]
basezext = basezext[["Doc.venda","EmissorOrd","Cen."]]
basezext.rename(columns={"Doc.venda" : "Ordem"}, inplace=True)
basezext.rename(columns={"Cen." : "Centro"}, inplace=True)
basezext.drop_duplicates(subset="Ordem", inplace=True)
basezext["Ordem"] = basezext["Ordem"].astype(str)

saldocontrato = pd.read_excel(Parametros.saplimpar + "Saldo contrato para configurar.xlsx",skiprows=6)
saldocontrato = saldocontrato.rename(columns=lambda  x: x.strip())
saldocontrato = saldocontrato.loc[saldocontrato["Doc.venda"] != "Doc.venda"]

saldocontrato.dropna(
    axis=0,
    how='any',
    subset=["Doc.venda"],
    inplace=True)
saldocontrato = saldocontrato[["Doc.venda","EmissorOrd","Cen."]]
saldocontrato["Doc.venda"] = saldocontrato["Doc.venda"].astype(str)
saldocontrato.rename(columns={"Doc.venda" : "Ordem"}, inplace=True)
saldocontrato.rename(columns={"Cen." : "Centro"}, inplace=True)

final = pd.concat([basezext, saldocontrato])
final.drop_duplicates(subset="Ordem", inplace=True)

cod_clientes = pd.read_csv(Parametros.depara + "Cod_geral_clientes.csv", low_memory=False)
cod_clientes = cod_clientes[["KUNNR_ID","CNPJ"]]
cod_clientes.rename(columns={"KUNNR_ID": "EmissorOrd"}, inplace=True)
cod_clientes["CNPJ"] = cod_clientes["CNPJ"].astype(str)
cod_clientes["CNPJ"] = str("00000000000000") + cod_clientes["CNPJ"].astype(str)
cod_clientes["CNPJ"] = cod_clientes["CNPJ"].str[-16:]
cod_clientes["CNPJ"] = cod_clientes["CNPJ"].str[:14]
cod_clientes.drop_duplicates(subset="EmissorOrd", inplace=True)

final = pd.merge(final, cod_clientes, on="EmissorOrd", how="left")
final = final[["Ordem","Centro","CNPJ"]]
final.drop_duplicates(subset="Ordem", inplace=True)



##############################################################################################

ordens = pd.merge(ordens, final, on="Ordem", how="left")
ordens["Centro final"] = np.where(ordens["Centro_x"].isnull(), ordens["Centro_y"], ordens["Centro_x"])
ordens["CNPJ final"] = np.where(ordens["Cliente_CNPJ"].isnull(), ordens["CNPJ"], ordens["Cliente_CNPJ"])

ordens = ordens[["Ordem","CNPJ final","Centro final"]]
ordens.rename(columns={"CNPJ final":"CNPJ"}, inplace=True)
ordens.rename(columns={"Centro final":"Centro"}, inplace=True)

ordens.drop_duplicates(subset="Ordem", inplace=True)

geral = pd.read_csv(Parametros.depara + "Cod_geral_clientes.csv", low_memory=False)

geral["CNPJ"] = geral["CNPJ"].astype(str)
geral["CNPJ"] = str("00000000000000") + geral["CNPJ"].astype(str)
geral["CNPJ"] = geral["CNPJ"].str[-16:]
geral["CNPJ"] = geral["CNPJ"].str[:14]

geral.drop_duplicates(subset="CNPJ", inplace=True)
geral.rename(columns={"KUNNR_ID":"Código cliente"}, inplace=True)
geral.rename(columns={"Nome_1":"Nome cliente"}, inplace=True)
geral.rename(columns={"Regiao":"Estado"}, inplace=True)

ordens = pd.merge(ordens, geral, on="CNPJ", how="left")

condicao = pd.read_csv(Parametros.depara + "Cond pagamento.TXT", sep=";", low_memory=False)
condicao = condicao[["OrdSAP", "ConpagOrd"]]
condicao["OrdSAP"] = condicao["OrdSAP"].astype(str)
condicao["ConpagOrd"] = condicao["ConpagOrd"].astype(str)
condicao.rename(columns={"OrdSAP" : "Ordem"}, inplace=True)
condicao.drop_duplicates(subset="Ordem", inplace=True)
condicao.rename(columns={"ConpagOrd" : "Cond pgto"}, inplace=True)
condicao["Condição pagamento"] = np.where(condicao["Cond pgto"] == "C091", "Antecipado", "Demais")
condicao = condicao[["Ordem", "Condição pagamento"]]

ordens = pd.merge(ordens, condicao, on="Ordem", how="left")
ordens["Cond pgto"] = np.where(ordens["Condição pagamento"] == "Antecipado", "Antecipado","Demais")
ordens.drop("Condição pagamento", axis=1, inplace=True)

nomes = pd.read_excel(Parametros.depara + "Nome pedidos.xlsx")
nomes["Ordem"] = nomes["Ordem"].astype(str)
nomes.drop_duplicates(subset="Ordem", inplace=True)

ordens = pd.merge(ordens, nomes, on="Ordem", how="left")


ordens.to_csv(Parametros.cart_x_proj + "Cod_clientes_novo.csv", index=False)


