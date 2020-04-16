# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:12:12 2020

@author: xkadj
"""
import pandas as pd


tcan_file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\K3_200115\trace_test.trc"

#tcan_messages = pd.read_csv(tcan_file, sep='[     ,  ]', skiprows=16, engine='python')#.values.tolist()
tcan_messages = pd.read_csv(tcan_file, sep='     ', skiprows=16, engine='python')#.values.tolist()