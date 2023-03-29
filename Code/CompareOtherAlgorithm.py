from Code.OtherAlgorithm import Test_BEEA, Test_HBEEA, Test_Stein, Test_P_stein, Test_MI
from Code.CTCMI import CT_IMI_CMMI

import os
import time
import secrets

cwd = os.getcwd()
output_path = os.path.join(cwd, '..', 'Output', 'Latency')

test_alg = ['CT_IMI', 'BEEA', 'HBEEA', 'Stein', 'P_Stein', 'MI']
color = ['green', '#FF6347', '#FF69B4', '#B8860B', '#A0522D', '#1E90FF']
alg_list = [CT_IMI_CMMI, Test_BEEA, Test_HBEEA, Test_Stein, Test_P_stein, Test_MI]

N = int(10e3)
scaled = 10e5 / N

P_192 = 2 ** 192 - 2 ** 64 - 1
P_224 = 2 ** 224 - 2 ** 96 + 1
P_256 = 2 ** 256 - 2 ** 224 - 2 ** 96 + 2 ** 64 - 1
P_384 = 2 ** 384 - 2 ** 128 - 2 ** 96 + 2 ** 32 - 1
P_521 = 2 ** 521 - 1
P_1279 = 2 ** 1279 - 1
P_2281 = 2 ** 2281 - 1

# P_list = [P_192, P_224, P_256, P_384, P_521, P_1279, P_2281]
P_list = [P_192]
P_name = ['192', '224', '256', '384', '521', '1279', '2281']
P_round = [202, 233, 263, 384, 521, 1279, 2281]


def CreateRandomNumber(l, h, num):
    if l == h:
        return [l for _ in range(num)]
    return [secrets.randbelow(h - l) + l for _ in range(num)]


def CreateDifferentBitNumber(bits, num):
    return CreateRandomNumber(2 ** (bits - 1), 2 ** bits - 1, num)


def TimingSingleAlgorithm(data, alg, p, idx):
    if alg != CT_IMI_CMMI:
        start = time.time()

        for each_data in data:
            alg(each_data, p)

        end = time.time()
        return float(end - start)
    else:
        start = time.time()

        for each_data in data:
            alg(each_data, p, P_round[idx])

        end = time.time()
        return float(end - start)


if __name__ == "__main__":

    idx = 0
    P = P_192

    bits_length_list = list(range(0 + 1, 192 + 1))
    data_list = [CreateDifferentBitNumber(bits_length, N) for bits_length in bits_length_list]

    for i, each_alg in enumerate(alg_list):
        time_list = []
        for j, each_data_list in enumerate(data_list):
            calc_time = TimingSingleAlgorithm(each_data_list, each_alg, P, idx)
            time_list.append(calc_time * scaled)
        output_path_time_list = os.path.join(output_path, 'Latency_of_' + test_alg[i] + '_for_P_' + P_name[idx] + '.txt')
        with open(output_path_time_list, 'w') as f:
            f.write('\n'.join(map(str, time_list)))

        print(test_alg[i], 'for', P_name[idx], 'finish')
    print('finish')
