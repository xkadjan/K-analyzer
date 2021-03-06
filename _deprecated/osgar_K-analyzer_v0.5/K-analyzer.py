# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:52:25 2019

@author: xkadj
"""

import pandas as pd
import k_plot

#can_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200116\osgar\K3_can.csv"
#can_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200116\osgar\K3_can_2.csv"

#pcan_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200121\osgar\K3_pcan.csv"
pcan_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200121\osgar\K3_can_1.csv"

#desired_speed_file = r"C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar\tmp_desired_speed.csv"
#desired_speed_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200113\osgar\K3_des_speed_test_4.csv"
#downdrops_front_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200107\osgar\downdrops_front.csv"
#downdrops_rear_file = r"C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200107\osgar\downdrops_rear.csv"


#H   HELP:
#python -m osgar.logger C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\K3_200119\test-pcan-200119_104320.log --stream can.can --format "{stream_id};{sec};{data[0]};{data[1].hex()};" > K3_can_2.csv
 
class MessageParser:
    def __init__(self, can_messages):
#        #extended can:
        self.values_0x901 = self.get_vesc_status(can_messages, 0x901)
        self.values_0x902 = self.get_vesc_status(can_messages, 0x902)
        self.values_0x903 = self.get_vesc_status(can_messages, 0x903)
        self.values_0x904 = self.get_vesc_status(can_messages, 0x904)
        self.values_0x905 = self.get_vesc_status(can_messages, 0x905)
        self.values_0x906 = self.get_vesc_status(can_messages, 0x906)
        self.values_0x301 = self.get_vesc_status(can_messages, 0x301)
        self.values_0x302 = self.get_vesc_status(can_messages, 0x302)
        self.values_0x303 = self.get_vesc_status(can_messages, 0x303)
        self.values_0x304 = self.get_vesc_status(can_messages, 0x304)
        self.values_0x305 = self.get_vesc_status(can_messages, 0x305)
        self.values_0x306 = self.get_vesc_status(can_messages, 0x306)
        #standart can:
        self.values_0x91 = self.get_vesc_status(can_messages, 0x91)
        self.values_0x92 = self.get_vesc_status(can_messages, 0x92)
        self.values_0x93 = self.get_vesc_status(can_messages, 0x93)
        self.values_0x94 = self.get_vesc_status(can_messages, 0x94)
        self.values_0x95 = self.get_vesc_status(can_messages, 0x95)
        self.values_0x96 = self.get_vesc_status(can_messages, 0x96)
        self.values_0x31 = self.get_vesc_status(can_messages, 0x31)
        self.values_0x32 = self.get_vesc_status(can_messages, 0x32)
        self.values_0x33 = self.get_vesc_status(can_messages, 0x33)
        self.values_0x34 = self.get_vesc_status(can_messages, 0x34)
        self.values_0x35 = self.get_vesc_status(can_messages, 0x35)
        self.values_0x36 = self.get_vesc_status(can_messages, 0x36)
        
        self.values_0x81 = self.get_voltage(can_messages, 0x81)
        self.values_0x82 = self.get_voltage(can_messages, 0x82)
        self.values_0x83 = self.get_tacho(can_messages, 0x83)
#        self.desired_speed = self.get_desired_speed(desired_speed_messages)
#        self.downdrops_front = self.get_downdrops(downdrops_front_messages)
#        self.downdrops_rear = self.get_downdrops(downdrops_rear_messages)
        
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
                erpm = int(messages[row][3].zfill(16)[0:8],16)
                if erpm > 2147483647: erpm = erpm - 4294967294
                current = int(messages[row][3].zfill(16)[8:12],16)
                if current > 32767: current = current - 65534
                duty_cycle = int(messages[row][3].zfill(16)[12:16],16)
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
    
    def get_tacho(self,messages, message_ID):
        values, values_tacho_1 , values_tacho_2, values_tacho_3, values_tacho_4, values_tacho_5, values_tacho_6 = [],[],[],[],[],[],[]
        for row in range(len(messages)):
            if messages[row][2] == message_ID:
#                counter = (messages[row][3])
                counter = int(messages[row][3].zfill(12)[0:2],16)
                tacho_id = int(messages[row][3].zfill(12)[2:4],16)
                tacho_1 = int(messages[row][3].zfill(12)[4:8],16)
                if tacho_1 > 32767: tacho_1 = tacho_1 - 65534
                tacho_2 = int(messages[row][3].zfill(12)[8:12],16)
                if tacho_2 > 32767: tacho_2 = tacho_2 - 65534
                if tacho_id == 1:
                    values_tacho_1.append([messages[row][1], counter, tacho_id, tacho_1])
                    values_tacho_2.append([messages[row][1], counter, tacho_id, tacho_2])
                if tacho_id == 2:
                    values_tacho_3.append([messages[row][1], counter, tacho_id, tacho_1])
                    values_tacho_4.append([messages[row][1], counter, tacho_id, tacho_2])
                if tacho_id == 3:
                    values_tacho_5.append([messages[row][1], counter, tacho_id, tacho_1])
                    values_tacho_6.append([messages[row][1], counter, tacho_id, tacho_2])
                values.append([messages[row][1], counter, tacho_id, tacho_1, tacho_2])
        values = pd.DataFrame(values,columns=['time','counter','tacho_id','tacho_1','tacho_2'])
        values_tacho_1 = pd.DataFrame(values_tacho_1,columns=['time','counter','tacho_id','tacho'])
        values_tacho_2 = pd.DataFrame(values_tacho_2,columns=['time','counter','tacho_id','tacho'])
        values_tacho_3 = pd.DataFrame(values_tacho_3,columns=['time','counter','tacho_id','tacho'])
        values_tacho_4 = pd.DataFrame(values_tacho_4,columns=['time','counter','tacho_id','tacho'])
        values_tacho_5 = pd.DataFrame(values_tacho_5,columns=['time','counter','tacho_id','tacho'])
        values_tacho_6 = pd.DataFrame(values_tacho_6,columns=['time','counter','tacho_id','tacho'])
        return [values, values_tacho_1 , values_tacho_2, values_tacho_3, values_tacho_4, values_tacho_5, values_tacho_6]
    
    def get_desired_speed(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','desired_speed','angular_speed']).drop('0',axis=1)
        values.desired_speed = values.desired_speed / 1000
        values.angular_speed = values.angular_speed / 100
        return values
    
    def get_downdrops(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','left','right']).drop('0',axis=1)
        return values
    
# =============================================================================
# MAIN
# =============================================================================
        
#can_messages = pd.read_csv(can_file, sep=';', engine='python').values.tolist()

#desired_speed_messages = pd.read_csv(desired_speed_file, sep=';', engine='python').values.tolist()
#downdrops_front_messages = pd.read_csv(downdrops_front_file, sep=';', engine='python').values.tolist()
#downdrops_rear_messages = pd.read_csv(downdrops_rear_file, sep=';', engine='python').values.tolist()
#
#can_parsed = MessageParser(can_messages)

#desired_speed_parsed = MessageParser(desired_speed_messages)
#
#k_plot.plot_can_current(can_parsed)
#k_plot.plot_can_erpm(can_parsed)
#k_plot.plot_can_duty_cycle(can_parsed,6)
##k_plot.plot_can_current(can_parsed)
##k_plot.plot_can_erpm(can_parsed)

pcan_messages = pd.read_csv(pcan_file, sep=';', engine='python').values.tolist() #, nrows = 500
pcan_parsed = MessageParser(pcan_messages)
k_plot.plot_can_duty_cycle(pcan_parsed,16)
k_plot.plot_can_duty_cycle_vesc(pcan_parsed,17)
k_plot.plot_can_tacho(pcan_parsed,20)

#
#k_plot.plot_desired_speed(desired_speed_parsed)
#k_plot.plot_downdrops(downdrops_front_parsed)
#k_plot.plot_downdrops(downdrops_rear_parsed)

