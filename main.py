import numpy as np
import pandas as pd



import os
import sys
from BarG.Analysis import CoreAnalyzer as CA

def sep_meas(words):
    signs = '1234567890.'
    res = ''
    for item in words:
        if item in signs:
            res+=item
    return float(res)
    
def read_signal(way):
    file = open(way)
    file.readlines(13)
    res = pd.read_csv(file, header = None, sep = '\t', names = ['vol', 'sec'])
    file.close()
    return res


way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'
materials = ['Denal920','DX2']
specimen = ['1/','2/','3/','4/','5/','6/']
subFold = '/IRCamera/Specimen'
testFold = 'test/EXP #1/'
dataFold = '/FLT/'
files = ['Parameters.txt','incid.FLT','trans.FLT']
#sr = 2e+9
for material in materials:
    print (f'material {material}')
    for item in range(len(specimen)):
        print (f'specimen number {specimen[item][0]}')
        
        #Загружаем геометрические параметры образцов 
        shapes = pd.read_csv(way+material+'.txt', sep = '\t')

        #Конфигурируем файл параметров для обработки экспериментов
        param = pd.read_csv(way + material + subFold + specimen[item] + testFold + files[0],
                            header = None, names = ['title', 'value'], sep=':')

        param['value'] = param['value'].apply(sep_meas)
        param.iloc[0,1] = float(shapes.d[item])*1e-3
        param.iloc[1,1] = float(shapes.l[item])*1e-3
        param.iloc[3,1] = param.value[3]*100000000 #1.9e+11
        np_param = np.array(param.value)

        path = way + material + subFold + specimen[item] + testFold + dataFold

        #Загружаем сигналы эксперимента
        signal1 = read_signal(path +files[1])
        signal2 = read_signal(path +files[2])


        #Определяем кто из них какой
        if max(signal1.vol) > max(signal2.vol):
            incid = signal1.vol-signal1.vol[0]
            transm = signal2.vol-signal2.vol[0]
        else:
            incid = signal2.vol-signal2.vol[0]
            transm = signal1.vol-signal1.vol[0]
        time = signal1.sec

        data = pd.DataFrame({'time': time,
                            'incid': incid,
                            'trans': transm})

        #Делаем анализ
        ca = CA.CoreAnalyzer(path, np_param)
        ca.load_experiments(np.array(incid), np.array(transm), np.array(time))
        ca.analyze()

        #формируем итоговую таблицу
        final_table = pd.DataFrame({'time': ca.time,
                                    'incid': ca.corr_incid.y,
                                    'trans': ca.corr_trans.y,
                                    'refl': ca.corr_refle.y,
                                    'U_in': ca.u_in,
                                    'U_out': ca.u_out,
                                    'eng_strain': ca.eng_stress_strain[0],
                                    'eng_stress': ca.eng_stress_strain[1],
                                    'true_strain': ca.true_stress_strain[0],
                                    'true_stress': ca.true_stress_strain[1],
                                    'F_in': ca.F_in,
                                    'F_out': ca.F_out })
        way_to_file = way + material + subFold + specimen[item]

        final_table.to_csv(way_to_file + 'result_data.txt', index = False, sep = '\t')
                            