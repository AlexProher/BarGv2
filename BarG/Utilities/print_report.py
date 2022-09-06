import plotly.graph_objects as go


def print_report(specimen):
    plots = [
                go.Scatter(name='Incident', y=specimen.raw_incid, x=specimen.raw_time,
                        mode='lines', visible=True),

                go.Scatter(name='Reflected', y=specimen.raw_transm, x=specimen.raw_time,
                        mode='lines', visible=True),
                
                go.Scatter(name='Incident', y=specimen.incid, x=specimen.time,
                        mode='lines', visible=False),
                go.Scatter(name='Reflected', y=specimen.reflect, x=specimen.time,
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
                                                    x=specimen.eng_strain, mode='lines', visible=False),

                go.Scatter(name='Stress_True', y=specimen.true_stress,
                                                x=specimen.true_strain, mode='lines', visible=False),

                go.Scatter(name='Stress_True', y=specimen.temperature,
                                                x=specimen.true_strain, mode='lines', visible=False)
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
                    args=[{'visible': [False]* 2 + [True] * 2 + [False] * 7},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Amplitude [V]'},
                            'showlegend': True}]),

                dict(label='Displacement',
                    method='update',
                    args=[{'visible': [False] * 4 + [True] + [False] * 6},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Displacement [m]'},
                            'showlegend': True}]),

                dict(label='Forces',
                    method='update',
                    args=[{'visible': [False] * 5 + [True] * 2 + [False] * 4},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Force [N]'},
                            'showlegend': True}]),

                dict(label='Velocities',
                    method='update',
                    args=[{'visible': [False] * 7 + [True] + [False] * 3},
                        {'xaxis': {'title': 'Time [μs]'},
                            'yaxis': {'title': 'Velocity [m/s]'},
                            'showlegend': True}]),

                dict(label='Stress - Strain',
                    method='update',
                    args=[{'visible': [False] * 8 + [True] * 2 + [False]},
                        {'xaxis': {'title': 'Strain'},
                            'yaxis': {'title': 'Stress [MPa]'},
                            'showlegend': True}]), 

                dict(label='Temperature',
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
                        margin=dict(l=100, r=200, t=100, b=100),
                        updatemenus=[dict(active=0, buttons=buttons, xanchor='left', x=0, y=1.2)]
                        )

    fig = go.Figure(data = plots, layout = layot)
    return fig