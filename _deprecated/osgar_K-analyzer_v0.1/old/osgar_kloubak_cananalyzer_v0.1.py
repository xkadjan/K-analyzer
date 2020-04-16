# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:52:25 2019

@author: xkadj
"""

import pandas as pd
#import numpy as np
import matplotlib.pyplot as plot

file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\tmp.csv"
 
def get_vesc_status(messages, message_ID):
# =============================================================================
#   VESC 90x message:
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
            values.append([messages[row][1], erpm/10, current/10, duty_cycle/10])
    values = pd.DataFrame(values,columns=['time','erpm','current','duty_cycle'])
    return values

def get_voltage(messages, message_ID):
    values = []
    for row in range(len(messages)):
        if messages[row][2] == message_ID:
            voltage = int(messages[row][3],16)
            values.append([messages[row][1], voltage/1000])
    values = pd.DataFrame(values,columns=['time','voltage'])
    return values

def plot_init(num):
    plot.figure(num=num, figsize=[7, 7], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')    
    plot.minorticks_on()
    plot.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    plot.style.use('seaborn-paper')
    plot.grid(True)   
    plot.tight_layout()
    return plot

# =============================================================================
# MAIN
# =============================================================================
    
messages = pd.read_csv(file, sep=';', engine='python').values.tolist()

values_0x91 = get_vesc_status(messages, 0x91)
values_0x92 = get_vesc_status(messages, 0x92)
values_0x93 = get_vesc_status(messages, 0x93)
values_0x94 = get_vesc_status(messages, 0x94)
values_0x81 = get_voltage(messages, 0x81)
values_0x82 = get_voltage(messages, 0x82)

plot_init(1)
plot.plot(values_0x91.time,values_0x91.current,'r.-', linewidth=0.5, label='motor_F-R(91h)_current[A]')
plot.plot(values_0x92.time,values_0x92.current,'g.-', linewidth=0.5, label='motor_F-L(92h)_current[A]')
plot.plot(values_0x93.time,values_0x93.current,'y.-', linewidth=0.5, label='motor_R-R(93h)_current[A]')
plot.plot(values_0x94.time,values_0x94.current,'k.-', linewidth=0.5, label='motor_R-L(94h)_current[A]')
plot.plot(values_0x81.time,values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
plot.plot(values_0x82.time,values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
plot.title('voltage/current', size=12, loc='left')
plot.xlabel('time[s]',size=10)
plot.ylabel('voltage[V] / current [A]',size=10)
plot.legend(loc=1)

plot_init(2)
plot.plot(values_0x91.time,values_0x91.erpm,'r.-', linewidth=0.5, label='motor_F-R(91h)_erpm[-]')
plot.plot(values_0x92.time,values_0x92.erpm,'g.-', linewidth=0.5, label='motor_F-L(92h)_erpm[-]')
plot.plot(values_0x93.time,values_0x93.erpm,'y.-', linewidth=0.5, label='motor_R-R(93h)_erpm[-]')
plot.plot(values_0x94.time,values_0x94.erpm,'k.-', linewidth=0.5, label='motor_R-L(94h)_erpm[-]')
plot.plot(values_0x81.time,values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
plot.plot(values_0x82.time,values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
plot.title('voltage/erpm', size=12, loc='left')
plot.xlabel('time[s]',size=10)
plot.ylabel('voltage[V] / erpm [-]',size=10)
plot.legend(loc=1)    

plot_init(3)
plot.plot(values_0x91.time,values_0x91.duty_cycle,'r.-', linewidth=0.5, label='motor_F-R(91h)_duty_cycle[%]')
plot.plot(values_0x92.time,values_0x92.duty_cycle,'g.-', linewidth=0.5, label='motor_F-L(92h)_duty_cycle[%]')
plot.plot(values_0x93.time,values_0x93.duty_cycle,'y.-', linewidth=0.5, label='motor_R-R(93h)_duty_cycle[%]')
plot.plot(values_0x94.time,values_0x94.duty_cycle,'k.-', linewidth=0.5, label='motor_R-L(94h)_duty_cycle[%]')
plot.plot(values_0x81.time,values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
plot.plot(values_0x82.time,values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
plot.title('voltage/duty_cycle', size=12, loc='left')
plot.xlabel('time[s]',size=10)
plot.ylabel('voltage[V] / duty_cycle [%]',size=10)
plot.legend(loc=1)   