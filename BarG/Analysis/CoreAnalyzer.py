from numpy import transpose, savetxt, array
import numpy as np
import sys
import os

from scipy.integrate import trapz, cumtrapz

from BarG.Calculators import FinalCalculation
from BarG.Calculators.dispersion_correction import dispersion_correction
from BarG.Analysis import SignalProcessing

from BarG.Utilities.TwoDimVec import TwoDimVec


class CoreAnalyzer:

    def __init__(self, path,  parameters):

        self.log = ''

        self.path_folder = path
        self.parameters = parameters

        self.incid = TwoDimVec()
        self.trans = TwoDimVec()
        self.refle = TwoDimVec()

        self.corr_incid = TwoDimVec()
        self.corr_trans = TwoDimVec()
        self.corr_refle = TwoDimVec()

        self.incid_og = TwoDimVec()
        self.trans_og = TwoDimVec()

        self.incid_strain = None
        self.trans_strain = None

        

        self.spec_diam = parameters[0]
        self.specimen_length = parameters[1]
        self.bar_diameter = parameters[2]
        self.young_modulus = parameters[3]
        self.first_gage = parameters[4]
        self.second_gage = parameters[5]
        self.sound_velocity = parameters[6]
        self.gage_factor = parameters[7]
        self.bridge_tension = parameters[8]
        self.spacing = int(parameters[9])
        self.prominence_percent = parameters[9]
        #self.smooth_value = parameters[11]
        self.smooth_value = 57
        self.poisson_ratio = 0.33
        self.damp_f = 10 ** (-3)
        self.bridge_type = 0.25
        self.mode = 'compression'
        


    def load_experiments(self, incid, trans, time):
        """
            This function takes data from the loaded experiment and
            makes it into two voltage and two time vectors:
            incident & transmitted.

            It keeps an "og" version - an original version of the vectors
             to be untouched by any processing that follows.
        """
        #self.incid = TwoDimVec([incid[i][1] for i in range(len(incid))],
        #                       [incid[i][0] for i in range(len(incid))]).force_signal_to_start_at_zero()
        #self.trans = TwoDimVec([trans[i][1] for i in range(len(trans))],
        #                       [trans[i][0] for i in range(len(trans))]).force_signal_to_start_at_zero()
        self.incid = TwoDimVec(time,incid).force_signal_to_start_at_zero()
        self.trans = TwoDimVec(time,trans).force_signal_to_start_at_zero()

        # Extract Time Per Point from the data.
        self.tpp = self.incid.x[1] - self.incid.x[0]

        # og = original. the following are defined as the original signals taken directly from the FLT files.
        # Saving them is necessary for resetting the signal cropping.
        self.incid_og = self.incid_og.create_absolute_copy(self.incid)
        self.trans_og = self.trans_og.create_absolute_copy(self.trans)

        return True

    def analyze(self):
        """
            This function is the main function that calls all the
            processing and calculations done on the experiment files.

        purpose: Analyze one given experiment or all of the experiments
        sp_mode: Signal Proceesing mode: Manual / Automatic cropping
        return: True is analysis and report production was succusful, False otherwise.
        """

        #   Analyze only one given experiment
        incid, trans, refle= SignalProcessing.auto_crop(self.update_logger, self)
        self.incid = self.incid.create_absolute_copy(incid)
        self.trans = self.trans.create_absolute_copy(trans)
        self.refle = self.refle.create_absolute_copy(refle)

        return self.single_analysis()

    def single_analysis(self):

        corr_incident, corr_transmitted, corr_reflected = dispersion_correction(self.update_logger, self)

        corr_incident, corr_transmitted, corr_reflected, \
        self.incid.x, self.trans.x, self.refle.x \
            = SignalProcessing.cross_correlate_signals(self.update_logger, corr_incident, corr_transmitted,
                                                       corr_reflected,
                                                       self.incid.x, self.trans.x, self.refle.x,
                                                       self.smooth_value)
        self.corr_incid.y = corr_incident
        self.corr_trans.y = corr_transmitted
        self.corr_refle.y = corr_reflected

        valid = FinalCalculation.final_calculation(self.update_logger, self)

        if valid:
 
            #self.save_data(self, self.exp_num, self.parameters)

            return True

        return False

    def analyze_all(self):
        self.corr_incid.y, self.corr_trans.y, self.corr_refle.y = dispersion_correction(self.update_logger, self)
        self.corr_incid.x = self.incid.x.copy()
        self.corr_trans.x = self.trans.x.copy()
        self.corr_refle.x = self.refle.x.copy()

        valid = FinalCalculation.final_calculation(self)
        if valid:
            return True
        else:
            return False
    def update_logger(self, text):
        self.log += text
        print (text)
    
    def save_data(CA, exp_num, parameters):
        

        desired_path = CA.path_folder + "/Exp #" + str(exp_num)

        
        
        vectors = [CA.incid_og.y, CA.trans_og.y, CA.incid_og.x]
        df = transpose(array(vectors))
        filepath = desired_path + '/Raw Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [CA.corr_incid.y, CA.corr_refle.y, CA.corr_trans.y, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Corrected Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Reflected [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [CA.u_in, CA.u_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Displacements.csv'
        savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

        vectors = [CA.true_stress_strain[0], CA.true_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain True.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.eng_stress_strain[0], CA.eng_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain Engineering.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [CA.F_in, CA.F_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Forces.csv'
        savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

        vectors = [CA.v_in, CA.v_out, CA.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Velocities.csv'
        savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')


        f_path = desired_path + "/Parameters.txt"

        if os.path.isfile(f_path):
            os.remove(f_path)

        f = open(f_path, 'x')
        f = open(f_path, 'r+')
        f.truncate(0)
        s = ""

        s += str(parameters[0][0]) + ": " + str(parameters[0][1]) + " [m]" + "\n"
        s += str(parameters[1][0]) + ": " + str(parameters[1][1]) + " [m]" + "\n"
        s += str(parameters[2][0]) + ": " + str(parameters[2][1]) + " [m]" + "\n"
        s += str(parameters[3][0]) + ": " + str(parameters[3][1] / (10 ** 9)) + " [GPa]" + "\n"
        s += str(parameters[4][0]) + ": " + str(parameters[4][1]) + " [m]" + "\n"
        s += str(parameters[5][0]) + ": " + str(parameters[5][1]) + " [m]" + "\n"
        s += str(parameters[6][0]) + ": " + str(parameters[6][1]) + " [m/s]" + "\n"
        s += str(parameters[7][0]) + ": " + str(parameters[7][1]) + "\n"
        s += str(parameters[8][0]) + ": " + str(parameters[8][1]) + " [V]" + "\n"
        s += "Spacing: " + str(CA.spacing) + " Points" + "\n"
        s += "Prominence: " + str(CA.prominence_percent * 100) + "%" + "\n"
        s += "Curve Smoothing Parameter: " + str(CA.smooth_value * 100) + "\n"
        s += "Average Strain Rate: " + str(CA.mean_strain_rate) + "[1/s]"
        s += "\n"  # For some reason, there is a problem without a new line at the end of the defaults file.
        f.write(s)
        f.close()
