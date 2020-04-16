# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 17:45:18 2020

@author: xkadj
"""
import matplotlib.pyplot as plot

def plot_init(num):
    plot.figure(num=num, figsize=[20, 4], dpi=100, facecolor='w', edgecolor='r').set_facecolor('whitesmoke')    
    plot.minorticks_on()
    plot.tick_params(axis='both',which='major',length=10,width=1,labelsize=6)
    plot.style.use('seaborn-paper')
    plot.grid(True)   
#    plot.tight_layout()
    return plot

def plot_can_current(msg):  
    plot_init(1)
    plot.plot(msg.values_0x91.time, msg.values_0x91.current,'r.-', linewidth=0.5, label='motor_F-R(91h)_current[A]')
    plot.plot(msg.values_0x92.time, msg.values_0x92.current,'g.-', linewidth=0.5, label='motor_F-L(92h)_current[A]')
    plot.plot(msg.values_0x93.time, msg.values_0x93.current,'y.-', linewidth=0.5, label='motor_R-R(93h)_current[A]')
    plot.plot(msg.values_0x94.time, msg.values_0x94.current,'k.-', linewidth=0.5, label='motor_R-L(94h)_current[A]')
    plot.plot(msg.values_0x81.time, msg.values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
    plot.plot(msg.values_0x82.time, msg.values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
    plot.title('voltage/current', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('voltage[V] / current [A]',size=10)
    plot.legend(loc=1)
    plot.tight_layout()
 
def plot_can_erpm(msg):  
    plot_init(2)
    plot.plot(msg.values_0x91.time, msg.values_0x91.erpm,'r.-', linewidth=0.5, label='motor_F-R(91h)_erpm[-]')
    plot.plot(msg.values_0x92.time, msg.values_0x92.erpm,'g.-', linewidth=0.5, label='motor_F-L(92h)_erpm[-]')
    plot.plot(msg.values_0x93.time, msg.values_0x93.erpm,'y.-', linewidth=0.5, label='motor_R-R(93h)_erpm[-]')
    plot.plot(msg.values_0x94.time, msg.values_0x94.erpm,'k.-', linewidth=0.5, label='motor_R-L(94h)_erpm[-]')
    plot.plot(msg.values_0x81.time, msg.values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
    plot.plot(msg.values_0x82.time, msg.values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
    plot.title('voltage/erpm', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('voltage[V] / erpm [-]',size=10)
    plot.legend(loc=1)  
    plot.tight_layout()

def plot_can_duty_cycle(msg,fignum):  
    plot_init(fignum)
    plot.plot(msg.values_0x91.time, msg.values_0x91.duty_cycle,'r.-', linewidth=0.5, label='motor_F-R(91h)_duty_cycle[%]')
    plot.plot(msg.values_0x92.time, msg.values_0x92.duty_cycle,'g.-', linewidth=0.5, label='motor_F-L(92h)_duty_cycle[%]')
    plot.plot(msg.values_0x93.time, msg.values_0x93.duty_cycle,'m.-', linewidth=0.5, label='motor_M-R(93h)_duty_cycle[%]')
    plot.plot(msg.values_0x94.time, msg.values_0x94.duty_cycle,'c.-', linewidth=0.5, label='motor_M-L(94h)_duty_cycle[%]')
    plot.plot(msg.values_0x95.time, msg.values_0x95.duty_cycle,'y.-', linewidth=0.5, label='motor_R-R(95h)_duty_cycle[%]')
    plot.plot(msg.values_0x96.time, msg.values_0x96.duty_cycle,'k.-', linewidth=0.5, label='motor_R-L(96h)_duty_cycle[%]')
    plot.plot(msg.values_0x81.time, msg.values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
    plot.plot(msg.values_0x82.time, msg.values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
    plot.title('voltage/duty_cycle standard (junction_module)', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('voltage[V] / duty_cycle [%]',size=10)
    plot.legend(loc=1)   
    plot.tight_layout()
    
def plot_can_duty_cycle_vesc(msg,fignum):  
    plot_init(fignum)
    plot.plot(msg.values_0x901.time, msg.values_0x901.duty_cycle,'r.-', linewidth=0.5, label='motor_F-R(901h)_duty_cycle[%]')
    plot.plot(msg.values_0x902.time, msg.values_0x902.duty_cycle,'g.-', linewidth=0.5, label='motor_F-L(902h)_duty_cycle[%]')
    plot.plot(msg.values_0x903.time, msg.values_0x903.duty_cycle,'m.-', linewidth=0.5, label='motor_M-R(903h)_duty_cycle[%]')
    plot.plot(msg.values_0x904.time, msg.values_0x904.duty_cycle,'c.-', linewidth=0.5, label='motor_M-L(904h)_duty_cycle[%]')
    plot.plot(msg.values_0x905.time, msg.values_0x905.duty_cycle,'y.-', linewidth=0.5, label='motor_R-R(905h)_duty_cycle[%]')
    plot.plot(msg.values_0x906.time, msg.values_0x906.duty_cycle,'k.-', linewidth=0.5, label='motor_R-L(906h)_duty_cycle[%]')
    plot.plot(msg.values_0x81.time, msg.values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
    plot.plot(msg.values_0x82.time, msg.values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
    plot.title('voltage/duty_cycle - extended (vesc)', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('voltage[V] / duty_cycle [%]',size=10)
    plot.legend(loc=1)   
    plot.tight_layout()
    
def plot_can_tacho(msg,fignum):  
    plot_init(fignum)
    plot.plot(msg.values_0x83[1].time, msg.values_0x83[1].tacho,'r.-', linewidth=0.5, label='enc_F-R(83h-id1)_dist[cm]')
    plot.plot(msg.values_0x83[2].time, msg.values_0x83[2].tacho,'g.-', linewidth=0.5, label='enc_F-L(83h-id1)_dist[cm]')
    plot.plot(msg.values_0x83[3].time, msg.values_0x83[3].tacho,'m.-', linewidth=0.5, label='enc_M-R(83h-id2)_dist[cm]')
    plot.plot(msg.values_0x83[4].time, msg.values_0x83[4].tacho,'c.-', linewidth=0.5, label='enc_M-L(83h-id2)_dist[cm]')
    plot.plot(msg.values_0x83[5].time, msg.values_0x83[5].tacho,'y.-', linewidth=0.5, label='enc_R-R(83h-id3)_dist[cm]')
    plot.plot(msg.values_0x83[6].time, msg.values_0x83[6].tacho,'k.-', linewidth=0.5, label='enc_R-L(83h-id3)_dist[cm]')
    plot.plot(msg.values_0x81.time, msg.values_0x81.voltage,'b.-', linewidth=1, label='12V_voltage[V]') 
    plot.plot(msg.values_0x82.time, msg.values_0x82.voltage,'b.-', linewidth=1, label='42V_voltage[V]') 
    plot.title('encoder distance', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('distance [cm]',size=10)
    plot.legend(loc=1)   
    plot.tight_layout()
    
def plot_desired_speed(msg):    
    plot_init(4)
    plot.plot(msg.desired_speed.time, msg.desired_speed.desired_speed,'r.-', linewidth=0.5, label='desired_speed[m/s]')
    plot.plot(msg.desired_speed.time, msg.desired_speed.angular_speed,'g.-', linewidth=0.5, label='angular_speed[deg/s]')
    plot.title('desired_speed/angular_speed', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('desired_speed [m/s] / angular_speed[deg/s]',size=10)
    plot.legend(loc=1)
    plot.tight_layout()
    
def plot_downdrops(msg):
    plot_init(5)
    plot.plot(msg.downdrops_front.time, msg.downdrops_front.left,'r.-', linewidth=0.5, label='downdrops_front.left[-]')
    plot.plot(msg.downdrops_front.time, msg.downdrops_front.right,'g.-', linewidth=0.5, label='downdrops_front.right[-]')
    plot.plot(msg.downdrops_rear.time, msg.downdrops_rear.left,'y.-', linewidth=0.5, label='downdrops_rear.left[-]')
    plot.plot(msg.downdrops_rear.time, msg.downdrops_rear.right,'k.-', linewidth=0.5, label='downdrops_rear.right[-]')
    plot.title('downdrops', size=12, loc='left')
    plot.xlabel('time[s]',size=10)
    plot.ylabel('downdrops[-]',size=10)
    plot.legend(loc=1)
    plot.tight_layout()