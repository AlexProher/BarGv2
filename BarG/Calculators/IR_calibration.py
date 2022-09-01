from numpy import mean, diff, exp
from pandas import DataFrame
from scipy.optimize import curve_fit
from .k_temp import k_temp
from ..Analysis.SignalProcessing import zeroing


def IR_calibration(update_logger, volt_IR_CAL, time_IR_CAL, volt_TC_CAL, time_TC_CAL, volt_IR_EXP):
    update_logger("IR Calibration Initialized...")
    HCT_sort = sorted(volt_IR_CAL, reverse=True)

    #   correct signal to zero by first 4 maximas and minimas
    HCT_delta_correct = mean(HCT_sort[0:3]) + mean(HCT_sort[-4:-1])
    """
        After zeroing the HCT signal previously, the positive and negative
        values are almost symmetric. the total voltage for the HCT is the
        differenc: (+ voltage) - (- voltage), but since they are almost equal
        it's possible just to multiply the positive values by 2 and have the
        required difference (delta) in the voltage, this timr just regarding
        to zero. Hence HCT is multiplied by 2 at the end.
    """

    HCT = [2 * (X - HCT_delta_correct / 2) for X in volt_IR_CAL]
    #   Take HCT's upper envelope:
    df = DataFrame(data={"y": HCT}, index=time_IR_CAL)

    windowsize = 20
    df["y_upperEnv"] = df["y"].rolling(window=windowsize).max().shift(int(-windowsize / 2))
    df["y_lowerEnv"] = df["y"].rolling(window=windowsize).min().shift(int(-windowsize / 2))

    from math import isnan
    HCT_envelope = df["y_upperEnv"].values.tolist()
    for i in range(len(HCT_envelope)):
        if not isnan(HCT_envelope[i]):
            HCT_envelope = HCT_envelope[i:]
            volt_TC_CAL = volt_TC_CAL[i:]
            time_IR_CAL = time_IR_CAL[i:]
            time_TC_CAL = time_TC_CAL[i:]
            break

    for i in range(len(HCT_envelope)):
        if not isnan(HCT_envelope[len(HCT_envelope) - i - 1]):
            HCT_envelope = HCT_envelope[:-i]
            volt_TC_CAL = volt_TC_CAL[:-i]
            time_IR_CAL = time_IR_CAL[:-i]
            time_TC_CAL = time_TC_CAL[:-i]
            break

    """
        The following automatically crops the unwanted ~ constant 
        beginning of the HCT's envelope.
    """

    #   Take derivative
    HCT_envelope_diff = diff(HCT_envelope)
    time_diff = time_IR_CAL[1] - time_IR_CAL[0]

    for i in range(len(HCT_envelope)):
        HCT_envelope_derivative = HCT_envelope_diff[i] / time_diff

        #   If the derivative is negative enough, crop the signal.
        if HCT_envelope_derivative < -0.05:
            #   Crop the signals according to the found crop index
            HCT_envelope = HCT_envelope[i:]
            HCT_time = time_IR_CAL[i:]

            TC = volt_TC_CAL[i:]
            TC_time = time_TC_CAL[i:]

            zeroing([HCT_time, TC_time])

            update_logger("...Cropping Complete")
            break

    #   Calculate a double exponential fit for the TC - HCT graph:
    #   y(x) = a * exp(b * x) + c + exp(d * x)
    def double_exponential_fit(x, a, b, c, d):
        return a * exp(b * x) + c * exp(d * x)

    P0 = (150, 0.04, -130, -0.2)

    coeff, _ = curve_fit(double_exponential_fit, HCT_envelope, TC, p0=P0, maxfev=5000)
    c1 = coeff[0]
    c2 = coeff[1]
    c3 = coeff[2]
    c4 = coeff[3]
    
    update_logger("...Curve Fitting 1 CMPLT")
    #   Calculate R^2 of the fit:
    def_HCT = [double_exponential_fit(X, c1, c2, c3, c4) for X in HCT_envelope]

    # residuals = TC - def_HCT
    # R_squared = sum((residuals ** 2) / def_HCT)

    Volt2Temp = k_temp(TC)
    update_logger("...K Temp Configured (Volt2Temp)")
    coeff, _ =curve_fit(double_exponential_fit, HCT_envelope, Volt2Temp, p0=P0, maxfev=5000)
    d1 = coeff[0]
    d2 = coeff[1]
    d3 = coeff[2]
    d4 = coeff[3]

    update_logger("...Curve Fitting 2 CMPLT with function (Volt -> Temperature):")
    update_logger("T(v) = " + str(d1) + " * exp {" + str(d2) + " * v} + " + str(d3) + " * exp {" + str(d4) + " * v}")

    #   Calculate R^2 of the fit:
    #   def_HCT = [double_exponential_fit(X, c1, c2, c3, c4) for X in HCT_envelope]
    #   residuals = TC - def_HCT
    #   temp_R_squared = sum((residuals ** 2) / def_HCT)

    IR_temperature = [double_exponential_fit(X, d1, d2, d3, d4) for X in volt_IR_EXP]
    zero_IR_temperature = mean(IR_temperature[1:50])
    IR_temperature = [T - zero_IR_temperature for T in IR_temperature]

    update_logger("IR Calibration CMPLT.")
    return IR_temperature
