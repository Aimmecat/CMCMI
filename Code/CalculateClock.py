import os
import numpy as np
import math
import secrets

cwd = os.getcwd()
output_path = os.path.join(cwd, '..', 'Output', 'Latency')
output_path2 = os.path.join(cwd, '..', 'Output', 'Constant')

P_name = ['192', '224', '256', '384', '521', '1279', '2203']

Hz = 3e9

clock_for_1us = (1 / Hz) * 1e6


def GetData(data_path):
    with open(data_path, 'r') as f:
        data = [float(line.strip()) for line in f]
    return data


if __name__ == "__main__":
    total_delay_list = []
    diff_list = []
    record = []
    record2 = []
    for idx in range(7):
        algorithm_data_path2 = os.path.join(output_path2,
                                            'Latency_of_' + "BY" + '_for_P_' + P_name[idx] + '.txt')
        data2 = GetData(algorithm_data_path2)
        record2.append(data2[0])
        print("Latency  for P_" + P_name[idx], 'is', round(data2[0] / clock_for_1us), 'clock')
