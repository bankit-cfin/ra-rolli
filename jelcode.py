#!/usr/bin/env python

import pandas as pd
import numpy as np

def build_dataset(filename = "data/data.xlsx", sheet = "Stata"):
    """Costruisce il dataset"""
    x = pd.read_excel("data/data.xlsx", "Stata")
    x.columns = [
        "pub_date", "pub_type", "JEL_co_1", "JEL_co_2",
        "JEL_co_3", "JEL_co_4", "JEL_co_5", "JEL_co_6", 
        "JEL_co_7"
    ]

    # rimuovo gli NA generati dalla celle vuote di read_excel        
    x.fillna('', inplace=True)

    # filtro i dati (TBD)     
    x = x[x.pub_date != "Forthcoming"]
    x = x[x.pub_date > 2015]
    x = x[x.pub_type != "Editor's Introduction"]
    x = x[x.pub_date != ""]

    for i in range(1, 7 + 1):
        src_name = "JEL_co_" + str(i)
        x[src_name] = x[src_name].apply(lambda y: y.strip())

    jelcodes_array = [
        "JEL_co_1", "JEL_co_2", "JEL_co_3", 
        "JEL_co_4", "JEL_co_5", "JEL_co_6", 
        "JEL_co_7"
    ]

    # mi sono utili i NaN...
    x = x.replace("", np.NaN)
    x["jel_count"] = x.apply(lambda y: 7-y[jelcodes_array].isnull().sum(), axis="columns")
    x["wei_ght"] = x.apply(lambda y: 1./y.jel_count, axis="columns")

    # metto in colonna i jelcodes con i rispettivi pesi
    d1 = x[["pub_date", "JEL_co_1", "wei_ght"]]
    d1.columns = ["pub_date", "jelcode", "weight"]

    for i in range(2, 8):
        src_name = "JEL_co_" + str(i)
        d2 = x[["pub_date", src_name, "wei_ght"]]
        d2.columns = ["pub_date", "jelcode", "weight"]
        d1 = d1.append(d2)
    
    # elimino il contributo per assenza di jelcodes
    d1 = d1[~d1.jelcode.isnull()]
    
    # converto tutti i jelcodes in maiuscolo
    d1["jelcode"] = d1.jelcode.str.upper()

    return d1

# G                    mercati finanziari e banche
# F                    economia internazionale, commercio, cambi
# E3-E5                politica monetaria, prezzi, ciclo economico
# C                    econometria, metodi matematici
# D6,J,M               mercato del lavoro, salari, innovazione
# D1-D5,D7-D8,E1-E2,   consumo, risparmio, redditi, ricchezza
# E6,H                 politica fiscale
# K,L                  economia industriale
# O,I,N                educazione, salute, sviluppo, storia
# Q,R,Y,Z,P,D9,A,B     residui: economia regionale, energia, mercato immobiliare

default_categories = {
    "Mercati finanziari e banche": ["G"],
    "Economia internazionale, commercio, cambi": ["F"],
    "Politica monetaria, prezzi, ciclo economico": ["E3", "E4", "E5"],
    "Econometria, metodi matematici": ["C"],
    "Mercato del lavoro, salari, innovazione": ["D6", "J", "M"],
    "Consumo, risparmio, redditi, ricchezza": ["D1", "D2" ,"D3", "D4", "D5", "D7", "D8", "E1", "E2"],
    "Politica fiscale": ["E6", "H"],
    "Economia industriale" : ["K", "L"],
    "Istruzione, salute, sviluppo economico, storia": ["O", "I", "N"],
    "Residui: economia regionale, energia e ambiente, mercato immobiliare": ["Q", "R", "Y", "Z", "P", "D9", "A" ,"B"]
}


def dataset(anni, d = build_dataset(), categories=default_categories):
    """Costruisce il dataset utile per il grafico"""
    # filtro gli anni
    d = d[d.pub_date.isin(anni)].copy()
    totale = d.weight.sum()
    d["percentuale"] = pd.Series(d.weight / totale, index=d.index)

    cat_column = []
    jelcodes_column = []
    percentuale_column = []

    considerati = pd.DataFrame(data=None, columns=d.columns)
    for label, jelcodes in categories.items():
        # non potendo facilmente selezionare i dati sul DataFrame
        # itero con un accumulatore
        aux = pd.DataFrame(data=None, columns=d.columns)
        for jcode in jelcodes:
            to_be_added = d[d.jelcode.str.startswith(jcode)]
            aux = aux.append(to_be_added)

        percentuale_categoria = aux.percentuale.sum()
        considerati = considerati.append(aux)
        # what a nasty, nasty, nasty way to do it...
        cat_column.append(label)
        jelcodes_column.append(", ".join(jelcodes))
        percentuale_column.append(percentuale_categoria)
    
    jelcode_residui = list(set(d.jelcode) ^ set(considerati.jelcode))
    
    cat_column.append("Residui non considerati")
    jelcodes_column.append(", ".join(jelcode_residui))
    percentuale_column.append(d[d.jelcode.isin(jelcode_residui)].percentuale.sum())

    return pd.DataFrame({ 
        "Categoria": cat_column,
        "jelcodes": jelcodes_column,
        "percentuale": percentuale_column
    })




