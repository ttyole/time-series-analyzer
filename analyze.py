#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import numpy as np
import pandas as pd

def analyze_file(file):
    data = pd.read_csv(file, sep = ',', parse_dates = True)
    dt = np.dtype('U25,f')
    results = np.array([(file.filename,np.nan),('Mean',0)], dtype=dt)
    dateString =  str(datetime.datetime.now()).replace(" ", "_").replace(".", "-").replace(':','-')
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, 'history',dateString +'.csv')
    np.savetxt(path , results, fmt='%s, %.18e')
    return dateString
