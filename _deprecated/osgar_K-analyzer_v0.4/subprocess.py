# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 11:19:54 2019

@author: xkadj
"""
import osgar


osgar.logger = r"C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logs\kloubak2-subt-estop-lora-191213_162253.log"





#import subprocess
##cmd = 'C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar>python -m osgar.logger C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logy\kloubak2-subt-estop-lora-191213_143751.log --stream can.can --format "{stream_id};{sec};{data[0]};{data[1].hex()}" > tmp.csv'
#cmd = r'C:\Users\xkadj\Desktop\ROBOTIKA\osgar_191206\osgar>python -m osgar.logger C:\Users\xkadj\OneDrive\PROJEKTY\Projekt_ROBOTIKA\logy\kloubak2-subt-estop-lora-191213_143751.log --stream can.can --times'
#
#exec(open(cmd).read())
#
##subprocess.call(cmd, shell=True)
#
#subprocess.call(["python","K-analyzer.py"]) 
#
##
##p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
##out, err = p.communicate() 
###result = out.split('\n')
###for lin in result:
###    if not lin.startswith('#'):
###        print(lin)