import numpy as np
import pandas as pd

import os

from BarG.Analysis import CoreAnalyzer as CA




way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'

materials = os.listdir(way)
materials = [item for item in materials if ('result' not in item) and ('.' not in item)]



for material in materials:
    print (f'material {material}')
    all_raw = pd.DataFrame()
    way_to_material = way + material + '/'
    print(way_to_material)

    files = os.listdir(way_to_material)
    files = [item for item in files if item[0] != '.'] ## на случей если в папке есть служебные файлы начинающиеся с "."

    dim = [item for item in files if '.txt' in item][0]
    samples = [item for item in files if '.txt' not in item]

    #Загружаем геометрические параметры образцов 
    shapes = pd.read_csv(way_to_material + dim, sep = '\t')
    for sample in samples:
        
        print (f'specimen {sample}')
        way_to_item = way_to_material + sample + '/'


        files_on_item = os.listdir(way_to_item)
        files_on_item = [item for item in files_on_item if item[0] != '.'] ## на случей если в папке есть служебные файлы начинающиеся с "."

        parameters = [item for item in files_on_item if '.txt' in item][0]
        
        #Загружаем файл параметров для обработки экспериментов
        param = pd.read_csv(way_to_item + parameters,
                            header = None, sep='\t')
        ind = samples.index(sample)
        np_param = np.array([shapes.d[ind]*1e-3, 
                            shapes.l[ind]*1e-3, 
                            *param.iloc[:,1]])


        #Делаем анализ
        ca = CA.CoreAnalyzer(way_to_item, np_param)
        row_data = ca.load_signals(sample)
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
        
        way_to_result = way + "/" + 'results_' + material + "/" + sample + "/" 
        
        if not os.path.exists(way_to_result):
            os.makedirs(way_to_result)
        

        final_table.to_csv(way_to_result + 'result_data.txt', index = False, sep = '\t')
    