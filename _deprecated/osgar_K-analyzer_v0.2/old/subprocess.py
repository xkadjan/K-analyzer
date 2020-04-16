# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:19:54 2019

@author: xkadj
"""

import subprocess
cmd = 'C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar>python -m osgar.logger C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logy\kloubak2-subt-estop-lora-191213_143751.log --stream can.can --format "{stream_id};{sec};{data[0]};{data[1].hex()}" > tmp.csv'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate() 
#result = out.split('\n')
#for lin in result:
#    if not lin.startswith('#'):
#        print(lin)