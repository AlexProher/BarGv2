from numpy import transpose, savetxt, array
import numpy as np
import os

from scipy.integrate import trapz, cumtrapz

from BarG.Calculators import FinalCalculation 
from BarG.Calculators.IR_calculation import IR_calculation
from BarG.Calculators.dispersion_correction import dispersion_correction
from BarG.Analysis import SignalProcessing

import BarG.Analysis._read_files as rd
from BarG.Utilities.TwoDimVec import TwoDimVec

class Experiment:
    def __init__(self, materials = None):
        if materials:
            self.materials = materials
            self.list_materials = [material.title for material in materials]
        else:
            self.materaials = []
            self.list_materials = []

    def add_material(self, material):
        if not isinstance(material, Material):
            return False
        self.materals.append(material)
        self.list_materials.append(material.title)

    def get_material(self, material):
        if isinstance(material, int):
            if material <= len(self.list_materials):
                return self.materials[material]
            else:
                print(f'Choose number from 0 to {len(self.list_materials)}')
        elif isinstance(material, str):
            if material in self.list_materials:
                return self.materials[self.list_materials.index(material)]
            else:
                print(f'No such material, choose from list {self.list_materials}')
        else:
            print(f'Choose number from 0 to {len(self.list_materials)} or title from list {self.list_materials}')

    def __call__(self, title):
        pass


class Material:
    def __init__(self, material):
        self.title = material
        self.__list_specimens = []
        self.__specimens = []
        self.__specimen_counter = -1

    


    def add_specimen(self, specimen):

        if isinstance (specimen, list):
            for item in specimen:
                self.add_specimen(item)
        else:
            if not isinstance(specimen, Specimen):
                return False
            self.__specimen_counter +=1
            self.__specimens.append(specimen)
            self.__list_specimens.append(specimen.title)
            specimen.material = self.title
            specimen.index = self.__specimen_counter
        
    def get_specimens(self):
        return self.__specimens

    

    def get_list_specimens(self):
        return self.__list_specimens
class Specimen:
    
    def __init__(self, specimen):
        self.title = specimen
        self.material = None
        self.index = None

        self.raw_incid = None
        self.raw_transm = None
        self.raw_time = None

        self.l = None
        self.d = None

        self.valid = True
        self.IR = None
        self.mech = True


        self.time = None
        self.incid = None
        self.trans = None
        self.reflect = None
        self.u_in = None
        self.u_out = None
        self.eng_strain = None
        self.eng_stress = None
        self.F_in = None
        self.F_out = None
        self.true_strain = None
        self.true_stress = None
        self.energy = None

        self.raw_temperature = None
        self.raw_time_IR = None

        self.temperature = None
        self.time_IR = None

    def __str__(self):
        return self.title
    
    def __repr__(self):
        return self.title

