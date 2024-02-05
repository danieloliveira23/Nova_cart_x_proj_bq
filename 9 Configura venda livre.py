import pandas as pd
import numpy as np
import os

import Parametros

df = pd.read_csv(Parametros.saplimpar + "Venda livre bq.csv", low_memory=False)

df.rename(columns={"Doc_Venda": "Doc.venda"}, inplace=True)
df.rename(columns={"Venda_Livre": "Status entrada"}, inplace=True)

df["Ordem art"] = df["Doc.venda"].astype(str) + df["Material"].astype(str)
df.drop_duplicates(subset="Ordem art", inplace=True)
df = df[["Ordem art", "Status entrada"]]
df = df.loc[:, ["Ordem art","Status entrada"]]
df.to_csv(Parametros.cart_x_proj + "Venda livre.csv", index=False)