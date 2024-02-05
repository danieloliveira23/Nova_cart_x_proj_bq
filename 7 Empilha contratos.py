import pandas as pd
import numpy as np


import Parametros


df = pd.read_csv(Parametros.cart_x_proj + "Leresse 2.csv", low_memory=False)
contratos = pd.read_excel(Parametros.depara + "teste contratos.xlsx")
contratos["Embarque"] = pd.to_datetime(contratos["Embarque"]).dt.date

final = pd.concat([df, contratos])

final.to_csv(Parametros.cart_x_proj + "Leresse 3.csv", index=False)