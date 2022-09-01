#from scipy.stats import linregress


def get_linear_regression(x, y):
    slope, intercept, _, _, _ = linregress(x, y)
    return [intercept + slope * X for X in x], intercept, slope

