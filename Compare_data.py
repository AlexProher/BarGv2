import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy import interpolate
#import biosig as bs
import os

def open_files(path):
    files = [file for file in os.listdir(path) if file[-4:] in ('.WFT', '.wft')]
    signals = pd.DataFrame({'time': [],
                        'incid':[],
                        'reflect':[]})

    for file in files:
        HDR=bs.header(path+file)
        sr = float(HDR.split('\n')[9][HDR.split('\n')[9].find(':')+2:-1])
        data=bs.data(path+file)


        res = []
        for item in data:
            res.append(item[0])
        if signals.incid.sum() == 0:
            signals.incid = res
        elif signals.incid.min() < min(res):
            signals.reflect = res
        else:
            signals.reflect = signals.incid
            signals.incid = res
    signals.time = np.arange(len(data))/sr

    return signals

def my_interpolation(data, len_aim):
    xnew = np.arange(0,len(data)-1,(len(data)-1)/len_aim)
    xnew[-1] = round(xnew[-1])
    x = np.arange(len(data))
    y = np.array(data)
    f = interpolate.interp1d(x, y)
    ynew = f(xnew)
    return (ynew)

def cut_signal(signal1, signal2, time1, time2):
    p1, p2 = find_slope(signal1, signal2)
    #param = 7800/780000 # волшебный параметр связаный с частотой дискретизации
    res_time = (time2[p2-3:]-time2[p2])+time1[p1]

    time_last = list(abs(res_time-list(time1)[-1]))
    time_last = time_last.index(min(time_last)) 
    res_time = list(res_time[:time_last])

    cut_sign2 = signal2[p2-3:time_last+p2-3]
    res = [item if item>0 else 0 for item in res_time]
    
    return (my_interpolation(cut_sign2, len(signal1)),
            my_interpolation(res, len(signal1)))

def find_slope(sign1, sign2):
    tr1 = sign1.max()*0.1
    tr2 = sign2.max()*0.05
    bin_sig1 = [1 if x>tr1 else 0 for x in sign1]
    bin_sig2 = [1 if x>tr2 else 0 for x in sign2]
    return (bin_sig1.index(1), bin_sig2.index(1))

way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'
materials = ['Denal920','DX2']
specimens = ['1','2','3','4','5','6']
to_IR_data = '/Specimen'
to_raw_data = '/test/Original WFT Files/'
IR_index = '_IR/'
subFold = '/IRCamera/Specimen'
testFold = 'test/EXP #1/'
dataFold = '/FLT/'

for material in materials:
    print (f'material {material}')
    fig0 = go.Figure()
    fig0.update_layout(template = 'plotly_white', width=800, height=600,
                        title = f'Strain vs Max Temperature, {material}')
    fig0.update_xaxes(title_text="Strain")
    fig0.update_yaxes(title_text="delta Temperature, C")


    for specimen in specimens:
    

        mech_data_path = way + material + subFold + specimen + '/'
        raw_data_path = way + material + subFold + specimen + to_raw_data
        thermo_data_path = way + material + subFold + specimen + to_IR_data + specimen + IR_index

        mech_data = pd.read_csv(mech_data_path+'result_data.txt', sep='\t')
        thermo_data = pd.read_csv(thermo_data_path +'Temperature_Spec_'+specimen+'.csv', sep = '\t' )
        raw_data = open_files(raw_data_path)
        print(thermo_data_path)
        

        fig1 = make_subplots(specs=[[{"secondary_y": True}]])
        fig1.update_layout(template = 'plotly_white', width=800, height=600,
                        title = f'Comparison IncidentWave vs Max Temperature, {material} specimen {specimen}')

        fig1.add_trace(go.Scatter(x = thermo_data.time-108e-6, 
                                    y = thermo_data['Point'], 
                                    name = 'Temperature'),
                                    secondary_y=True)
        fig1.add_trace(go.Scatter(x = raw_data.time, 
                                    y = raw_data.incid, 
                                    name = 'Incident Signal'))

        fig1.update_xaxes(title_text="Time, s")

        fig1.update_yaxes(title_text="Voltage, V", secondary_y=False)
        fig1.update_yaxes(title_text="Temperature rise, C", secondary_y=True, range=[-thermo_data['Point'].max()-10,thermo_data['Point'].max()+10])


        func_sign, func_time = cut_signal(mech_data.true_strain, thermo_data['Point'], mech_data.time, thermo_data.time)

        fig2 = make_subplots(specs=[[{"secondary_y": True}]])
        fig2.update_layout(template = 'plotly_white', width=800, height=600,
                        title = f'True Strain vs Mean Temperature, {material} specimen {specimen}')
        fig2.add_trace(go.Scatter(x = mech_data.true_strain, 
                                    y = mech_data.true_stress,
                                    name = 'True Stress'),
                                    secondary_y=False)
        fig2.add_trace(go.Scatter(x = mech_data.true_strain, 
                                    y = func_sign, 
                                    name = 'Temperature  rise, C'),
                                    secondary_y=True)
        

        fig2.update_xaxes(title_text="Strain")

        fig2.update_yaxes(title_text="Stress, MPa", secondary_y=False)
        fig2.update_yaxes(title_text="Temperature, C", secondary_y=True)

        fig1.write_html(thermo_data_path + f'Specimen{specimen}_SignalTemperature_max.html')
        fig2.write_html(thermo_data_path + f'Specimen{specimen}_StressTemperature_max.html')

        fig3 = go.Figure()
        fig3.update_layout(template = 'plotly_white', width=800, height=600,
                        title = f'Strain vs MaxTemperature, {material}')
        fig3.update_xaxes(title_text="Strain")
        fig3.update_yaxes(title_text="Betha int")
        fig3.add_trace(go.Scatter(x = mech_data.true_strain, 
                                    y = func_sign/mech_data.true_stress, 
                                    name = f'specimen_{specimen}'))

        fig0.add_trace(go.Scatter(x = mech_data.true_strain, 
                                    y = func_sign, 
                                    name = f'specimen_{specimen}'))
        fig0.write_html(way + material +'_T-Q_max.html')
        #fig3.write_html(way + material +'_betha_mean.html')

