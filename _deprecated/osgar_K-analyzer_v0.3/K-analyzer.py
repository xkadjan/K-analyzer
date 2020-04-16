# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:52:25 2019

@author: xkadj
"""

import pandas as pd
import k_plot

can_file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\tmp.csv"
desired_speed_file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\tmp_desired_speed.csv"
downdrops_front_file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\downdrops_front.csv"
downdrops_rear_file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\downdrops_rear.csv"
 
class MessageParser:
    def __init__(self, can_messages):
        self.values_0x91 = self.get_vesc_status(can_messages, 0x91)
        self.values_0x92 = self.get_vesc_status(can_messages, 0x92)
        self.values_0x93 = self.get_vesc_status(can_messages, 0x93)
        self.values_0x94 = self.get_vesc_status(can_messages, 0x94)
        self.values_0x81 = self.get_voltage(can_messages, 0x81)
        self.values_0x82 = self.get_voltage(can_messages, 0x82)
        self.desired_speed = self.get_desired_speed(desired_speed_messages)
        self.downdrops_front = self.get_downdrops(downdrops_front_messages)
        self.downdrops_rear = self.get_downdrops(downdrops_rear_messages)
        
    def get_vesc_status(self,messages, message_ID):
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
    
    def get_voltage(self,messages, message_ID):
        values = []
        for row in range(len(messages)):
            if messages[row][2] == message_ID:
                voltage = int(messages[row][3],16)
                values.append([messages[row][1], voltage/1000])
        values = pd.DataFrame(values,columns=['time','voltage'])
        return values
    
    def get_desired_speed(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','left','right']).drop('0',axis=1)
        return values
    
    def get_downdrops(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','left','right']).drop('0',axis=1)
        return values
    
# =============================================================================
# MAIN
# =============================================================================
can_messages = pd.read_csv(can_file, sep=';', engine='python').values.tolist()
desired_speed_messages = pd.read_csv(desired_speed_file, sep=';', engine='python').values.tolist()
downdrops_front_messages = pd.read_csv(downdrops_front_file, sep=';', engine='python').values.tolist()
downdrops_rear_messages = pd.read_csv(downdrops_rear_file, sep=';', engine='python').values.tolist()

msg = MessageParser(can_messages)

k_plot.plot_can_current(msg)
k_plot.plot_can_erpm(msg)
k_plot.plot_can_duty_cycle(msg)
k_plot.plot_desired_speed(msg)
k_plot.plot_downdrops(msg)

