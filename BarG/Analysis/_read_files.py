import pandas as pd
#import biosig as bs
import os
import shutil
import numpy as np
""""

If you install biosig use this fuction

def read_wft(way):
    HDR=bs.header(way)
    data=bs.data(way)
    sr = float(HDR.split('\n')[9][HDR.split('\n')[9].find(':')+2:-1])

    res = pd.DataFrame({'sec':np.arange(len(data))/sr,
                        'vol':[item[0] for item in data]})
    
    return HDR, res
"""
def apply_exe(path):
    WFT2FLT_path = shutil.copy("C:/Users/dflws/Desktop/BarGv2/BarGv2/BArG/ProgramFiles/WFT2FLTN.EXE", path)  # Copy the WFT2FLT program into the given path.
    WFT2FLT_command_path = WFT2FLT_path + " -dir=."  # This is the full command that is used in the cmd.

    os.chdir(path)  # Run cmd through the given path.
    os.system(WFT2FLT_command_path)  # Run the WFT2FLT program using cmd.
    os.remove(WFT2FLT_path)  # Remove the WFT2FLT.EXE file from the path.

    files = os.listdir(path)
    os.makedirs(path + '/' + "Original WFT Files")
    for file in files:
        file_name, file_type = os.path.splitext(file)
        file_type = file_type[1:]
        if file_type == "WFT":
            shutil.move(path + "/" + file, path + '/' + "Original WFT Files")

def read_wft(way):
    apply_exe(way)
    files = os.listdir(way)
    data_FLT = [item for item in files if '.FLT' in item]

    if data_FLT:
        signal1 = read_flt(way +data_FLT[0])
        signal2 = read_flt(way +data_FLT[1])

    return signal1, signal2


def read_flt(way):
    
    res = pd.read_csv(way, header = 1, sep = '\t', names = ['vol', 'sec'])
    
    return res