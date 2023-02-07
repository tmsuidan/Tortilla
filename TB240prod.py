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
local PC's hard drive at the start and moved to a network drive after processing."""


x=0
#start a counter on line 37 and start lists lines 40-50
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
    if not os.path.isfile('./images/best.jpg'):
        c1=0
        while c1==0:
            print("best.jpg is not saved to the images folder. Please save the image to the images folder and press enter when ready to proceed. \n best.jpg no se guarda en la carpeta de imágenes. Guarde la imagen en la carpeta de imágenes y presione Entrar cuando esté listo para continuar.")
            checkbest=input()
            if len(checkbest)==0:
                if not os.path.isfile('./images/best.jpg'): c1=0
                if os.path.isfile('./images/best.jpg'): c1=1
         
    if not os.path.isfile('./images/avg.jpg'):
        c2=0
        while c2==0:
            print("avg.jpg is not saved to the images folder. Please save the image to the images folder and press enter when ready to proceed. \n avg.jpg no se guarda en la carpeta de imágenes. Guarde la imagen en la carpeta de imágenes y presione Entrar cuando esté listo para continuar.")
            checkavg=input()
            if len(checkavg)==0:
                if not os.path.isfile('./images/avg.jpg'): c2=0
                if os.path.isfile('./images/avg.jpg'): c2=1
              
    if not os.path.isfile('./images/worst.jpg'):
        c3=0
        while c3==0:
            print("worst.jpg is not saved to the images folder. Please save the image to the images folder and press enter when ready to proceed. \n worst.jpg no se guarda en la carpeta de imágenes. Guarde la imagen en la carpeta de imágenes y presione Entrar cuando esté listo para continuar.")
            checkworst=input()
            if len(checkworst)==0:
                if not os.path.isfile('./images/worst.jpg'): c3=0
                if os.path.isfile('./images/worst.jpg'): c3=1
            
        
    samp_shift=input('Enter shift / Ingresar turno (A/B/C):')
    while len(samp_shift)==0:
        samp_shift=input('Invalid Entry \n Enter shift / Ingresar turno (A/B/C):')
    while samp_shift not in ["A","B","C","a","b","c"]:
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
    if len(samp_date_list)!=0 and samp_date!=samp_date_list[-1]:
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
        #checks if the date sample date is the same as previous with an exception for if it's the first sample. If not the same, starts new lists so that each csv only contains that sample's date
    samp_line=input("Enter line / Ingrese la linea (1, 2, or 6):")
    while len(samp_line)==0:
        samp_line=input("Enter line / Ingrese la linea (1, 2, or 6):")
    while samp_line not in ["1","2","6"]:
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
    while diam <=0.0 or diam>14.0:
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
        
        
        
        both_mask=trans_mask + 150*press_tf
        
        cv2.imwrite('./images/{}_{}_{}_{}_trans.jpg'.format(samp_date,  samp_line, samp_time,img_name), trans_mask)
        cv2.imwrite('./images/{}_{}_{}_{}_press.jpg'.format(samp_date,  samp_line, samp_time,img_name), press_mask)
        cv2.imwrite('./images/{}_{}_{}_{}_both.jpg'.format(samp_date,  samp_line, samp_time,img_name), both_mask)
        os.rename(img1_filename, './images/{}_{}_{}_{}_orig.jpg'.format(samp_date,  samp_line, samp_time,img_name))
        
        
        
        area_total=math.pi * (0.5*diam)**2
        percent_trans=num_trans/non_black
        percent_press=num_press / non_black
        
        area_trans=(percent_trans)*area_total
        area_press=(percent_press)*area_total
        
        if percent_trans>0.15:
            pf="Fail"
        else: pf="Pass"
        
        pf_list.append(pf)
        
        
        
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
        shutil.move('./csvs/{}_{}_data.csv'.format(samp_date, samp_shift), 'D:\Documents\LaChiquita\YumTB\Script\ProcData\{}_{}_data.csv'.format(samp_date.strip('/'), samp_shift))
        shutil.move('./images/{}_{}_{}_{}_orig.jpg'.format(samp_date, samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\YumTB\Script\ProcImages\{}_{}_{}_{}_{}_orig.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        shutil.move('./images/{}_{}_{}_{}_trans.jpg'.format(samp_date,  samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\YumTB\Script\ProcImages\{}_{}_{}_{}_{}_trans.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        shutil.move('./images/{}_{}_{}_{}_press.jpg'.format(samp_date,  samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\YumTB\Script\ProcImages\{}_{}_{}_{}_{}_trans.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        shutil.move('./images/{}_{}_{}_{}_both.jpg'.format(samp_date,  samp_line, samp_time,img_name), 'D:\Documents\LaChiquita\YumTB\Script\ProcImages\{}_{}_{}_{}_{}_both.jpg'.format(samp_date.strip('/'), samp_shift, samp_line, samp_time,img_name))
        
        
        
    
    
    y=input("Press 'Y' and enter to continue or 'N' and enter to end collection. \n Presione 'Y' e ingrese para continuar o 'N' e ingrese para finalizar el cobro del turno.")
    while y.upper()not in ['Y','N']:
        y=input("Inavlid Entry \nPress 'Y' and enter to continue or 'N' and enter to end collection for the shift. \n Presione 'Y' e ingrese para continuar o 'N' e ingrese para finalizar la recopilación..")
        
    
    if y.upper()=='Y': x=0
    elif y.upper()=='N': x=1
    






