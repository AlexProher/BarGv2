import numpy as np
import pandas as pd

import os

from BarG.Analysis.CoreAnalyzer import CoreAnalyzer
from BarG.Analysis.CoreAnalyzer import Material, Experiment, Specimen




way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'

materials = os.listdir(way)
exp = Experiment([Material(item) for item in materials if ('result' not in item) and ('.' not in item)])



for material in exp.materaials:
    print (f'material {material.title}')
    all_raw = pd.DataFrame()
    way_to_material = way + material.title + '/'
    print(way_to_material)

    files = os.listdir(way_to_material)
    files = [item for item in files if item[0] != '.'] ## на случей если в папке есть служебные файлы начинающиеся с "."

    dim = [item for item in files if '.txt' in item][0]
    
    material.add_specimen([Specimen(item) for item in files if '.txt' not in item])

    #Загружаем геометрические параметры образцов 
    if dim:
        shapes = pd.read_csv(way_to_material + dim, sep = '\t')
    else:
        print('NO mechanical experiment to analyse')

    for specimen in material.get_specimens():

        if shapes.d[specimen.index] and shapes.l[specimen.index]:
            specimen.d = shapes.d[specimen.index]*1e-3
            specimen.l = shapes.l[specimen.index]*1e-3
            specimen.mech = True
        
        
        print (f'specimen {specimen.title}')
        way_to_item = way_to_material + specimen.title + '/'


        files_on_item = os.listdir(way_to_item)
        files_on_item = [item for item in files_on_item if item[0] != '.'] ## на случей если в папке есть служебные файлы начинающиеся с "."

        for item in files_on_item:
            if 'Parameters.txt' in item:
                parameters = item
                                #Загружаем файл параметров для обработки экспериментов
                param = pd.read_csv(way_to_item + parameters,
                                    header = None, sep='\t')
                

                np_param = np.array([specimen.d, 
                                    specimen.l, 
                                    *param.iloc[:,1]])

            #Need to think about it                        
            #else:
            #    specimen.mech = False
            #    np_param = np.zeros((13,1))

            if '_IR' in item:
                specimen.IR = True

        #Делаем анализ
        ca = CoreAnalyzer(way_to_item, np_param, specimen)
        ca.begin_analyse(specimen.title)

        specimen.time = ca.time
        specimen.incid = ca.corr_incid.y
        specimen.trans = ca.corr_trans.y
        specimen.refle = ca.corr_refle.y
        specimen.u_in = ca.u_in
        specimen.u_out = ca.u_out
        specimen.eng_strain = ca.eng_stress_strain[0]
        specimen.eng_stress = ca.eng_stress_strain[1]
        specimen.F_in = ca.F_in
        specimen.F_out = ca.F_out

        specimen.true_strain = ca.true_stress_strain[0]
        specimen.true_stress = ca.true_stress_strain[1]

        specimen.temperature = ca.temperature
        specimen.time_IR = ca.time_IR
    


        #формируем итоговую таблицу
        final_table = pd.DataFrame({'time':  specimen.time,
                                    'incid': specimen.incid,
                                    'trans': specimen.trans,
                                    'refl': specimen.refle,
                                    'U_in': specimen.u_in,
                                    'U_out': specimen.u_out,
                                    'eng_strain': specimen.eng_strain,
                                    'eng_stress': specimen.eng_stress,
                                    'true_strain': specimen.true_strain,
                                    'true_stress': specimen.true_stress,
                                    'F_in': specimen.F_in,
                                    'F_out': specimen.F_out,
                                    'Temperature': specimen.temperature
                                    })
        
        way_to_result = way + "/" + 'results_' + material.title + "/" + specimen.title + "/" 
        
        if not os.path.exists(way_to_result):
            os.makedirs(way_to_result)

        ca.result_path = way_to_result
        ca.save_data()

        final_table.to_csv(way_to_result + 'result_data.txt', index = False, sep = '\t')
    
    #print(material.get_list_specimens())
    