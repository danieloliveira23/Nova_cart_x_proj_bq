import pandas as pd

import Parametros


basezext = pd.read_excel(Parametros.saplimpar + "Pegar ZEXT.xlsx", skiprows=6)
basezext=basezext.rename(columns=lambda x: x.strip())
basezext = basezext[["Doc.ref."]]
basezext = basezext.dropna()
basezext = basezext.drop_duplicates()
print(basezext.head(10))
basezext = basezext.loc[basezext["Doc.ref."] != "Doc.ref."]
basezext.to_csv(Parametros.depara + "Base ZEXT para jogar no SAP.csv", index=False)