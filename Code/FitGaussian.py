from scipy.optimize import curve_fit
import numpy as np

def gaussian(x, a, mu, sigma):
    return a * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))

def Fit_Curve_Gaussian(data_x, data_y, init_vector=None):

    sort_idx = np.argsort(data_x)
    data_x_sorted = np.array(data_x)[sort_idx]
    data_y_sorted = np.array(data_y)[sort_idx]

    parameter, _ = curve_fit(gaussian, data_x_sorted, data_y_sorted, p0=init_vector)

    return parameter
