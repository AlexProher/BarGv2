import numpy as np
import pandas as pd

import os

from BarG.Analysis.CoreAnalyzer import CoreAnalyzer
from BarG.Analysis.CoreAnalyzer import Material, Experiment, Specimen
from BarG.Utilities import print_report
from BarG.Utilities import material_report as mr

""" 
Function make analysis of experiment which in the "way" folder
It is important thing that structure must be like the next:
in the way is nessesary to be folder "material" with all samples folder

in the folder way/material/ shuold be "material".txt which is table like:
name    l   d
Specimen1  length  diameter
...
SpecimenN  length  diameter

numbers of raws in this *.txt the same with folders "Specimen*" in the folder material
it is important that the name in "material".txt and name folder is the same because it 
is connection between dimentions and specimen

in the folder "way/material/Specimen*" should be data incid and reflected in *.WFT or *.FLT
and file parameters.txt which is:

Bar Diameter	0.0127	[m]
Young's Modulus	7.0e+10	[Pa]
First Gauge	0.66	[m]
Second Gauge	0.11	[m]
Sound Velocity	5050.0	[m/s]
Gauge Factor	2.12	[0]
Bridge Tension	10.6	[V]
Spacing	60	Points
Prominence	50.0	%
Curve Smoothing Parameter	7100	[0]
Average Strain Rate	1000.138897554203	[1/s]

and if IR records was during the experiment, folder "Specimen*_IR"
which contains *.hcc file
"""


def make_analysis(way):
    #way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'
    #way = '/Users/lubimyj/Git/experiments/RAF/'

    materials = os.listdir(way)
    #materials = ['12_06_22_1k']
    exp = Experiment([Material(item) for item in materials if ('result' not in item) and ('.' not in item)])



    for material in exp.materials:
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
            shapes = pd.read_csv(way_to_material + dim, sep = '\t', index_col='name')
        else:
            print('NO mechanical experiment to analyse')

        for specimen in material.get_specimens():

            if specimen.title in shapes.index.values:
                specimen.d = shapes.loc[specimen.title, 'd']*1e-3
                specimen.l = shapes.loc[specimen.title, 'l']*1e-3
                specimen.mech = True
            else:
                raise KeyError(f'No data about dimentions of {specimen.title}')
            
            
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
            specimen.reflect = ca.corr_refle.y
            specimen.u_in = ca.u_in
            specimen.u_out = ca.u_out
            specimen.eng_strain = ca.eng_stress_strain[0]
            specimen.eng_stress = ca.eng_stress_strain[1]
            specimen.F_in = ca.F_in
            specimen.F_out = ca.F_out

            specimen.true_strain = ca.true_stress_strain[0]
            specimen.true_stress = ca.true_stress_strain[1]

            specimen.raw_temperature = ca.raw_temperature
            specimen.raw_time_IR = ca.raw_time_IR

            specimen.temperature = ca.temperature
            specimen.time_IR = ca.time_IR

        


            #формируем итоговую таблицу
            final_table = pd.DataFrame({'time':  specimen.time,
                                        'incid': specimen.incid,
                                        'trans': specimen.trans,
                                        'refl': specimen.reflect,
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

            print_report.machanisc(specimen).write_html(way_to_result + 'report.html')

            if specimen.IR:
                print_report.temperature(specimen).write_html(way_to_result + 'report_temperature.html')

            
            ca.save_data()

            final_table.to_csv(way_to_result + 'result_data.txt', index = False, sep = '\t')
        
        
        material.reports = mr.print_report(material)
        material.reports[0].write_html(way + "/" + 'results_' + material.title + "/" + 'mech_report.html')

        if material.reports[1]._data_objs:
            material.reports[1].write_html(way + "/" + 'results_' + material.title + "/" + 'thermal_report.html')
        #print(material.get_list_specimens())
    return exp    