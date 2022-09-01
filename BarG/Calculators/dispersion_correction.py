from numpy.fft import fft, ifft
from numpy import zeros, pi, real, exp

from .bancroft_interpolation import bancroft_interpolation
from .phase_velocity_calculation import phase_velocity_calculation


def dispersion_correction(update_logger, CA):
    """
        This function corrected the signals due to their dispersion in the bar.
        This is done with Fourier transforms (FFT -> Correction -> Inverse FFT)
        Input:  CoreAnalyzer (CA) object
        Output: Corrected signals (incident, reflected, transmitted)
    """

    vcc_incid, vcc_trans, vcc_reflected = CA.incid.y, CA.trans.y, CA.refle.y
    bar_diameter, tpp, sound_velocity, poisson_ratio = CA.bar_diameter, CA.tpp, CA.sound_velocity, CA.poisson_ratio
    first_gage, second_gage = CA.first_gage, CA.second_gage

    #   Perform FFT on all signals:
    fft_incid = fft(vcc_incid, axis=0)
    fft_trans = fft(vcc_trans, axis=0)
    fft_reflected = fft(vcc_reflected, axis=0)

    n = len(fft_incid)  # length of signals
    bar_radius = bar_diameter / 2

    frequencies = zeros(n)
    change_in_frequency = 1 / n / tpp

    #   harmonic series
    for i in range(n):
        frequencies[i] = change_in_frequency * (i + 1)

    ratios = bancroft_interpolation(poisson_ratio)

    #   Velocities will be filled with the interpolated velocities.
    velocities = zeros(n)

    #   Incident, Reflected & Transmitted phases respectively
    i_phase = []
    r_phase = []
    t_phase = []

    update_logger("...obtaining Fourier components")
    for i in range(n // 2):
        #   Calculating (by interpolation) the phase velocity of each Fourier component.
        velocities[i] = phase_velocity_calculation(frequencies[i], bar_radius, sound_velocity, ratios)

        '''
                    Note that the first is positive (+) and the following two are negative (-). 
                    This is because the incident
                    wave is the one prior to the impact, so we move it forward in time,
                    and the transmitted and reflected occur after the impact, 
                    therefore are needed to move backwards in time.
        '''

        #   Calculate phase changes:
        i_phase.append(2 * pi * frequencies[i] * first_gage * ((1 / sound_velocity) - (1 / velocities[i])))
        r_phase.append(-2 * pi * frequencies[i] * first_gage * ((1 / sound_velocity) - (1 / velocities[i])))
        t_phase.append(-2 * pi * frequencies[i] * second_gage * ((1 / sound_velocity) - (1 / velocities[i])))

    '''
                    The following deals with Aliasing of the Fourier Transform analytically.
    '''

    i_phase.append(0)
    r_phase.append(0)
    t_phase.append(0)

    for i in range(n):
        i_phase.append(- i_phase[n // 2 - i])
        r_phase.append(- r_phase[n // 2 - i])
        t_phase.append(- t_phase[n // 2 - i])

    fti = []
    ftr = []
    ftt = []

    #   Add the phase change to each Fourier component.
    #   '1j = sqrt(-1)'
    for i in range(min(len(fft_reflected), len(r_phase))):
        fti.append(exp(1j * i_phase[i]) * fft_incid[i])
        ftr.append(exp(1j * r_phase[i]) * fft_reflected[i])
        ftt.append(exp(1j * t_phase[i]) * fft_trans[i])

    update_logger("...Fourier components obtained, performing inverse Fourier transform...")
    # Inverse Fourier transform
    clean_incident = real(ifft(fti, axis=0))
    clean_reflected = real(ifft(ftr, axis=0))
    clean_transmitted = real(ifft(ftt, axis=0))

    # Damp factor fixing
    damp_f = CA.damp_f
    corrected_incident = clean_incident * exp((-1) * damp_f * first_gage)
    corrected_reflected = clean_reflected * exp((+1) * damp_f * first_gage)
    corrected_transmitted = clean_transmitted * exp((+1) * damp_f * second_gage)

    update_logger("Dispersion Correction CMPLT.")
    return corrected_incident, corrected_transmitted, corrected_reflected