import secrets
import os
import time
from Code.OtherAlgorithm import FLT
from Code.CompareOtherAlgorithm import TimingSingleAlgorithm

cwd = os.getcwd()
output_path = os.path.join(cwd, '..', 'Output', 'Constant')

P_192 = 2 ** 192 - 2 ** 64 - 1
P_224 = 2 ** 224 - 2 ** 96 + 1
P_256 = 2 ** 256 - 2 ** 224 - 2 ** 96 + 2 ** 64 - 1
P_384 = 2 ** 384 - 2 ** 128 - 2 ** 96 + 2 ** 32 - 1
P_521 = 2 ** 521 - 1
P_1279 = 2 ** 1279 - 1
P_2281 = 2 ** 2281 - 1

N = int(10e0)
scaled = 10e5 / N

P_list = [P_192, P_224, P_256, P_384, P_521, P_1279, P_2281]
P_name = ['192', '224', '256', '384', '521', '1279', '2281']

if __name__ == "__main__":

    data_list_total = []
    for idx, P_str in enumerate(P_name):
        data_list = [secrets.randbelow(2**int(P_name[idx])) for _ in range(N)]
        data_list_total.append(data_list)

    for idx, P in enumerate(P_list):
        calc_time = TimingSingleAlgorithm(data_list_total[idx], FLT, P, idx)
        output_path_time_list = os.path.join(output_path, 'Latency_of_FLT_for_P_' + P_name[idx] + '.txt')
        with open(output_path_time_list, 'w') as f:
            f.write('\n'.join(map(str, [calc_time * scaled])))