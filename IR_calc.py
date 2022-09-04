from TelopsToolbox.hcc.readIRCam import read_ircam
import TelopsToolbox.utils.image_processing as ip
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import numpy as np

way = '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/'
materials = ['Denal920','DX2']
specimens = ['1','2','3','4','5','6']
subFold = '/IRCamera/Specimen'
to_IR_data = '/Specimen'
IR_index = '_IR/'


#Raw IR movie

for material in materials:
    for specimen in specimens:
        print (f'Material {material}, specimen {specimen}')

#material = materials[0]
#specimen = specimens[0]

        path = way+material+subFold+specimen+to_IR_data+specimen+IR_index
        path == '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/Denal920/IRCamera/Specimen1/Specimen1_IR/'
        file = to_IR_data[1:]+specimen+IR_index[:-1]+'.hcc'
        
        data, header, specialPixel, nonSpecialPixel = read_ircam(path+file)
                                                        

        header_df = pd.DataFrame(header)
        
        frame = data[0]

        numero_header = 0
        this_header = header_df.iloc[numero_header]
        frame_rate = this_header[20]

        fig_dict = {
                    "data": [],
                    "layout": { 'yaxis': dict(domain=[0.25, 1]),
                                'yaxis2': dict(domain=[0, 0.15]),
                                'title': 'Matetial: ' + material + ' specimen №' + specimen
                                },
                    "frames": []
                    }


        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                        "fromcurrent": True, "transition": {"duration": 1,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
            ]

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        #make data for rirst snap
        image_2D = ip.form_image(this_header, data[0])[0]-273.15
        first_frame = image_2D   
        frame_zero = go.Heatmap(z = image_2D)
        frame_one = go.Scatter(y = np.array(image_2D).max(axis=0), xaxis = 'x2', yaxis ='y2')

        fig_dict['data'].append(frame_zero)
        fig_dict['data'].append(frame_one)


        # make other frames
        for pic in range(len(data)):

            image_2D = ip.form_image(this_header, data[pic])[0]-273.15
            vertical_temp = np.array(image_2D).max(axis=0)

            trace2 = go.Scatter(y = vertical_temp, xaxis = 'x2', yaxis ='y2',)
            trace1 = go.Heatmap(z = image_2D, yaxis="y1")

            frame_n = {"data": [trace1, trace2], "name": str(pic)}

            slider_step = {"args": [[pic],
                                    {"data": {"duration": 300, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 300}}
                                    ],
                            "label": f'{round(pic/frame_rate*1e+6,3)} mks',
                            "method": "animate"}
                            
            fig_dict['layout']['yaxis2']['range'] = [0,max(vertical_temp)+10]
            fig_dict["frames"].append(frame_n)   
            sliders_dict["steps"].append(slider_step)

        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)

        #fig.show()
        #fig.write_html(path+file[:-3]+'html')

#Masked IR movie

def bin_image(image, tresh = 5):
    image = [list(map(lambda x: 1 if (x > tresh) else 0, line)) for line in image]
    return image


