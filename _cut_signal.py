import numpy as np
from scipy import interpolate

##
#Идея следующая Передаются два сигнала и соответствующие массивы времени
#Первый сигнал - сигнал деформаций он короче чем второй, но он лучше дескитезирован
#
#Второй сигнал - синал температуры его нужно интерполировать и обрезать по длине первого сигнала


def find_slope(sign1, sign2): #sign1 - Сигнал деформаций (опорный), sign2 - Сигнал температуры
    tr1 = sign1.max()*0.01
    tr2 = sign2.max()*0.01
    bin_sig1 = [1 if x>tr1 else 0 for x in sign1]
    bin_sig2 = [1 if x>tr2 else 0 for x in sign2]
    return (bin_sig1.index(1), bin_sig2.index(1))

def my_interpolation(t, data):
    xnew = np.arange(0,len(data)-1,t*1e-9)
    xnew[-1] = round(xnew[-1])
    x = np.arange(len(data))
    y = np.array(data)
    f = interpolate.interp1d(x, y, kind = 'quadratic')
    ynew = f(xnew)
    return (xnew, ynew)

def cut_signal(signal1, signal2, time1, time2):
    #сначала интерполируем второй синал чтобы его можно было двигать плавно
    interpolated_signal2 = my_interpolation(signal2, 500)   #500 нс - величина обратная Частоте дискретизации
    p1, p2 = find_slope(signal1, interpolated_signal2)

    

 
    
    return ()
    
