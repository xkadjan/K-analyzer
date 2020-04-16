# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 22:37:11 2019

@author: xkadj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plot

#path = [r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logy\napalete.csv"]
#path = [r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logy\dlouhajizda.csv"]
#path = [r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\can.txt"]
path = [r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\tmp.csv"]

# =============================================================================
# 
# =============================================================================
 
def get_current(messages, message_ID):
    values = []
    for row in range(len(messages)):
        if messages[row][0] == message_ID:
            value = (int(messages[row][1][4:6],16)*255 + int(messages[row][1][6:8],16))
            if value > 32767: value = value - 65535
            values.append((value * 10))
    mean = np.array(values).mean()
    return values, mean

# =============================================================================
# MAIN
# =============================================================================

for file in path:
    message_ID = 145
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values, mean = get_current(messages, message_ID)
    print(file.split('\\')[-1],mean)
    plot.plot(values,'r.-', linewidth=0.5, label='motor_91h_current[mA]')

for file in path:
    message_ID = 146
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values, mean = get_current(messages, message_ID)
    print(file.split('\\')[-1],mean)
    plot.plot(values,'g.-', linewidth=0.5, label='motor_92h_current[mA]')

for file in path:
    message_ID = 147
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values, mean = get_current(messages, message_ID)
    print(file.split('\\')[-1],mean)
    plot.plot(values,'y.-', linewidth=0.5, label='motor_93h_current[mA]')
    
for file in path:
    message_ID = 148
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values, mean = get_current(messages, message_ID)
    print(file.split('\\')[-1],mean)
    plot.plot(values,'k.-', linewidth=0.5, label='motor_94h_current[mA]')
    
for file in path:
    message = 130
    list_of_angles = []
    rows = pd.read_csv(file, sep=';', engine='python').values.tolist()
    for row in range(len(rows)):
        if rows[row][0] == message: list_of_angles.append(int(rows[row][1][4:6],16)*255 + int(rows[row][1][6:8],16))      
    list_of_angles_np = np.array(list_of_angles)
    mean = list_of_angles_np.mean()
    print(file.split('\\')[-1],mean)
    plot.plot(list_of_angles,'b.-',linewidth=0.1,label='battery_voltage[A]')
#    plot.plot([0,len(list_of_angles_np)],[mean,mean],'r-')
#    
    
plot.figure(num=1, figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')    
plot.minorticks_on()
plot.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
plot.style.use('seaborn-paper')
plot.grid(True)
plot.legend(loc=1)
plot.tight_layout()

plot.title('voltage/current', size=12, loc='left')
plot.xlabel('sample[-]',size=10)
plot.ylabel('voltage[mV] / current [mA/10]',size=10)
    