for material in materials:
    for specimen in specimens:
        print (f'Masking Material {material}, specimen {specimen}')

        path = way+material+subFold+specimen+to_IR_data+specimen+IR_index
        path == '/Users/lubimyj/Git/experiments/Plansee-Tungstan-W/Denal920/IRCamera/Specimen1/Specimen1_IR/'
        file = to_IR_data[1:]+specimen+IR_index[:-1]+'.hcc'
        
        data, header, specialPixel, nonSpecialPixel = read_ircam(path+file)
                                                        

        header_df = pd.DataFrame(header)
        frame = data[0]

        numero_header = 0
        this_header = header_df.iloc[numero_header]

        fig_dict = {
                    "data": [],
                    "layout": { 'yaxis': dict(domain=[0.25, 1]),
                                'yaxis2': dict(domain=[0, 0.15]),
                                'title': 'Matetial: ' + material + ' specimen №' + specimen
                                },
                    "frames": []
                    }


        fig_dict["layout"]["hovermode"] = "closest"
        fig_dict["layout"]["updatemenus"] = [
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True},
                                        "fromcurrent": True, "transition": {"duration": 1,
                                                                            "easing": "quadratic-in-out"}}],
                        "label": "Play",
                        "method": "animate"
                    },
                    {
                        "args": [[None], {"frame": {"duration": 0, "redraw": True},
                                        "mode": "immediate",
                                        "transition": {"duration": 0}}],
                        "label": "Pause",
                        "method": "animate"
                    }
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.1,
                "xanchor": "right",
                "y": 0,
                "yanchor": "top"
            }
            ]

        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 20},
                "prefix": "",
                "visible": True,
                "xanchor": "right"
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": []
        }

        #make data for rirst snap
        image_2D = ip.form_image(this_header, data[0])[0]-273.15
        first_frame = image_2D   
        frame_zero = go.Heatmap(z = image_2D)
        frame_one = go.Scatter(y = np.array(image_2D).max(axis=0), xaxis = 'x2', yaxis ='y2')

        fig_dict['data'].append(frame_zero)
        fig_dict['data'].append(frame_one)


        # make other frames
        for pic in range(len(data)):

            image_2D = ip.form_image(this_header, data[pic])[0]-273.15

            final_image = (image_2D-first_frame)*bin_image(image_2D, image_2D.max()*0.8)

            vertical_temp = np.array(final_image).max(axis=0)

            trace2 = go.Scatter(y = vertical_temp, xaxis = 'x2', yaxis ='y2',)
            trace1 = go.Heatmap(z = final_image, yaxis="y1")

            frame_n = {"data": [trace1, trace2], "name": str(pic)}

            slider_step = {"args": [[pic],
                                    {"data": {"duration": 300, "redraw": True},
                                    "mode": "immediate",
                                    "transition": {"duration": 300}}
                                    ],
                            "label": f'{round(pic/frame_rate*1e+6,3)} mks',
                            "method": "animate"}
                            
            fig_dict['layout']['yaxis2']['range'] = [0,max(vertical_temp)+10]
            fig_dict["frames"].append(frame_n)   
            sliders_dict["steps"].append(slider_step)

        fig_dict["layout"]["sliders"] = [sliders_dict]

        fig = go.Figure(fig_dict)

        #fig.show()
        #fig.write_html(path+file[:-4]+'_masked.html')

#recieve data
        time = np.array(range(len(data)))/this_header[20]
        temperature_data = pd.DataFrame({'time': time})

        temperature_line = []
        temperature_point = []

        for tres in range(10):
            sample = []
            for pic in range(len(data)):
                image_2D = ip.form_image(this_header, data[pic])[0]-273.15
                
                mask = bin_image(image_2D, image_2D.max()*(tres*0.1))
                final_image = (image_2D-first_frame)*mask
                if np.array(mask).sum():
                    sample.append(final_image.sum()/np.array(mask).sum())
                else:
                    sample.append(0)
                

            temperature_data[f'Tr_{round(tres*0.1,2)}'] = sample

        for pic in range(len(data)):
            image_2D = ip.form_image(this_header, data[pic])[0]-273.15 - first_frame
            temperature_line.append(image_2D[10].sum()/64)
            temperature_point.append(image_2D.max())

        temperature_data['Line'] = temperature_line
        temperature_data['Point'] = temperature_point

        temperature_data.to_csv(path+'Temperature_Spec_'+specimen+'Max_Tr.csv', index = False, sep = '\t')

        fig3 = go.Figure()
        fig3.update_layout(template = 'plotly_white', width=800, height=600,
                        title = f'Delta Temperature during Experiment {material} Specimen {specimen}')

        fig3.update_yaxes(title = 'Temperature')
        fig3.update_xaxes(title = 'Time')
        trace_area = go.Scatter(x = time, y = temperature_data['Tr_0.8'], name = f'Mean Temperature')
        trace_point = go.Scatter(x = time, y = temperature_point, name = 'Max Temperarure')

        fig3.add_trace(trace_area)
        fig3.add_trace(trace_point)
        #fig3.write_html(path+file[:-4]+'_data.html')



    
