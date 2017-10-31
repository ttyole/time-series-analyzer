#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, flash, redirect, url_for, render_template
import pandas as pd
from analyze import analyze_file

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
        Route de base autorisant l'utilisateur à upload un nouveau .csv ou a accéder
        à l'historique des anciennes analyses
    """
    if request.method == 'POST':
        # on vérifie que la requete contient un fichier
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # on vérifie que le fichier envoyé est bien un .csv
        if not file.filename.endswith('.csv'):
            flash('Incorrect file. Please upload a csv file')
            return redirect(request.url)
        # on analyse le fichier, puis on redirige sur la page de son analyse
        if file:
            result_index = analyze_file(file)
            return redirect(url_for('show_analysis',
                                    result_index=result_index))
    # si cette route est appelée avec la méthode GET, on récupère l'historique des 
    # analyses grace au fichier history.csv et on affiche le template upload.html 
    # avec cet historique
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'history.csv')
    try:
        history = pd.read_csv(path, sep=",")
    except:
        history = pd.DataFrame([])
    return render_template('upload.html', history=history)



@app.route('/analysis')
def show_analysis():
    """
        Route affichant une analyse.
        L'analyse est récupérée dans le fichier history.csv, à l'index indiqué en
        paramètre http de cette route.
    """
    result_index = int(request.args.get('result_index', ''))
    directory = os.path.dirname(__file__)
    path = os.path.join(directory, 'history.csv')
    # on affiche le template analysis.html avec les données d'analyses récupérés
    return render_template('analysis.html', analysis=pd.read_csv(path, sep=",").loc[[result_index]])
