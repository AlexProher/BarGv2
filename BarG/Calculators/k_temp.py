from scipy.interpolate import interp1d
from numpy import loadtxt, arange

from BarG.Calculators import OneDimInterp


def k_temp(v):
    """
    K = Type of Thermocouple
    """

    vector_file = open("../ProgramFiles/k_type.txt")
    k_type = loadtxt(vector_file, delimiter='\t')
    vector_file.close()
    temp = []
    volt = []
    for i in range(len(k_type)):
        try:
            temp.append(float(k_type[i][0]))
            volt.append(float(k_type[i][1]))

        except:
            continue
    #   VOLTS CONVERTED TO mVOLT
    v = [X * 1000 for X in v]
    size_v = len(v)

    #   for T type thermocouple converts volts in temperature w/r to zero junction
    #   correction for ambient temperature

    tamb = 22
    vamb = 0.879

    inf = -400
    sup = +400

    intt = OneDimInterp.interp(temp, 5)
    intv = OneDimInterp.interp(volt, 5)

    temp = intt
    volt = intv
    v = [X + vamb for X in v]
    t_resu = []
    for i in range(size_v):
        diff_volt = [abs(v[i] - X) for X in volt]
        min_diff_volt = min(diff_volt)
        index = diff_volt.index(min_diff_volt)
        if volt[index] >= v[i]:
            del_v = volt[index] - volt[index - 1]
            del_t = temp[index] - temp[index - 1]
            t_resu.append(temp[index - 1] + (del_t / del_v) * (v[i] - volt[index - 1]))
        else:
            del_v = volt[index + 1] - volt[index]
            del_t = temp[index + 1] - temp[index]
            t_resu.append(temp[index] + (del_t / del_v) * (v[i] - volt[index]))

    return t_resu


