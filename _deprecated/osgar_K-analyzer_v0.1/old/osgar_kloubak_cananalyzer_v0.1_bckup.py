# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:52:25 2019

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
# =============================================================================
#     bytes 0-3 are the current RPM as a whole number, from most significant byte to least significant, respectively.
#     bytes 4-5 are the current current, most to least, but I’m not sure what units yet.
#     bytes 6-7 are the current dutycycle in 10ths of a percent, from most to least.
# =============================================================================
    values = []
    for row in range(len(messages)):
        if messages[row][2] == message_ID:
            erpm = int(messages[row][3][0:8],16)
            if erpm > 2147483647: erpm = erpm - 4294967294
            current = int(messages[row][3][8:12],16)
            if current > 32767: current = current - 65534
            duty_cycle = int(messages[row][3][12:16],16)
            if duty_cycle > 32767: duty_cycle = duty_cycle - 65534
            values.append([messages[row][1], erpm, current/10, duty_cycle])
    values = pd.DataFrame(values,columns=['time','erpm','current','duty_cycle'])
    return values

def get_voltage(messages, message_ID):
    values = []
    for row in range(len(messages)):
        if messages[row][2] == message_ID:
            value = (int(messages[row][3][4:6],16)*255 + int(messages[row][3][6:8],16))
#            if value > 32767: value = value - 65535
            values.append([messages[row][1], value/1000])
    values = pd.DataFrame(values,columns=['time','voltage'])
    mean = np.array(values).mean()
    return values, mean

# =============================================================================
# MAIN
# =============================================================================

for file in path:
    message_ID = 145
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values = get_current(messages, message_ID)
    plot.plot(values.time,values.current,'r.-', linewidth=0.5, label='motor_F-R(91h)_current[A]')

for file in path:
    message_ID = 146
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values = get_current(messages, message_ID)
    plot.plot(values.time,values.current,'g.-', linewidth=0.5, label='motor_F-L(92h)_current[A]')
    
for file in path:
    message_ID = 147
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values = get_current(messages, message_ID)
    plot.plot(values.time,values.current,'y.-', linewidth=0.5, label='motor_R-R(93h)_current[A]')
    
for file in path:
    message_ID = 148
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values = get_current(messages, message_ID)
    plot.plot(values.time,values.current,'k.-', linewidth=0.5, label='motor_R-L(94h)_current[A]')
    
    
for file in path:
    message_ID = 130
    messages = pd.read_csv(file, sep=';', engine='python').values.tolist()
    values, mean = get_voltage(messages, message_ID)
#    print(file.split('\\')[-1],mean)
    plot.plot(values.time,values.voltage,'b.-', linewidth=1, label='vesc_voltage[V]')
  
plot.figure(num=1, figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')    
plot.minorticks_on()
plot.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
plot.style.use('seaborn-paper')
plot.grid(True)
plot.legend(loc=1)
plot.tight_layout()

plot.title('voltage/current', size=12, loc='left')
plot.xlabel('sample[-]',size=10)
plot.ylabel('voltage[V] / current [A]',size=10)
    
