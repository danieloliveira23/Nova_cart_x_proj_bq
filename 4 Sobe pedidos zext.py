import pandas as pd
import numpy as np

import Parametros



dfvendas = pd.read_csv(Parametros.cart_x_proj + "Leresse 1.csv", low_memory=False)

exportacao = pd.read_excel(Parametros.depara + "ZEXT para subir leresse.xlsx")
exportacao["Embarque"] = pd.to_datetime(exportacao["Embarque"]).dt.date
final = pd.concat([dfvendas, exportacao])
final.to_csv(Parametros.cart_x_proj + "Leresse 2.csv", index=False)