class CoreAnalyzer:

    def __init__(self, path,  parameters, specimen):

        self.log = ''
        self.current_specimen = specimen
        self.path_folder = path
        self.result_path = None
        self.parameters = parameters
        self.current_specimen.parameters = parameters

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
        #self.young_modulus = 71.7e+9
        self.first_gage = parameters[4]
        self.second_gage = parameters[5]
        self.sound_velocity = parameters[6]
        #self.sound_velocity = 5050
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

        self.ir_mode = specimen.IR
        self.mech_exp = specimen.mech

        self.raw_temperature = None
        self.raw_time_IR = None
        self.temperature = None
        self.time_IR = None

    def begin_analyse(self, files):
        if self.mech_exp:

            files = os.listdir(self.path_folder)
            #Загружаем сигналы эксперимента
            data_FLT = [item for item in files if '.FLT' in item]
            data_WFT = [item for item in files if '.WFT' in item]

            if data_FLT:
                signal1 = rd.read_flt(self.path_folder +data_FLT[0])
                signal2 = rd.read_flt(self.path_folder +data_FLT[1])
            elif data_WFT:
                hdr, signal1 = rd.read_wft(self.path_folder +data_WFT[0])
                hdr, signal2 = rd.read_wft(self.path_folder +data_WFT[1])
            else:
                self.update_logger('No mech data to analyse')
                self.mech_exp = False

            #Определяем кто из них какой
        if self.mech_exp:
            if min(signal1.vol) < min(signal2.vol):
                incid = signal1.vol-signal1.vol[0]
                transm = signal2.vol-signal2.vol[0]
            else:
                incid = signal2.vol-signal2.vol[0]
                transm = signal1.vol-signal1.vol[0]
            time = signal1.sec

            self.current_specimen.raw_incid = incid
            self.current_specimen.raw_transm = transm
            self.current_specimen.raw_time = time

            self.load_experiments(np.array(incid), np.array(transm), np.array(time))

        if self.ir_mode:
            IR_calculation(self)
            self.update_logger(f'temperature {len(self.temperature)} - stress {len(self.true_stress_strain[1])}')
        else:
            self.update_logger('No IR data to analyse')
        
        return True
        


    def load_experiments(self, incid, trans, time):
        """
            This function takes data from the loaded experiment and
            makes it into two voltage and two time vectors:
            incident & transmitted.

            It keeps an "og" version - an original version of the vectors
             to be untouched by any processing that follows.
        """

        self.incid = TwoDimVec(time,incid).force_signal_to_start_at_zero()
        self.trans = TwoDimVec(time,trans).force_signal_to_start_at_zero()

        # Extract Time Per Point from the data.
        self.tpp = self.incid.x[1] - self.incid.x[0]

        # og = original. the following are defined as the original signals taken directly from the FLT files.
        # Saving them is necessary for resetting the signal cropping.
        self.incid_og = self.incid_og.create_absolute_copy(self.incid)
        self.trans_og = self.trans_og.create_absolute_copy(self.trans)

        return self.analyze()

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


        self.single_analysis()



        return True 

    def single_analysis(self):

        #corr_incident, corr_transmitted, corr_reflected = dispersion_correction(self.update_logger, self)

        corr_incident, corr_transmitted, corr_reflected, \
        self.incid.x, self.trans.x, self.refle.x \
            = SignalProcessing.cross_correlate_signals(self.update_logger, 
                                                    self.incid.y,self.trans.y,self.refle.y,
                                                      self.incid.x, self.trans.x, self.refle.x,
                                                       self.smooth_value)
 # corr_incident, corr_transmitted,corr_reflected,


        self.corr_incid.y = corr_incident
        self.corr_trans.y = corr_transmitted
        self.corr_refle.y = corr_reflected

        #self.corr_incid.y = self.incid.y
        #self.corr_trans.y = self.trans.y
        #self.corr_refle.y = self.refle.y



        return FinalCalculation.final_calculation(self.update_logger, self)

   
    def update_logger(self, text):
        self.log += text
        print (text)
    
    def save_data(self):
        

        desired_path = self.result_path

        vectors = [self.incid_og.y, self.trans_og.y, self.incid_og.x]
        df = transpose(array(vectors))
        filepath = desired_path + '/Raw Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [self.corr_incid.y, self.corr_refle.y, self.corr_trans.y, self.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Corrected Signals.csv'
        savetxt(filepath, df, delimiter=',', header='Incident [V], Reflected [V], Transmitted [V], time [s]', fmt='%s')

        vectors = [self.u_in, self.u_out, self.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Displacements.csv'
        savetxt(filepath, df, delimiter=',', header='u_in [m], u_out [m], time [s]', fmt='%s')

        vectors = [self.true_stress_strain[0], self.true_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain True.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [self.eng_stress_strain[0], self.eng_stress_strain[1]]
        df = transpose(array(vectors))
        filepath = desired_path + '/Stress-Strain Engineering.csv'
        savetxt(filepath, df, delimiter=',', header='Strain, Stress', fmt='%s')

        vectors = [self.F_in, self.F_out, self.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Forces.csv'
        savetxt(filepath, df, delimiter=',', header='F_in [N], F_out [N], time [s]', fmt='%s')

        vectors = [self.v_in, self.v_out, self.time]
        df = transpose(array(vectors))
        filepath = desired_path + '/Velocities.csv'
        savetxt(filepath, df, delimiter=',', header='v_in [m/s], v_out [m/s], time [s]', fmt='%s')

        if (self.ir_mode):
            vectors = [self.time_IR, self.temperature]
            df = transpose(array(vectors))
            filepath = desired_path + '/Temperature.csv'
            savetxt(filepath, df, delimiter=',', header='time [s], temperature [C]', fmt='%s')


