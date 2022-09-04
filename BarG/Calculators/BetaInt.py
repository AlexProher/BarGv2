import numpy as np
from scipy.integrate import trapz

from BarG.Calculators import LinearRegression


def beta_int(update_logger, CA, true_strain, true_stress):
    #   beta_int calculation:
    rho = CA.density
    Cp = CA.heat_capacity
    """
        The plastic strain is the strain after the elastic region. 
        A cropping should be done to obtain this area.
    """

    length = len(true_stress)
    from scipy.stats import linregress

    #   Find sigma_y (yield point):
    """
        To find sigma_y we perform a linear regression repeatedly, 
        each iteration enlarging the size of the vector upon which 
        the regression os performed. When the value of r^2 > 0.9
        we can assume we found the elastic zone (since it is linear). 

        Once r^2 > 0.9 is reached we start searching for our cropping point:
        this is where we leave the elastic zone and the curve starts to become
        less inclined. Once we enter the r^2 < 0.9 zone we can approximate that 
        this is where the plastic zone begins. 
    """
    crop_idx = 0
    point_searching_activated = False
    for i in range(10, length):

        _, _, r, _, _ = linregress(true_strain[0:i], true_stress[0:i])

        if 0.9 < r ** 2 and not point_searching_activated:
            point_searching_activated = True

        if r ** 2 < 0.9 and point_searching_activated:
            crop_idx = i
            update_logger("...Yield point found")
            break

    plastic_stress = true_stress[crop_idx:]
    plastic_strain = true_strain[crop_idx:]

    # Uncomment to see (graphically) the actual cropping with respect
    # to the original stress - strain curve (needs to import matplotlib plot):
    """
    plt.figure()
    plt.plot(true_strain, true_stress)
    plt.plot(plastic_strain, plastic_stress)
    plt.show()
    """

    #   Make the strain start at zero:
    de = plastic_strain[0]
    CA.plastic_strain = [X - de for X in plastic_strain]

    CA.plastic_stress = plastic_stress
    CA.IR_temperature = CA.IR_temperature[crop_idx:]
    CA.plastic_time = CA.time[crop_idx:]

    dt = CA.time[0]
    CA.plastic_time = [X - dt for X in CA.plastic_time]

    '''
        Since IR_temperature & the plastic stress are not the same length,
        we shall interpolate the plastic stress & strain to be accordingly.
    '''

    beta_int = []
    Wp = []

    #   Start at 5% of strain vector to avoid singularity:
    starting_idx = int(len(plastic_strain) * 5 / 100) + 1

    for i in range(starting_idx, len(plastic_stress)):
        # [Stress is in MPa thus * 10^6]
        Wp_i = trapz(plastic_stress[0:i], plastic_strain[0:i]) * (10 ** 6)
        Wp.append(Wp_i)
        beta_int.append(rho * Cp * CA.IR_temperature[i] / Wp_i)

    Wp = [0] + Wp
    beta_int = [0] + beta_int

    #   Search for maximum temperature:
    max_temp_idx = np.argmax(CA.IR_temperature)

    CA.beta_int = beta_int
    CA.Wp = Wp[:max_temp_idx]

    CA.LR_T_Wp,\
    CA.LR_T_Wp_intercept,\
    CA.LR_T_Wp_slope = LinearRegression.get_linear_regression(CA.Wp, CA.IR_temperature[:max_temp_idx])

