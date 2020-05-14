# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 10:52:25 2019

@author: xkadj
"""
import argparse
import pandas as pd
import k_plot

class MessageParser:
    def __init__(self, log_file,robot):
        self.log_file = log_file
        self.robot = robot
        streams,can_messages = self.deserialize()

        #extended can:
        self.values_0x901 = self.get_vesc_status(can_messages, 0x901)
        self.values_0x902 = self.get_vesc_status(can_messages, 0x902)
        self.values_0x903 = self.get_vesc_status(can_messages, 0x903)
        self.values_0x904 = self.get_vesc_status(can_messages, 0x904)
        self.values_0x905 = self.get_vesc_status(can_messages, 0x905)
        self.values_0x906 = self.get_vesc_status(can_messages, 0x906)
        self.values_0x301 = self.get_vesc_ctrl(can_messages, 0x301)
        self.values_0x302 = self.get_vesc_ctrl(can_messages, 0x302)
        self.values_0x303 = self.get_vesc_ctrl(can_messages, 0x303)
        self.values_0x304 = self.get_vesc_ctrl(can_messages, 0x304)
        self.values_0x305 = self.get_vesc_ctrl(can_messages, 0x305)
        self.values_0x306 = self.get_vesc_ctrl(can_messages, 0x306)
        #standart can:
        self.values_0x91 = self.get_vesc_status(can_messages, 0x91)
        self.values_0x92 = self.get_vesc_status(can_messages, 0x92)
        self.values_0x93 = self.get_vesc_status(can_messages, 0x93)
        self.values_0x94 = self.get_vesc_status(can_messages, 0x94)
        self.values_0x95 = self.get_vesc_status(can_messages, 0x95)
        self.values_0x96 = self.get_vesc_status(can_messages, 0x96)
        self.values_0x31 = self.get_vesc_ctrl(can_messages, 0x31)
        self.values_0x32 = self.get_vesc_ctrl(can_messages, 0x32)
        self.values_0x33 = self.get_vesc_ctrl(can_messages, 0x33)
        self.values_0x34 = self.get_vesc_ctrl(can_messages, 0x34)
        self.values_0x35 = self.get_vesc_ctrl(can_messages, 0x35)
        self.values_0x36 = self.get_vesc_ctrl(can_messages, 0x36)

        self.values_0x83 = self.get_can_tacho(can_messages, 0x83)
        self.values_0x81 = self.get_can_voltage(can_messages, 0x81)
        self.values_0x82 = self.get_can_voltage(can_messages, 0x82)
        self.values_0x71 = self.get_can_downdrops(can_messages, 0x71)
        self.values_0x72 = self.get_can_downdrops(can_messages, 0x72)
        self.values_0x80 = self.get_can_angle(can_messages, 0x80)

    def deserialize(self):
        from osgar.logger import LogReader, lookup_stream_names, lookup_stream_id
        from osgar.lib.serialize import deserialize

        streams = lookup_stream_names(self.log_file)

        with LogReader(self.log_file, only_stream_id=lookup_stream_id(self.log_file,'can.can')) as log:
            log_list = []
            for timestamp, stream_id, data in log:
                sec = timestamp.total_seconds()
                stream_id = stream_id
                data = deserialize(data)
                log_list.append([stream_id,sec,data[0],data[1].hex(),len(data[1])])
        return streams,log_list

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

    def get_vesc_ctrl(self,messages, message_ID):
        values = []
        for row in range(len(messages)):
            if messages[row][2] == message_ID:
                erpm = int(messages[row][3].zfill(16),16)
                #if erpm > 2147483647: erpm = erpm - 4294967294
                values.append([messages[row][1], erpm])
        values = pd.DataFrame(values,columns=['time','erpm'])
        return values

    def get_can_voltage(self,messages, message_ID):
        values = []
        for row in range(len(messages)):
            if messages[row][2] == message_ID:
                voltage = int(messages[row][3],16)
                values.append([messages[row][1], voltage/1000])
        values = pd.DataFrame(values,columns=['time','voltage'])
        return values

    def get_can_tacho(self,messages, message_ID):
        if self.robot == 'K2':
            values, values_tacho_1 , values_tacho_2, values_tacho_3, values_tacho_4, values_tacho_5, values_tacho_6 = [],[],[],[],[],[],[]
            for row in range(len(messages)):
                if messages[row][2] == message_ID:
                    tacho_1 = int(messages[row][3].zfill(4)[0:4],16)
                    tacho_2 = int(messages[row][3].zfill(4)[4:8],16)
                    tacho_3 = int(messages[row][3].zfill(4)[8:12],16)
                    tacho_4 = int(messages[row][3].zfill(4)[12:16],16)
                    values_tacho_1.append([messages[row][1],0,0,tacho_1])
                    values_tacho_2.append([messages[row][1],0,0,tacho_2])
                    values_tacho_3.append([messages[row][1],0,0,tacho_3])
                    values_tacho_4.append([messages[row][1],0,0,tacho_4])
            values_tacho_1 = pd.DataFrame(values_tacho_1,columns=['time','counter','tacho_id','tacho'])
            values_tacho_2 = pd.DataFrame(values_tacho_2,columns=['time','counter','tacho_id','tacho'])
            values_tacho_3 = pd.DataFrame(values_tacho_3,columns=['time','counter','tacho_id','tacho'])
            values_tacho_4 = pd.DataFrame(values_tacho_4,columns=['time','counter','tacho_id','tacho'])
            values_tacho_5 = pd.DataFrame(columns=['time','counter','tacho_id','tacho'])
            values_tacho_6 = pd.DataFrame(columns=['time','counter','tacho_id','tacho'])
            return [values, values_tacho_1 , values_tacho_2, values_tacho_3, values_tacho_4, values_tacho_5, values_tacho_6]

        elif self.robot == 'K3':
            values, values_tacho_1 , values_tacho_2, values_tacho_3, values_tacho_4, values_tacho_5, values_tacho_6 = [],[],[],[],[],[],[]
            for row in range(len(messages)):
                if messages[row][2] == message_ID:
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

    def get_can_downdrops(self,messages,message_ID):
        values = []
        for row in range(len(messages)):
            if messages[row][2] == message_ID:
                left = int(messages[row][3].zfill(8)[0:4],16)
                right = int(messages[row][3].zfill(8)[4:8],16)
                values.append([messages[row][1], left, right])
        values = pd.DataFrame(values,columns=['time','left','right'])
        return values

    def get_can_angle(self,messages,message_ID):
        values = []
        if self.robot == 'K2':
            for row in range(len(messages)):
                if messages[row][2] == message_ID:
                    angle = int(messages[row][3].zfill(8)[0:8],16)
                    values.append([messages[row][1], angle])
            values = pd.DataFrame(values,columns=['time','angle'])
        if self.robot == 'K3':
            for row in range(len(messages)):
                if messages[row][2] == message_ID:
                    angle = int(messages[row][3].zfill(8)[0:4],16)
                    angle_2 = int(messages[row][3].zfill(8)[4:8],16)
                    values.append([messages[row][1], angle, angle_2])
            values = pd.DataFrame(values,columns=['time','angle','angle_2'])
        return values

    def get_desired_speed(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','desired_speed','angular_speed']).drop('0',axis=1)
        values.desired_speed = values.desired_speed / 1000
        values.angular_speed = values.angular_speed / 100
        return values

    def get_downdrops(self,messages):
        values = pd.DataFrame(messages,columns=['0','time','left','right']).drop('0',axis=1)
        return values

    def get_all_messages(pcan_messages):
        messages_list = []
        messages_all_df = pd.DataFrame(pcan_messages,columns=['stream','time','message_ID','message'])
        messages_IDs = messages_all_df.message_ID.drop_duplicates().tolist()
        messages_IDs.sort()
        for messages_ID in range(len(messages_IDs)):
            id_list = []
            for row in range(len(pcan_messages)):
                if pcan_messages[row][2] == messages_IDs[messages_ID]:
                    id_list.append(pcan_messages[row])
            meassages = pd.DataFrame(id_list,columns=['stream','time','id','content'])
            meassages = meassages[['id','stream','time','content']]
            messages_list.append(meassages)
        return messages_list, messages_IDs

def argParser():
    parser = argparse.ArgumentParser(description='   K-analyzer\nCopyright (c) 2020 CULS Prague, robotika.cz, s.r.o.\nprogrammed by: Jan Kaderabek')
    parser.add_argument("logname")
    parser.add_argument("robot")
    args = parser.parse_args()
    parser.print_help()
    return args

# =============================================================================
# MAIN
# =============================================================================
if __name__ == '__main__':

    # Get required arguments (logname robot)
    args = argParser()

    # Parse osgar log to dataframes
    can = MessageParser(args.logname,args.robot)

    # Plot seznozors in time
    fig_serie = 20  # From this nuber are plotting figs
    KPlot = k_plot.KPlotter(args.robot,fig_serie)
    KPlot.plot_can_ctrl_erpm(can)
    KPlot.plot_can_ctrl_erpm_vesc(can)
    KPlot.plot_can_current(can)
    KPlot.plot_can_duty_cycle(can)
    KPlot.plot_can_duty_cycle_vesc(can)
    KPlot.plot_can_tacho(can)
    KPlot.plot_can_downdrops(can)
    KPlot.plot_can_angle(can)

