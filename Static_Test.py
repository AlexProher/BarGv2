import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os

def squere(d):
    return(round(np.pi*d**2/4,2))
def strain(l0, l):
    return(round((l0-l)/l0, 3))

way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/Static/'
#materials = ['Denal920','DX2','SS316L-B','SS316L-R','SS316L-TZ']
materials = ['Denal920','DX2']
all_materials = {}

fig = go.Figure()
fig.update_layout(template = 'plotly_white', width=800, height=600, title= 'All tests')

for material in materials:
    print (f'material {material}')

    ## Считываем данные о геометрии образцов из файла в папке с материалом

    dimentions = pd.read_csv(way+material+'/'+material+'.txt', sep = '\t')
    dimentions['squere'] = dimentions.d0.apply(squere)
    dimentions['strain'] = [strain(dimentions.loc[ind]['l0'],dimentions.loc[ind]['l']) for ind in range(len(dimentions))]

    ## по количеству файлов с расширением '.lvm' определяем и составляем список названий файлов
    files = [item for item in os.listdir(way+material) if '.lvm' in item]

    fig1 = go.Figure()
    fig1.update_layout(template = 'plotly_white', width=800, height=600, title= material)
    all_materials = {}

    for item in range(len(dimentions)):
        file = files[item]
        data = pd.read_csv(way+material+'/'+file, sep = '\t', header= 21)
        data = data[data.Untitled < -100]
        results = pd.DataFrame({'time': data.X_Value,
                                'stress': abs(data.Untitled)/dimentions.loc[item]['squere']/1e-6/1e+6,      ## MPa
                                'strain': abs(data['Untitled 3']-max(data['Untitled 3']))/dimentions.loc[item]['l0']})
        all_materials.keys()
        fig1.add_trace(go.Scatter(x = results.strain, y = results.stress/1e+3, name = f'Specimen {item}'))
        fig.add_trace(go.Scatter(x = results.strain, y = results.stress/1e+3, name = f'{material} Sp_{item}'))
    fig1.update_xaxes(title = 'Strain')
    fig1.update_yaxes(title = 'Stress, GPa')
    fig1.write_html(way+material+'/'+material+'.html')

fig.update_xaxes(title = 'Strain')
fig.update_yaxes(title = 'Stress, GPa')
fig.write_html(way+'All_tests_2.html')
