from tkinter import font
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np


def machanisc(specimen):
    plots = [
                go.Scatter(name='Incident', y=specimen.raw_incid, x=specimen.raw_time,
                        mode='lines', visible=False),

                go.Scatter(name='Transmitted', y=specimen.raw_transm, x=specimen.raw_time,
                        mode='lines', visible=False),
                
                go.Scatter(name='Incident', y=specimen.incid, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='Reflected', y=specimen.reflect, x=specimen.time,
                        mode='lines', visible=False),
                
                go.Scatter(name='Transmitted', y=specimen.trans, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='U_in', y=specimen.u_in, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='F_in', y=specimen.F_in, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='F_out', y=specimen.F_out, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='V_in', y=specimen.u_out, x=specimen.time,
                        mode='lines', visible=False),

                go.Scatter(name='Stress_Engineering', y=specimen.eng_stress,
                                                    x=specimen.eng_strain, mode='lines', visible=True),

                go.Scatter(name='Stress_True', y=specimen.true_stress,
                                                x=specimen.true_strain, mode='lines', visible=True),
            ]
    buttons = [
                dict(label='Raw Signals',
                    method='update',
                    args=[{'visible': [True] * 2 + [False] * 9},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Amplitude [V]'},
                            'showlegend': True}]),

                dict(label='Corrected Signals',
                    method='update',
                    args=[{'visible': [False]* 2 + [True] * 3 + [False] * 6},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Amplitude [V]'},
                            'showlegend': True}]),

                dict(label='Displacement',
                    method='update',
                    args=[{'visible': [False] * 5 + [True] + [False] * 5},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Displacement [m]'},
                            'showlegend': True}]),

                dict(label='Forces',
                    method='update',
                    args=[{'visible': [False] * 6 + [True] * 2 + [False] * 3},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Force [N]'},
                            'showlegend': True}]),

                dict(label='Velocities',
                    method='update',
                    args=[{'visible': [False] * 8 + [True] + [False] * 2},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Velocity [m/s]'},
                            'showlegend': True}]),

                dict(label='Stress - Strain',
                    method='update',
                    args=[{'visible': [False] * 9 + [True] * 2},
                        {'xaxis': {'title': 'Strain'},
                            'yaxis': {'title': 'Stress [MPa]'},
                            'showlegend': True}]), 
                            ] 
    layot = go.Layout(title_x=0.5, template='none',
                    title = f'{specimen.material} {specimen.title}',
                        font=dict(size=16),
                        #legend=dict(yanchor='top', xanchor='right', y=1.2, x=1, font=dict(size=30)),
                        margin=dict(l=100, r=300, t=100, b=100),
                        updatemenus=[dict(active=0, buttons=buttons, xanchor='left', x=0, y=1.2)]
                        )

    fig = go.Figure(data = plots, layout = layot)

    fig.add_annotation(dict(font=dict(color='black', size=18),
                            
                            x=1.02,
                            y=0.55,
                            showarrow=False,
                            text="<b>Experiment Parameters:<b>",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.5,
                            showarrow=False,
                            text=f"Spec.diameter = {str(round(specimen.parameters[0]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.45,
                            showarrow=False,
                            text=f"Spec.length = {str(round(specimen.parameters[1]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.4,
                            showarrow=False,
                            text=f"Bar diameter = {str(round(specimen.parameters[2]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.35,
                            showarrow=False,
                            text=f"E = {str(specimen.parameters[3] / (10 ** 9))} [GPa]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.28,
                            showarrow=False,
                            text=f"Sound vel = {str(specimen.parameters[6])} [m/s]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.23,
                            showarrow=False,
                            text=f"V bridge = {str(specimen.parameters[8])} [V]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))
    

    fig.add_annotation(dict(font=dict(color='black', size=16),
                        
                            x=1.02,
                            y=0.8,
                            showarrow=False,
                            text=f"Ultimate stress = {str(round(max(specimen.true_stress)))} [MPa]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.75,
                            showarrow=False,
                            text=f"Strain for Ult.Stress = {str(round(specimen.corr_strain[list(specimen.corr_stress).index(max(specimen.corr_stress))],4))}",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=16),
                            
                            x=1.02,
                            y=0.7,
                            showarrow=False,
                            text=f"Strain rate = {str(round(specimen.strain_rate,2))} [1/s]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    
    return fig

def temperature(specimen):
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])

    fig1.update_layout(template = 'none', 
                        font=dict(size=16),
                        title = f'{specimen.material} {specimen.title}')

    fig1.add_trace(go.Scatter(x = specimen.true_strain, 
                                y = specimen.true_stress,
                                name = 'True Stress'),
                                secondary_y=False)
    fig1.add_trace(go.Scatter(x = specimen.true_strain, 
                                y = specimen.temperature, 
                                name = 'Temperature'),
                                secondary_y=True)

    fig1.update_xaxes(title_text="Strain")

    fig1.update_yaxes(title_text="Stress, [MPa]", secondary_y=False)
    fig1.update_yaxes(title_text="Temperature rise, C", secondary_y=True)
    return fig1


def make_appx(sp2):



    fig = make_subplots(rows = 2, cols = 2, column_widths=[0.7, 0.3])
    fig.update_layout(template = None, title = sp2.title)

    fig.add_trace(go.Scatter(x = sp2.raw_time * 1e6, y = sp2.raw_incid[:int(len(sp2.raw_incid)/2)]*1e3, name = 'Incident'), 1, 1)
    fig.add_trace(go.Scatter(x = sp2.raw_time * 1e6, y = sp2.raw_transm[:int(len(sp2.raw_transm)/2)]*1e3, name = 'Transmitted'), 1, 1)

    fig.update_xaxes(title_text="Time, us", row=1, col=1, title_font = {"size": 20}, tickfont = {"size": 20})
    fig.update_xaxes(title_text="Time, us", row=2, col=1, title_font = {"size": 20},tickfont = {"size": 20})

    fig.add_trace(go.Scatter(y = np.array(sp2.F_in)/1e3, x = np.array(sp2.time)* 1e6, name = 'F_in'), 2, 1)
    fig.add_trace(go.Scatter(y = np.array(sp2.F_out)/1e3, x = np.array(sp2.time)* 1e6, name = 'F_out'), 2, 1)

    fig.update_yaxes(title_text="Voltage, mV", row=1, col=1, title_font = {"size": 20}, tickfont = {"size": 20})
    fig.update_yaxes(title_text="Force, kN", row=2, col=1, title_font = {"size": 20}, tickfont = {"size": 20})

    posx = 0.7
    posy = 0.75
    fig.update_layout(legend=dict(
                                
                                yanchor="top",    
                                y=1.1,
                                xanchor="center",
                                x=0.8))

    fig.add_annotation(dict(font=dict(color='black', size=22),
                                
                            x=posx,
                            y=posy+0.05,
                            showarrow=False,
                            text="<b>Experiment Parameters:<b>",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                        
                            x=posx,
                            y=posy - 0.14,
                            showarrow=False,
                            text=f"Ultimate stress = {str(round(max(sp2.true_stress)))} [MPa]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.22,
                            showarrow=False,
                            text=f"Strain for Ult.Stress = {str(round(sp2.true_strain[sp2.true_stress.index(max(sp2.true_stress))],4))}",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.3,
                            showarrow=False,
                            text=f"Strain rate = {str(round(sp2.strain_rate,2))} [1/s]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))


    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.38,
                            showarrow=False,
                            text=f"Spec.diameter = {str(round(sp2.parameters[0]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.5,
                            showarrow=False,
                            text=f"Spec.length = {str(round(sp2.parameters[1]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.58,
                            showarrow=False,
                            text=f"Bar diameter = {str(round(sp2.parameters[2]*1e6) * 1000 / 1e6)} [mm]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.65,
                            showarrow=False,
                            text=f"Bar Young's mod. = {str(sp2.parameters[3] / (10 ** 9))} [GPa]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))

    fig.add_annotation(dict(font=dict(color='black', size=20),
                            
                            x=posx,
                            y=posy - 0.03,
                            showarrow=False,
                            text=f"Sound vel = {str(sp2.parameters[6])} [m/s]",
                            textangle=0,
                            xanchor='left',
                            xref="paper",
                            yref="paper"))



    fig.update_layout(width = 1000, height = 700, font = dict(size = 20))

    return fig




