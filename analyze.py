#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os, sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def analyze_file(file):
    """
        Analyse le fichier 'file' et les enregistre dans une nouvelle ligne du fichier history.csv
        Retourne l'index de cette nouvelle analyse dans history.csv
    """

    data = pd.read_csv(file, sep=',', parse_dates=[0], names=['date', 'value'], header=0, dayfirst=True)

    # On récupère toutes les données numériques intéressantes
    results = {}
    results['filename'] = file.filename
    results['date'] = str(datetime.datetime.now()).replace(" ", "_").replace(".", "-").replace(':','-')
    results['Mean'] = data.value.mean()
    results['Variance'] = data.value.var()
    results['1st quartile'] = data['value'].quantile(0.25)
    results['2nd quartile'] = data['value'].quantile(0.5)
    results['3rd quartile'] = data['value'].quantile(0.75)
    results['Minimum date'] = data.date.iloc[data.value.idxmin()].strftime('%d/%m/%Y')
    results['Minimum'] = data.value.min()
    results['Maximum date'] = data.date.iloc[data.value.idxmax()].strftime('%d/%m/%Y')
    results['Maximum'] = data.value.max()

    # On crée un graphe traçant la valeur et la fft du csv 
    fig, (ax1, ax2) = plt.subplots( nrows=2, ncols=1 )  # create figure & 1 axis
    ax1.plot( data['date'], data['value'])
    ax1.set_ylabel('Value')
    ax2.plot( range(data.shape[0]), np.fft.fft(data['value'] - data.value.mean()))
    ax2.set_ylabel('FFT')
    # On l'enregistre dans le dossier static
    path_graph = os.path.join(os.path.dirname(__file__), 'static',results['date'] + '.png')
    fig.savefig(path_graph)
    plt.close(fig)

    # On charge tous nos résultats dans une dataframe qu'on ajoute à history.csv
    results_df = pd.DataFrame(results, index=[1])
    path_history = os.path.join(os.path.dirname(__file__), 'history.csv')
    try:
        history = pd.read_csv(path_history,',')
        history = history.append(results_df, ignore_index=True)
    # Si history.csv n'existe pas, on le crée
    except:
        history = pd.DataFrame(results_df)
    history.to_csv(path_history)

    # On retourne l'index de la nouvelle analyse
    return history.shape[0]-1
