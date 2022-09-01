import os
from numpy import loadtxt, zeros


def bancroft_interpolation(poisson_ratio):
    """
        This function uses Bancroft's Data to calculate the different wave velocities.
        Please read the manual "Signal Cleaning" for a full understanding of this function.
        The specific number 26 is simply the number of rows in Bancroft's data table.
    """
    p_r = poisson_ratio  # The bar's Poisson's ratio NEEDS TO BE ADDED
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    bancrofts_data = loadtxt("../Calculators/bancrofts_data.txt")

    rwr = zeros(26)  # Radius - Wavelength Ratio (RWR)
    phase_velocities = zeros(26)

    # The following interpolates poisson's ratio according to its value.
    # "column" is the needed column from Bancroft's data table (based on Poisson's ratio's value).

    if 0.2 <= p_r <= 0.25:
        interpolated_p_r = (p_r - 0.2) / (0.25 - 0.2)
        column = 0

    elif 0.25 <= p_r <= 0.30:
        interpolated_p_r = (p_r - 0.25) / (0.30 - 0.25)
        column = 1

    elif 0.3 <= p_r <= 0.35:
        interpolated_p_r = (p_r - 0.3) / (0.35 - 0.3)
        column = 2

    else:
        column = 3
        print('nu out of program range')

    if column != 3:
        for j in range(26):
            rwr[j] = bancrofts_data[j][4] / 2
            phase_velocities[j] = bancrofts_data[j][column] + (
                    bancrofts_data[j][column + 1] - bancrofts_data[j][column]) * interpolated_p_r

    ratios = zeros((26, 2))  # previously named 'hh'

    rwr = rwr[0:25]
    rwr = rwr[:]

    phase_velocities = phase_velocities[0:25]
    phase_velocities = phase_velocities[:]

    for i in range(25):
        ratios[i][0] = rwr[i]
        ratios[i][1] = phase_velocities[i]

    return ratios