import os
import numpy as np
import matplotlib.pyplot as plt

cwd = os.getcwd()
output_path = os.path.join(cwd, '..', 'Output', 'Latency')


def GetData(data_path):
    with open(data_path, 'r') as f:
        data = [float(line.strip()) for line in f]
    return data


P_name = ['192', '224', '256', '384', '521', '1279', '2281']

color_list = ['green', '#FF6347', '#FF69B4', '#B8860B', '#A0522D', '#1E90FF']

test_alg = ['BEEA', 'HBEEA', 'Stein', 'P_Stein', 'MI', 'CT_IMI']

if __name__ == "__main__":

    bit_list = [j for j in range(1, 2282)]
    plt.figure(figsize=(20, 10))

    diff_list_total = np.zeros((7, 2281))

    for i in range(len(test_alg)):

        total_delay_list = []
        diff_list = []
        for idx in range(7):
            algorithm_data_path = os.path.join(output_path,
                                               'Latency_of_' + test_alg[i] + '_for_P_' + P_name[idx] + '.txt')
            data = GetData(algorithm_data_path)
            total_delay_list += data
            data_array = np.array(data)
            diff_list += (data_array - np.mean(data_array)).tolist()
        diff_list_total[i] = np.array(diff_list)
        plt.plot(bit_list, total_delay_list, '--', color=color_list[i], label=test_alg[i])

    plt.title("The efficiency of different algorithm in different bits length", fontsize=30)
    plt.xlabel("Bit-Length", fontsize=20)
    plt.ylabel("Latency(us)", fontsize=20)
    plt.legend(loc="lower right", fontsize=15)
    plt.grid(ls='--', alpha=0.4)
    plt.xticks(range(1, 2400, 80))
    plt.yticks(range(0, 3500, 200))
    plt.gca().yaxis.set_ticklabels([])

    plt.axes([0.16, 0.448, 0.32, 0.4])
    for idx in range(6):
        plt.plot(bit_list, diff_list_total[idx], '--', color=color_list[idx], label=test_alg[idx])
    plt.title("Diff")
    plt.legend(loc="lower right", fontsize=12)
    plt.grid(ls='--', alpha=0.4)
    plt.xticks(range(1, 2400, 200))
    plt.yticks(range(-400, 450, 50))

    plt.show()
