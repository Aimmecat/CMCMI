import secrets
import os
import numpy as np
from Code.CTCMI import CT_IMI_CMMI, EEA
from Code.FitGaussian import Fit_Curve_Gaussian
from Code.VerifyGaussian import Verify_Gaussian

COVER_COPY_OUTPUT = True

cwd = os.getcwd()
output_path = os.path.join(cwd, '..', 'Output')
copy_output_path = os.path.join(cwd, '..', 'Copy_Output')
output_path_boundary = os.path.join(output_path, 'stored_boundary_n.txt')

N = int(10e2)

P_192 = 2 ** 192 - 2 ** 64 - 1
P_224 = 2 ** 224 - 2 ** 96 + 1
P_256 = 2 ** 256 - 2 ** 224 - 2 ** 96 + 2 ** 64 - 1
P_384 = 2 ** 384 - 2 ** 128 - 2 ** 96 + 2 ** 32 - 1
P_521 = 2 ** 521 - 1
P_1279 = 2 ** 1279 - 1
P_2281 = 2 ** 2281 - 1

P_list = [P_192, P_224, P_256, P_384, P_521, P_1279, P_2281]
P_name = ['192', '224', '256', '384', '521', '1279', '2281']

with open(output_path_boundary, 'r') as f:
    P_init_N = [int(line.strip()) for line in f]

if __name__ == "__main__":

    # Search
    for idx, P in enumerate(P_list):

        print("Starting create test number for P_", P_name[idx])

        # Create Test Number, random_test_number >= 2
        random_number_list = []
        for _ in range(N):
            random_test_number = secrets.randbelow(P-2) + 2
            random_number_list.append(random_test_number)

        print("Finishing create")

        boundary_n = P_init_N[idx]

        record_cnt = {}

        for i in range(N):
            calculate_result, cnt = CT_IMI_CMMI(random_number_list[i], P, boundary_n)
            verify_result = EEA(random_number_list[i], P)
            while calculate_result != verify_result:
                boundary_n += 1
                calculate_result, _ = CT_IMI_CMMI(random_number_list[i], P, boundary_n)
            if cnt not in record_cnt.keys():
                record_cnt[cnt] = 1
            else:
                record_cnt[cnt] += 1

        cnt_list, number = list(record_cnt.keys()), list(record_cnt.values())

        output_path_cnt_list = os.path.join(output_path, 'P_'+P_name[idx]+'_cnt_list.txt')
        output_path_cnt_number = os.path.join(output_path, 'P_'+P_name[idx]+'_number.txt')
        with open(output_path_cnt_list, 'w') as f:
            f.write('\n'.join(map(str, cnt_list)))
        with open(output_path_cnt_number, 'w') as f:
            f.write('\n'.join(map(str, number)))

        if COVER_COPY_OUTPUT:
            output_path_cnt_list = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_cnt_list.txt')
            output_path_cnt_number = os.path.join(copy_output_path, 'P_' + P_name[idx] + '_number.txt')
            with open(output_path_cnt_list, 'w') as f:
                f.write('\n'.join(map(str, cnt_list)))
            with open(output_path_cnt_number, 'w') as f:
                f.write('\n'.join(map(str, number)))

        P_init_N[idx] = boundary_n

        print("Search for P_", P_name[idx], ' finished, the boundary is', boundary_n)
        print("----------------------------------------------------")

    print("Search process finished")
    print("----------------------------------------------------")

    # store data
    with open(output_path_boundary, 'w') as f:
        f.write('\n'.join(map(str, P_init_N)))

    #Verify
    for idx, P in enumerate(P_list):
        print("Starting create verify number for P_", P_name[idx])

        random_number_list = []
        for _ in range(N):
            random_test_number = secrets.randbelow(P - 2) + 2
            random_number_list.append(random_test_number)

        print("Finishing create")
        print("----------------------------------------------------")

        for i in range(N):
            calculate_result, _ = CT_IMI_CMMI(random_number_list[i], P, P_init_N[idx])
            verify_result = EEA(random_number_list[i], P)
            if calculate_result != verify_result:
                print("Verify error for P_", P_name[idx], ' boudary is ', P_init_N[idx])
                assert (calculate_result == verify_result)
        print("Verify for P_", P_name[idx], ' passed')
        print("----------------------------------------------------")
    print("Verify process finished")
