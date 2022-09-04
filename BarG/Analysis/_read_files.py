import pandas as pd
import biosig as bs
import numpy as np

def read_wft(way):
    HDR=bs.header(way)
    data=bs.data(way)
    sr = float(HDR.split('\n')[9][HDR.split('\n')[9].find(':')+2:-1])

    res = pd.DataFrame({'sec':np.arange(len(data))/sr,
                        'vol':[item[0] for item in data]})
    
    return HDR, res

def read_flt(way):
    file = open(way)
    file.readlines(13)
    res = pd.read_csv(file, header = None, sep = '\t', names = ['vol', 'sec'])
    file.close()
    return res