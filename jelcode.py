#!/usr/bin/env python

import pandas as pd
import numpy as np

x = pd.read_excel("PubEst_2020_backup.xlsx", "Stata")
x.columns = ["pub_date", "pub_type", "JEL_co_1", "JEL_co_2",
             "JEL_co_3", "JEL_co_4", "JEL_co_5", "JEL_co_6", "JEL_co_7"]

# rimuovo gli NA generati dalla celle vuote di read_excel        
x.fillna('', inplace=True)

# filtro i dati (TBD)     
x = x[x.pub_date != "Forthcoming"]
x = x[x.pub_date > 2015]
x = x[x.pub_type != "Editor's Introduction"]
x = x[x.pub_date <= 2020 ]
x = x[x.pub_date != ""]

#todo: probabile errore, sego una lettera di jelcode, cosi' E32 ed E31 sono la stessa cosa
# genero i nomi jelco1, jelco2, ... jelco7 con u substr dei jelcodes originali

for i in range(1, 8):
    src_name = "JEL_co_" + str(i)
    x[src_name] = x[src_name].apply(lambda y: y.strip())

# genero la colonna

x = x.replace("", np.NaN)
x["jel_count"] = x.apply(lambda y: 7-y[["JEL_co_1", "JEL_co_2", "JEL_co_3", "JEL_co_4", "JEL_co_5", "JEL_co_6", "JEL_co_7"]].isnull().sum(), axis="columns")
x["wei_ght"] = x.apply(lambda y: 1./(7-y[["JEL_co_1", "JEL_co_2", "JEL_co_3", "JEL_co_4", "JEL_co_5", "JEL_co_6", "JEL_co_7"]].isnull().sum()), axis="columns")

d1 = x[["pub_date", "JEL_co_1", "wei_ght"]]
d1.columns = ["pub_date", "jelcode", "weight"]

for i in range(2, 8):
    src_name = "JEL_co_" + str(i)
    d2 = x[["pub_date", src_name, "wei_ght"]]
    d2.columns = ["pub_date", "jelcode", "weight"]
    d1 = d1.append(d2)
    
d1 = d1[~d1.jelcode.isnull()]
d1["j1"] = d1.jelcode.apply(lambda y: y[0])
 