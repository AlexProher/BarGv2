from numpy import arange
from scipy.interpolate import interp1d


def interp(ys, mul):
    # linear extrapolation for last (mul - 1) points
    ys = list(ys)
    ys.append(2 * ys[-1] - ys[-2])
    # make interpolation function
    xs = arange(len(ys))
    fn = interp1d(xs, ys, kind="cubic")
    # call it on desired data points
    new_xs = arange(len(ys) - 1, step=1. / mul)
    return fn(new_xs)