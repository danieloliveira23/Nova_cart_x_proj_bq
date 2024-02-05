import pandas as pd
import glob
import os
import datetime

import Parametros

#path = "C:\\Users\\daniel.silva\\Downloads\\automacao cart x proj\\"
path = Parametros.cart_x_proj


def juntatudo():
    var = ["Resumo novo*.csv"]
    for i in var:
        files = os.path.join(path, i)
        files = glob.glob(files)
        df = pd.concat(map(pd.read_csv, files), ignore_index=True)
        print(df)
        i = str.replace(i,"*","")
        df.to_csv(path + 'Total resumo novo ' + i)
