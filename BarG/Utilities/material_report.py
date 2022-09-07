from turtle import title
import plotly.graph_objects as go

def print_report(material):
    fig1 = go.Figure()
    fig1.update_layout(template = 'none', 
                        font=dict(size=16),
                        title = f'Stress-Strain curves for {material.title}')
    fig1.update_xaxes(title = 'Strain')
    fig1.update_yaxes(title = 'Stress, [MPa]')
    
    fig2 = go.Figure()
    fig2.update_layout(template = 'none', 
                        font=dict(size=16),
                        title = f'Temperatures for {material.title},',
                        )
    fig2.update_xaxes(title = 'Time, [mks]')
    fig2.update_yaxes(title = 'Temperature rise, [C]')


    for item in material.get_specimens():
        trace_mech = go.Scatter(x = item.true_strain, y = item.true_stress, name = item.title)
        fig1.add_trace(trace_mech)
        if item.IR:
            trace_temperature = go.Scatter(x = item.raw_time_IR, y = item.raw_temperature, name = item.title)
            fig2.add_trace(trace_temperature)
        
    return fig1, fig2