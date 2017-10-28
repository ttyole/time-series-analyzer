#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, flash, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import numpy as np
import config
from analyze import analyze_file

app = Flask(__name__)
app.config.from_object(config)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        print(file.filename)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not file.filename.endswith('.csv'):
            flash('Incorrect file. Please upload a csv file')
            return redirect(request.url)
        if file:
            analysis_file_name = analyze_file(file)
            return redirect(url_for('show_analysis',
                                    filename=analysis_file_name))
    return render_template('upload.html')

@app.route('/analysis')
def show_analysis():
    date_string = request.args.get('filename', '')
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'history',date_string +'.csv')
    dt = np.dtype('U25,f')
    return render_template('analysis.html', analysis=np.loadtxt(path, delimiter=",", dtype=dt))
