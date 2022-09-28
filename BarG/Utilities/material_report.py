from turtle import title
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def print_report(material):
    fig1 = go.Figure()
    fig1.update_layout(template = 'none', width = 1000, height = 700, 
                        font=dict(size=20))
    fig1.update_xaxes(title = 'Strain', title_font = {"size": 20}, tickfont = {"size": 20})
    fig1.update_yaxes(title = 'Stress, [MPa]', title_font = {"size": 20}, tickfont = {"size": 20})


    
    fig2 = go.Figure()
    fig2.update_layout(template = 'none', 
                        font=dict(size=16),
                        title = f'Temperatures for {material.title},',
                        )
    fig2.update_xaxes(title = 'Time, [mks]')
    fig2.update_yaxes(title = 'Temperature rise, [C]')

    max_str = 0
    for item in material.get_specimens():
        trace_mech = go.Scatter(x = item.corr_strain, y = item.corr_stress, name = f'{item.title}')
        fig1.add_trace(trace_mech)
        ind = list(item.corr_stress).index(max(item.corr_stress))
        cur_max_str = item.corr_strain[ind]
        if cur_max_str > max_str:
            max_item = item

        
        if item.IR:
            trace_temperature = go.Scatter(x = item.raw_time_IR, y = item.raw_temperature, name = item.title)
            fig2.add_trace(trace_temperature)

    
    ind = list(max_item.corr_stress).index(max(max_item.corr_stress))
    #fig1.update_xaxes(range = [0,max_item.corr_strain[ind]+max(max_item.corr_strain)/5])
      
    return fig1, fig2


def generate_table(material):
    report = pd.DataFrame()
    for item in material.get_specimens():
        report = pd.concat([report, pd.DataFrame({'diameter [mm]': item.d*1000,
                                    'length [mm]': item.l*1000,
                                    'Ult.Stress [MPa]': round(max(item.true_stress)),
                                    'Strain for Ult.Stress': round(item.true_strain[item.true_stress.index(max(item.true_stress))],4),
                                    'Energy [kJ]': round(item.energy,2),
                                    'Strain Rate [1/s]': round(item.strain_rate,2)
                                    }, index=[item.title])], axis = 0)
    return report