# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 09:49:58 2022

@author: talam
"""

import math
import numpy as np
import pandas as pd


#import matplotlib.pyplot as plt
#could plot data if desired
import cv2
import shutil
import os

import datetime



directory="./images"
if not os.path.exists(directory):
    os.makedirs(directory)
path1=directory

directory2="./csvs"
if not os.path.exists(directory2):
    os.makedirs(directory2)
    
path2=directory2

"""Creats directories if they don't exist, but I intended for them to be on the 
local PC's hard drive at the start."""


x=0
#start a counter on line 37 and start lists lines 39-50
samp_shift_list=[]
samp_date_list=[]
samp_line_list=[]
samp_time_list=[]
rating_list=[]
t_perc_list=[]
op_perc=[]
t_area_list=[]
op_area=[]
pf_list=[]
diam_list=[]

#function to validate time entry 
def validate_time(d):
    try: 
        datetime.datetime.strptime(d, '%I%M%p')    
        return True
    except ValueError:
        return False

#function to validate date

def validate_date(d):
    try:
        datetime.datetime.strptime(d,'%m%d%y' )
        return True
    except ValueError:
        return False
#Below is the data that has to be entered by the technician. 
while(x==0):
    
    print("Please take a picture on the foam board of each tortilla. Name the best, 'best', the average, 'avg', and the worst, 'worst.'\n Por favor tome una foto en el tablero de espuma de cada tortilla. Nombra lo mejor, 'best', lo promedio, 'avg', y lo peor, 'worst'." )
    samp_shift=input('Enter shift / Ingresar turno (A/B/C):')
    while len(samp_shift)==0:
        samp_shift=input('Invalid Entry \n Enter shift / Ingresar turno (A/B/C):')
    if samp_shift not in ["A","B","C","a","b","c"]:
        samp_shift=input('Invalid Entry \n Enter shift / Ingresar turno (A/B/C):')
    samp_shift=samp_shift.upper()
    samp_date=input("Enter sample date  MMDDYY (If current date, press enter) / Ingrese la fecha de la muestra MMDDYY (Si es la fecha actual, presione enter):")
    if len(samp_date )==0:
        samp_date=datetime.date.today()
        samp_date=samp_date.strftime('%m%d%y')
    while validate_date(samp_date) is False:
        samp_date=input("Invalid Entry \nEnter sample date  MMDDYY (If current date, press enter) / Ingrese la fecha de la muestra MMDDYY (Si es la fecha actual, presione enter):")
        if len(samp_date )==0:
            samp_date=datetime.date.today()
            samp_date=samp_date.strftime('%m%d%y')
        
    samp_line=input("Enter line / Ingrese la linea (1, 2, or 6):")
    while len(samp_line)==0:
        samp_line=input("Enter line / Ingrese la linea (1, 2, or 6):")
    if samp_line not in ["1","2","6"]:
        samp_line=input("Invalid Entry \n Enter line / Ingrese la linea (1, 2, or 6):")
    samp_line='F'+samp_line
    
    samp_time=input("Enter sample time / Ingrese el tiempo de muestra (HHMMAM or PM):")
    while len(samp_time)==0 or validate_time(samp_time) is False:
        samp_time=input("Invalid Entry \nEnter sample time / Ingrese el tiempo de muestra (HHMMAM or PM):")
        
    samp_time=samp_time.upper().replace(':','').replace(' ','')
    diam=input("Enter size in inches / ingrese el tamaño en pulgadas:")
    while len(diam)==0:
        diam=input("Invalid Entry \n Enter size in inches / ingrese el tamaño en pulgadas:")
    diam=float(diam)
    if diam <=0.0 or diam>14.0:
        diam=float(input("Invalid Entry \n Enter size in inches / ingrese el tamaño en pulgadas:"))
    


    for img_name in ('best', 'worst', 'avg'):
        
        img1_filename="./images/"+img_name+'.jpg'
        img1 = cv2.imread(img1_filename)
        
        samp_shift_list.append(samp_shift)
        samp_date_list.append(samp_date)
        samp_line_list.append(samp_line)
        samp_time_list.append(samp_time)
        rating_list.append(img_name)
        diam_list.append(diam)
        
        
        
        NumPixels=img1.shape[0]*img1.shape[1]
        black_lower=np.array([0,0,0])
        black_up=np.array([80,80,100])
        black_mask=cv2.inRange(img1,black_lower,black_up)
        black_tf=black_mask/255.0
        num_black=np.sum(black_tf)
        non_black=NumPixels-num_black
        
        
        trans_lower=np.array([130,130,100])
        trans_upper=np.array([170,180,160])
        trans_mask=cv2.inRange(img1, trans_lower, trans_upper)
        trans_tf=trans_mask/255.0
        num_trans=np.sum(trans_tf)
        
        press_lower=np.array([130,130,100])
        press_upper=np.array([170,180,160])
        press_mask=cv2.inRange(img1, press_lower, press_upper)
        press_tf=trans_mask/255.0
        num_press=np.sum(press_tf)
        
        
        
        
        
        cv2.imwrite('./images/{}_{}_{}_{}_{}_trans.jpg'.format(samp_date, samp_shift, samp_line, samp_time,img_name), trans_mask)
        cv2.imwrite('./images/{}_{}_{}_{}_{}_trans.jpg'.format(samp_date, samp_shift, samp_line, samp_time,img_name), press_mask)
        os.rename(img1_filename, './images/{}_{}_{}_{}_{}_orig.jpg'.format(samp_date, samp_shift, samp_line, samp_time,img_name))
        
        
        
        area_total=math.pi * (0.5*diam)**2
        percent_trans=num_trans/non_black
        percent_press=num_press / non_black
        
        area_trans=(percent_trans)*area_total
        area_press=(percent_press)*area_total
        
        if percent_trans>0.15:
            pf="Fail"
        else: pf="Pass"
        
        pf_list.append(pf)
        
        # print("For the ", img_name, " sample at ",samp_time,", the percent translucense is ", "{:.2f}".format(percent_trans), "% and the area is ", "{:.2f}".format(area_trans), "square inches, and the result is ", pf,".")
        # print("Para ", img_name," muestras a las ",samp_time,", el porcentaje de translucidez es del ", "{:.2f}".format(percent_trans), "% y el area es de ", "{:.2f}".format(area_trans), " pulgadas cuadradas, y el resultado es ", pf,".")
        
        t_perc_list.append(percent_trans)
        t_area_list.append(area_trans)
        op_perc.append(percent_press)
        op_area.append(area_press)
        
        df=pd.DataFrame( {'Date': samp_date_list,'Shift':samp_shift_list,\
                          'Line':samp_line_list, 'Time': samp_time_list,\
                              'Size(in)':diam_list,\
                        'Best/ Worst/ Average': rating_list,\
                            'Percent Overpressed':op_perc, 'Area Overpressed':op_area,
                        'Percent Translucense':t_perc_list, 'Area Translucense (sq in)':t_area_list, 'Pass/Fail':pf_list})
        print(df.iloc[-1,])
            
        df.to_csv('./csvs/{}_{}_data.csv'.format(samp_date, samp_shift), index=False)
        shutil.move('./csvs/{}_{}_data.csv'.format(samp_date, samp_shift), 'D:\Documents\LaChiquita\ProcData\{}_{}_data.csv'.format(samp_date.strip('/'), samp_shift))
        shutil.move('./images/{}_{}_{}_{}_{}_orig.jpg'.format(samp_date, samp_shift, samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\ProcImages\{}_{}_{}_{}_{}_orig.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        shutil.move('./images/{}_{}_{}_{}_{}_trans.jpg'.format(samp_date, samp_shift, samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\ProcImages\{}_{}_{}_{}_{}_trans.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        
        
    
    
    x=input("Press enter to continue or any other letter key followed by enter to end collection for the shift. \n Presione enter para continuar o cualquier otra tecla de letra sequida de enter para finalizar la recopilacion del turno.")
    if len(x )==0: x=0






