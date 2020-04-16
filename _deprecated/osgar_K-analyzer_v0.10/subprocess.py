# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:19:54 2019

@author: xkadj
"""
from osgar.logger import LogReader, lookup_stream_names
from osgar.lib.serialize import deserialize
import pandas as pd
#import struct

log_file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\kloubak2-subt-estop-lora-191213_162253.log"
#log_file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\K2_200217\test-pcan-200218_004148.log"
#log_file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\K2_200128\test-pcan-200128_185745.log"
#log_file = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\K2_200204\test-pcan-200204_142841.log"

streams = lookup_stream_names(log_file)
for list_id in range(len(streams)):
    if 'can.can' == streams[list_id]: break

with LogReader(log_file,only_stream_id=20) as log:
    log_list = []
    for timestamp, stream_id, data in log:
        sec = timestamp.total_seconds()
        stream_id = stream_id
#        msg_id = data[2] #hex(data[2])
#        msg_len = len(data[-9:-1])
#        msg_content = struct.unpack(str(msg_len)+'B', data[-9:-1])
#        log_list.append([sec,stream_id,msg_id,msg_len,msg_content,str(data)])
        data_des = deserialize(data)
#        msg_id = data[2] #hex(data[2])
#        msg_len = len(data[-9:-1])
#        msg_content = struct.unpack(str(msg_len)+'B', data[-9:-1])
        log_list.append([stream_id,sec,data_des[0],data_des[1].hex(),len(data_des[1])])        
        deserialize(data)
        
#    log = pd.DataFrame(log_list)


#0:00:06.076378 19 [0, 654]
#0:00:06.634475 19 [0, 656]
#0:00:07.176152 19 [0, 654]
#
#0:00:07.575947 20 [36, b'\x00\x00\xfa\x00', 0]
#0:00:07.586776 20 [146, b'\x00\x00\x00\x00\x00\x00\x00\x00', 0]
#0:00:07.587167 20 [145, b'\x00\x00\x00\x00\xff\xf7\x00\x00', 0]
#
#0:00:07.571883 21 b'\x02D\x00\x00\x00\x00'
#0:00:07.572395 21 b'\x02d\x00\x00\x00\x00'
#0:00:07.572976 21 b'\x02\x84\x00\x00\x00\x00'
        
#00000000fff70000

test = pd.read_csv(r'C:\Users\xkadj\OneDrive\Plocha\ROBOTIKA\osgar_200121\osgar\test.csv', sep=';', engine='python').values.tolist()