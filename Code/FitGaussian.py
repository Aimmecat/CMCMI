from scipy.optimize import curve_fit
import scipy.integrate as spi
from scipy.stats import norm
import math
import numpy as np
import os
import matplotlib.pyplot as plt


def GetData(cnt_list_path, number_path):
    with open(cnt_list_path, 'r') as f:
        cnt_list = [int(line.strip()) for line in f]
    with open(number_path, 'r') as f:
        number = [int(line.strip()) for line in f]
    return cnt_list, number

def discrete_gaussian(k, mu, sigma):
    return norm.pdf(k + 0.5, loc=mu, scale=sigma) - norm.pdf(k - 0.5, loc=mu, scale=sigma)


def gaussian(x, mu, sigma):
    return np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))


def Fit_Curve_Gaussian(data_x, data_y, init_vector=None):

    parameter, _ = curve_fit(gaussian, data_x, data_y, p0=init_vector)
    # parameter, _ = curve_fit(discrete_gaussian, data_x, data_y, p0=init_vector)

    return parameter


P_name = ['192', '224', '256', '384', '521', '1279', '2281']

if __name__ == "__main__":
    cwd = os.getcwd()
    copy_output_path = os.path.join(cwd, '..', 'Copy_Output')

    for idx in range(len(P_name)):
        cnt_list_path = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_cnt_list.txt')
        number_path = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_number.txt')
        cnt_list, number = GetData(cnt_list_path, number_path)

        sort_idx = np.argsort(cnt_list)
        data_x_sorted = np.array(cnt_list)[sort_idx]
        data_y_sorted = np.array(number)[sort_idx]

        data = []
        for i in range(len(cnt_list)):
            data += number[i] * [cnt_list[i]]

        mean, std = np.mean(data), np.std(data)

        low_boundary, up_boundary = min(cnt_list), max(cnt_list)

        max_data_y = max(data_y_sorted)

        data_y_sorted = data_y_sorted / max_data_y

        parameter = Fit_Curve_Gaussian(data_x_sorted, data_y_sorted, init_vector=[mean, std])

        mu, sigma = parameter

        z = (up_boundary - mu) / sigma
        upper = (2*int(P_name[idx]) - mu) / sigma

        cdf, _ = spi.quad(lambda t: gaussian(t, 0, 1), z, upper)

        total_prob = 0.0
        less_upper_prob = 0.0
        for i in range(1, 2 * int(P_name[idx])):
            prob = gaussian(i, *parameter)
            total_prob += prob
            if i <= up_boundary:
                less_upper_prob += prob
        residue_prob = 1 - (less_upper_prob / total_prob)

        mu_minus_3sigma, mu_add_3sigma = mu - 3 * sigma, mu + 3 * sigma

        least_bit_length = up_boundary
        while gaussian(least_bit_length, *parameter) > 1 / max_data_y:
            least_bit_length += 1

        gaussian_y = gaussian(data_x_sorted, *parameter)

        MSE = sum((gaussian_y - data_y_sorted)**2)

        plt.plot(data_x_sorted, data_y_sorted, 'b.', label='data')
        plt.plot(data_x_sorted, gaussian_y, 'r-', label='fit')

        print("P_"+P_name[idx]+':', mu, sigma, mu_minus_3sigma, mu_add_3sigma, low_boundary, up_boundary, MSE, least_bit_length, cdf, residue_prob, math.log2(residue_prob))
    plt.show()